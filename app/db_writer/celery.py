import os
import time

from celery import Celery, signals
from celery.signals import setup_logging

settings_module = os.getenv("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["apps.rules", "apps.notifications", "apps.telemetry"])


@setup_logging.connect
def disable_celery_logging(**kwargs):
    """
    Prevent Celery from hijacking/overwriting Django's LOGGING dictConfig.
    Django will configure handlers/formatters (including your JSON formatter).
    """
    pass