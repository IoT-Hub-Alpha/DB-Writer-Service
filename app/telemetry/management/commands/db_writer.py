from time import sleep
from IoTKafka import IoTKafkaConsumer
from django.core.management.base import BaseCommand
from django.conf import settings
from app.telemetry.services.write_buffer import WriteBuffer

class Command(BaseCommand):
    help = "Consume telemetry.raw in BATCHES, validate, route, and publish."

    def __init__(self):
        super().__init__()
        self._running = True
        
    def add_arguments(self, parser):
        parser.add_argument(
            "--clean-topic", default=settings.KAFKA_TOPIC_TELEMETRY_CLEAN
        )
        parser.add_argument("--dlq-topic", default=settings.KAFKA_TOPIC_TELEMETRY_DLQ)
        parser.add_argument(
            "--writer-group-id", default=f"{settings.KAFKA_CLIENT_ID}-db-writer-clean"
        )
        parser.add_argument("--poll-timeout", type=float, default=1.0)
        parser.add_argument("--max-messages", type=int, default=0)

        parser.add_argument(
            "--batch-size",
            type=int,
            default=500,
            help="Number of messages to process in one batch",
        )
        
    def handle(self, *args, **options):
        clean_group_id, poll_timeout = (
            options["writer_group_id"],
            options["poll_timeout"],
        )
        clean_topic, dlq_topic = (
            options["clean_topic"],
            options["dlq_topic"],
        )
        batch_size = options["batch_size"]
        consumer_clean = IoTKafkaConsumer(group_id=clean_group_id, enable_auto_offset=False)
        consumer_clean.subscribe([clean_topic])
        
        write_buffer = WriteBuffer(consumer_clean, poll_timeout, batch_size)
        
        while self._running:
            write_buffer.handle()
            sleep(1)