
from django.core.management.base import BaseCommand

from property_filter.models import (
    BooleanClass,
    NumberClass,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for num in range(21):
            NumberClass.objects.update_or_create(number=num)

        # Boolean Filters
        BooleanClass.objects.update_or_create(id=1, is_true=True)
        BooleanClass.objects.update_or_create(id=2, is_true=False)
        BooleanClass.objects.update_or_create(id=3, )
        BooleanClass.objects.update_or_create(id=4, is_true=True)
        BooleanClass.objects.update_or_create(id=5, is_true=False)
        BooleanClass.objects.update_or_create(id=6, )
