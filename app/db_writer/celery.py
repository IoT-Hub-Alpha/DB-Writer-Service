import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_writer.settings")

app = Celery("db_writer")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(['telemetry'])