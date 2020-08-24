'''
TODO - FEATURES

    - Script Calls
        - 1000 Entries
        - 10000 Entries
        - 50000 Entries
        - 100000 Entries

    - Script Arguments
        - Number of Database Entries

    - Batch Script to call it, so can easily change the Database Used, and call both
    - Benchmark Model to Run Against
    - Multiple Databases (Sqlits + postgresql)
    - Multiple Number Database Entries
    - Multiple Datatypes
    - Multiple Filter Types (Single and Multiple Choice Ones)
    - Many (Single Filters) and Few (Multiple Filters) results
    - Compare Timing Filter & PropertyFilter
 
    - Tests
        - Single

    - LOGGING:
        - Log which Database is used

    FilterCombinations
        - Single Filter (NumberFilter)
        - Single Filter (CharFilter)
        - Single Filter (MultipleChoiceFilter AND)
        - Single Filter (MultipleChoiceFilter OR)
        - Mixed Filter (Number and Char Filter)
        - Mixed Filter (Number, Char Filter, Multiple Choice Filters)
        - Mixed Filter (5 Filters)

        call:TimeFilterAndPropetime_filters

    - CSV Output (1 Row per test scenario)
        x Date/Time
        x PropertyFilter Version used
        x Database Used
        x Database Entries
        - Results Found
        - Filters Used
        - Number of Fields Filtered
        - Filters Timing
        - Property Timing



    TimeFilterAndPropetime_filters(filter_dic, property_filter_dic, ???)  filter_dic/property_filter_dic = {'filter_name': lookup_value, 'name2': lookup_value...}
        time filterset.qs
        time propertyfilterset.qs
        log timing
'''

import configparser
import datetime
import logging
import os
import random
import sys

sys.path.insert(1, '../../')  # Find our main project

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from django_property_filter.utils import get_db_vendor, get_db_version

from property_filter.models import MultiFilterTestModel

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('db_entry_count', type=int)
        parser.add_argument('csv_out_path', type=str)

    def handle(self, *args, **options):  # pylint: disable=too-many-locals,too-many-branches
        csv_path = options['csv_out_path']
        db_entry_count = options['db_entry_count']

        # Setup The Database for Tests
        self.setup_test_db(db_entry_count)

        # Run the Filtering

        # Log the Result/Csv Entries


        # Single Test Entry
        test_dic = {}
        test_dic['date/time'] = timezone.now()
        test_dic['version'] = get_plugin_version()
        test_dic['database'] = F'{get_db_vendor()} ({get_db_version()})'
        test_dic['Target DB Entries'] = db_entry_count
        test_dic['Actual DB Entries'] = MultiFilterTestModel.objects.all().count()

        append_data_to_csv(csv_path, test_dic)

    def setup_test_db(self, db_entry_count):
        tz = timezone.get_default_timezone()

        # Define the Test Ranges
        number_range = [1, 2, 3]
        text_range = ['One', 'Two', 'Three']
        is_true_range = [True, False]
        date_range = [
            datetime.date(2018, 2, 1),
            datetime.date(2018, 3, 1),
            datetime.date(2018, 4, 1)
        ]
        date_time_range = [
            datetime.datetime(2066, 3, 2, 12, tzinfo=tz),
            datetime.datetime(2066, 3, 3, 12, tzinfo=tz),
            datetime.datetime(2066, 3, 4, 12, tzinfo=tz)
        ]

        with transaction.atomic():
            # Clear Existing DB
            MultiFilterTestModel.objects.all().delete()

            # Generate Random Data
            bulk_list = []
            with transaction.atomic():
                for _ in range(1, db_entry_count + 1):
                    bulk_list.append(
                        MultiFilterTestModel(
                            number=random.choice(number_range),
                            text=random.choice(text_range),
                            is_true=random.choice(is_true_range),
                            date=random.choice(date_range),
                            date_time=random.choice(date_time_range)
                        )
                    )

                MultiFilterTestModel.objects.bulk_create(bulk_list)


def append_data_to_csv(csv_file_path, data):
        print(data)


def get_plugin_version():
    config = configparser.RawConfigParser()
    config.read('../../setup.cfg')
    version = config.get('metadata', 'version')
    return version
