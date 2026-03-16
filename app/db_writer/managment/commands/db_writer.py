from time import sleep
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Consume telemetry.raw in BATCHES, validate, route, and publish."

    def __init__(self):
        super().__init__()
        self._running = True
        
    def handle(self, *args, **kwargs):
        while True:
            print("im working here!!!")
            sleep(2)