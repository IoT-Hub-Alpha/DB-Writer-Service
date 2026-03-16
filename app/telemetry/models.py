from django.db import models
from django.contrib.postgres.indexes import GinIndex

class Telemetry(models.Model):
    id = models.BigAutoField(primary_key=True)
    device = models.CharField(max_length=200, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField(
        help_text=(
            'Schema: {"schema_version": "1.0", "serial_number": "SN123456", '
            '"value": 5.2}'
        )
    )

    class Meta:
        db_table = "telemetry"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(
                fields=["device", "-timestamp"], name="idx_telemetry_device_time"
            ),
            models.Index(fields=["-timestamp"], name="idx_telemetry_timestamp"),
            GinIndex(fields=["payload"], name="idx_telemetry_payload_gin"),
        ]
        verbose_name_plural = "Telemetry"

    def __str__(self):
        return f"Telemetry {self.id} - {str(self.device)} at {self.timestamp}"
