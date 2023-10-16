from django.core.management.base import BaseCommand
from bus_data.tasks import download_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        download_data.delay()
