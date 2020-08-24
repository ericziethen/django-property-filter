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
        - Filter Result Count
        - Property FIlter Result Count


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

from django_filters import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    DateFilter,
    DateTimeFilter,
    MultipleChoiceFilter,
    NumberFilter
)

from django_property_filter import (
    PropertyFilterSet,
    PropertyBooleanFilter,
    PropertyCharFilter,
    PropertyDateFilter,
    PropertyDateTimeFilter,
    PropertyMultipleChoiceFilter,
    PropertyNumberFilter
)
from django_property_filter.utils import get_db_vendor, get_db_version

from property_filter.models import MultiFilterTestModel

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


# Define the Test Ranges
NUMBER_RANGE = [1, 2, 3]
TEXT_RANGE = ['One', 'Two', 'Three']
IS_TRUE_RANGE = [True, False]
DATE_RANGE = [
    datetime.date(2018, 2, 1),
    datetime.date(2018, 3, 1),
    datetime.date(2018, 4, 1)
]
DATE_TIME_RANGE = [
    datetime.datetime(2066, 3, 2, 12, tzinfo=timezone.get_default_timezone()),
    datetime.datetime(2066, 3, 3, 12, tzinfo=timezone.get_default_timezone()),
    datetime.datetime(2066, 3, 4, 12, tzinfo=timezone.get_default_timezone())
]
NUMBER_CHOICES = [(c, F'Number: {c}') for c in NUMBER_RANGE]


class MultiFilterFilterSet(FilterSet):
    number = MultipleChoiceFilter(
        field_name='number', lookup_expr='exact', conjoined=False,  # OR
        choices=NUMBER_CHOICES)
    class Meta:
        model = MultiFilterTestModel
        fields = ['text', 'is_true', 'date', 'date_time']


class PropertyMultiFilterFilterSet(PropertyFilterSet):
    prop_number = PropertyMultipleChoiceFilter(
        field_name='prop_number', lookup_expr='exact', conjoined=False,  # OR
        choices=NUMBER_CHOICES)

    class Meta:
        model = MultiFilterTestModel
        fields = ['prop_number']
        exclude = ['number', 'text', 'is_true', 'date', 'date_time']
        property_fields = [
            ('prop_text', PropertyCharFilter, ['exact']),
            ('prop_is_true', PropertyBooleanFilter, ['exact']),
            ('prop_date', PropertyDateFilter, ['exact']),
            ('prop_date_time', PropertyDateTimeFilter, ['exact']),
        ]


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('db_entry_count', type=int)
        parser.add_argument('csv_out_path', type=str)

    def handle(self, *args, **options):  # pylint: disable=too-many-locals,too-many-branches
        csv_path = options['csv_out_path']
        db_entry_count = options['db_entry_count']

        # Setup The Database for Tests
        self.setup_test_db(db_entry_count)

        # Setup the Result Dic
        test_dic = {}
        test_dic['date/time'] = timezone.now()
        test_dic['version'] = get_plugin_version()
        test_dic['database'] = F'{get_db_vendor()} ({get_db_version()})'
        test_dic['Target DB Entries'] = db_entry_count
        test_dic['Actual DB Entries'] = MultiFilterTestModel.objects.all().count()

        # Run the Filtering
        self.run_filters(test_dic)

        # Log the Result/Csv Entries
        append_data_to_csv(csv_path, test_dic)

    def setup_test_db(self, db_entry_count):
        with transaction.atomic():
            # Clear Existing DB
            MultiFilterTestModel.objects.all().delete()

            # Generate Random Data
            bulk_list = []
            with transaction.atomic():
                for _ in range(1, db_entry_count + 1):
                    bulk_list.append(
                        MultiFilterTestModel(
                            number=random.choice(NUMBER_RANGE),
                            text=random.choice(TEXT_RANGE),
                            is_true=random.choice(IS_TRUE_RANGE),
                            date=random.choice(DATE_RANGE),
                            date_time=random.choice(DATE_TIME_RANGE)
                        )
                    )

                MultiFilterTestModel.objects.bulk_create(bulk_list)

    def run_filters(self, test_dic):
        # Setup the Filtersets
        filter_fs = MultiFilterFilterSet(
            {
                'number': [NUMBER_RANGE[0], NUMBER_RANGE[1]],
                'text': TEXT_RANGE[0],
                'is_true': IS_TRUE_RANGE[0],
                'date': DATE_RANGE[0],
                'date_time': DATE_TIME_RANGE[0]
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        property_filter_fs = PropertyMultiFilterFilterSet(
            {
                'prop_number': [NUMBER_RANGE[0], NUMBER_RANGE[1]],
                'prop_text__exact': TEXT_RANGE[0],
                'prop_is_true__exact': IS_TRUE_RANGE[0],
                'prop_date__exact': DATE_RANGE[0],
                'prop_date_time__exact': DATE_TIME_RANGE[0]
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        # Normal Filtering
        filter_start_time = timezone.now()
        fs_qs = filter_fs.qs
        filter_end_time = timezone.now()
        filer_duration = (filter_end_time - filter_start_time).total_seconds()

        # Property Filtering
        property_filter_start_time = timezone.now()
        pfs_qs = property_filter_fs.qs
        property_filter_end_time = timezone.now()
        property_filer_duration = (property_filter_end_time - property_filter_start_time).total_seconds()

        #print(fs_qs.query)
        #print(pfs_qs.query)
        if fs_qs or pfs_qs:
            assert fs_qs.count() == pfs_qs.count(), F'Counts "{fs_qs.count()}" and "{pfs_qs.count()}" differ'

        # Update Results
        test_dic['Filter Result Count'] = fs_qs.count()
        test_dic['Filter Time'] = F'{filer_duration} seconds'
        test_dic['Property Filter Result Count'] = pfs_qs.count()
        test_dic['Property Filter Time'] = F'{property_filer_duration} seconds'
        test_dic['Property Time Factor'] = property_filer_duration / filer_duration

def append_data_to_csv(csv_file_path, data):
        print(data)


def get_plugin_version():
    config = configparser.RawConfigParser()
    config.read('../../setup.cfg')
    version = config.get('metadata', 'version')
    return version
