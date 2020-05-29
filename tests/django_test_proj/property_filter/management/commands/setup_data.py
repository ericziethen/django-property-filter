
from django.core.management.base import BaseCommand

from property_filter.models import (
    NumberClass,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for num in range(21):
            NumberClass.objects.update_or_create(number=num)
