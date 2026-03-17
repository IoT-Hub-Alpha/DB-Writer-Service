import logging
from uuid import UUID
from celery import shared_task
from typing import Any
from dataclasses import dataclass
from django.db import OperationalError, InterfaceError
from IoTKafka import IoTKafkaProducer
from django.db.utils import DatabaseError
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.db import transaction
from celery.exceptions import MaxRetriesExceededError
from telemetry.services.publish_to_dlq import publish_flush_to_dlq
from telemetry.models import Telemetry


@dataclass
class WriterResult:
    success: bool = True
    written_to_db: int = 0
    written_to_dlq: int = 0

    def to_dict(self):
        return {
            "success": self.success,
            "written_to_db": self.written_to_db,
            "written_to_dlq": self.written_to_dlq,
        }


logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2, default_retry_delay=60)
def bulk_telemetry_write(self, flush) -> dict[str, Any]:
    producer = IoTKafkaProducer()
    result = WriterResult()
    telem_data = []
    bad_data = []

    try:
        for p in flush:
            if not p.get("device_serial"):
                logger.warning(
                    "empty serial!", extra={"device": p.get("device_serial")}
                )
                bad_data.append(p)
                continue
            telem_data.append(
                Telemetry(payload=p.get("payload"), device=p.get("device_serial"))
            )

        if bad_data:
            logger.warning("No device id detected", extra={"bad_data": bad_data})

            result.written_to_dlq += len(bad_data)

            publish_flush_to_dlq(producer, bad_data, reason="Wrong device serial")

        if not telem_data:
            logger.info("Nothing to write, Bad batch")
            return result.to_dict()

        logger.info(
            f"Attempting flush of {len(flush)} size, attempt {self.request.retries}",
            extra={"retry_num": self.request.retries, "buffeR_size": len(flush)},
        )

        with transaction.atomic():
            Telemetry.objects.bulk_create(
                telem_data, batch_size=settings.DB_INSERT_BATCH_SIZE
            )
            result.written_to_db += len(telem_data)
            logger.info("Successfully written to DB")

    except (OperationalError, InterfaceError, DatabaseError) as e:
        try:
            logger.warning(
                f"DB Write failed due to: {e}, attempt {self.request.retries}"
            )
            raise self.retry(countdown=60 * (2**self.request.retries))
        except MaxRetriesExceededError:
            logger.warning("DB Write attemps execceded max, dumping batch to telem.dlq")
            if publish_flush_to_dlq(producer, flush, reason="Failed DB Write"):
                result.written_to_dlq += len(flush)
            else:
                result.success = False

    return result.to_dict()
