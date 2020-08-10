
import datetime
import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import make_aware

from property_filter.models import (
    VolumeTestModel,
)


class Command(BaseCommand):

    def handle(self, *args, **options):

        with transaction.atomic():
            # Clear the Data
            VolumeTestModel.objects.all().delete()

            # Add the Data
            self.setup_volume_test_model()

        print('>> Setup Finished')

    def setup_volume_test_model(self):
        print('Setup VolumeTestModel')

        max_entries = 10000
        is_true_range = [True, False]
        number_range = range(10)
        date_range = [timezone.now().date()]

        bulk_list = []

        # Create a List of Objects for Bulk Creation
        print(F'{timezone.now()} - Start Creating Bulk List')
        for entry_count in range(1, max_entries + 1):
            bulk_list.append(
                VolumeTestModel(
                    is_true=random.choice(is_true_range),
                    number=random.choice(number_range),
                    date=random.choice(date_range),
                    text=F'Entry {entry_count}'
                )
            )

        print(F'{timezone.now()} - Finished Creating Bulk List')

        # Bulk Create the List
        print(F'{timezone.now()} - Start Bulk Insert {len(bulk_list)} items')
        if bulk_list:
            VolumeTestModel.objects.bulk_create(bulk_list)

        print(F'{timezone.now()} - Finished Bulk Insert {len(bulk_list)} items')
