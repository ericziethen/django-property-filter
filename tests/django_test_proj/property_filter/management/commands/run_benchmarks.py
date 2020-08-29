'''
TODO - FEATURES


    # TODO
      - Add Simple Tests To Filter Every Filter
        - Start with the Intfield Initially
        - Loop through Each Filter
        - Run the same test as

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
        - Average Time / 10000 Tests (To compare different sample sizes with each other)

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

from django_filters import *

from django_property_filter import *
from django_property_filter.utils import get_db_vendor, get_db_version

from property_filter.filters import add_supported_filters, add_supported_property_filters
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

        result_dic_list = []

        # Setup the Base Result Data
        base_test_dic = {}
        base_test_dic['date/time'] = timezone.now()
        base_test_dic['version'] = get_plugin_version()
        base_test_dic['database'] = F'{get_db_vendor()} ({get_db_version()})'
        base_test_dic['Target DB Entries'] = db_entry_count
        base_test_dic['Actual DB Entries'] = MultiFilterTestModel.objects.all().count()

        # Run the Tests for each Filter as a Single Filter
        result_dic_list += self.run_all_filter_tests(base_test_dic.copy())

        # Run The combined Test with multiple filters
        result_dic_list += self.run_multi_filter_comparison(base_test_dic.copy())

        # Log the Result/Csv Entries
        append_data_to_csv(csv_path, result_dic_list)

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

    def run_all_filter_tests(self, test_dic):

        # TODO - Create a List of Filter Named when Creating the Base Filterset with all Filters
        # TODO - LOOP All filters
        #filter_fs = 

        #property_filter_fs = 
        return []

    def run_multi_filter_comparison(self, base_data_dic):
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

        self._run_filter_comparison(filter_fs, property_filter_fs, base_data_dic)

        return [base_data_dic]

    def _run_filter_comparison(self, filter_fs, property_filter_fs, test_dic):
        # TODO - Run Multiple Times and Take Average
        # TODO - Try with other Combinations of Filters???, single filter...
        # TODO - Have a loop to run basic tests on every Filter Separately
        #   - Can have 1 Big Filterset with each Filter (2, for Filter and Property)
        #       - Each filter for the same field/prop_filed
        #       - Name the Filter based on FilterName so loop can pick up, 
        #   - Then the Loop Can Filter for 1 of the Items for each of the filters and compare the 2

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

        # Update Results
        test_dic['Filter Result Count'] = fs_qs.count()
        test_dic['Filter Time'] = F'{filer_duration} seconds'
        test_dic['Property Filter Result Count'] = pfs_qs.count()
        test_dic['Property Filter Time'] = F'{property_filer_duration} seconds'

        if filer_duration:
            test_dic['Property Time Factor'] = property_filer_duration / filer_duration
        else:
            test_dic['Property Time Factor'] = 'Null Time for Filter'

        filter_list = get_filter_types_from_filter_names(filter_fs, filter_fs.data.keys())
        test_dic['Filters Used'] = sorted(filter_list)
        filter_list = get_filter_types_from_filter_names(property_filter_fs, property_filter_fs.data.keys())
        test_dic['Property Filters Used'] = sorted(filter_list)

        assert test_dic['Filter Result Count'] == test_dic['Property Filter Result Count']


def append_data_to_csv(csv_file_path, data_dic):
    for data in data_dic:
        print(data)


def get_plugin_version():
    config = configparser.RawConfigParser()
    config.read('../../setup.cfg')
    version = config.get('metadata', 'version')
    return version

def get_filter_types_from_filter_names(filterset, filter_name_list):
    type_list = []

    for name in filter_name_list:
        qualified_name = None

        # Check name as is
        if name in filterset.filters:
            qualified_name = name

        # Get name
        if qualified_name:
            type_list.append(filterset.filters[qualified_name].__class__.__name__)
        else:
            type_list.append(F'Unknown Type for "{name}"')

    return type_list




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

FILTER_LIST = [
    AllValuesFilter,
    AllValuesMultipleFilter,
    BaseCSVFilter,
    BaseInFilter,
    BaseRangeFilter,
    BooleanFilter,
    CharFilter,
    DateFilter,
    DateFromToRangeFilter,
    DateRangeFilter,
    DateTimeFilter,
    DateTimeFromToRangeFilter,
    DurationFilter,
    IsoDateTimeFilter,
    IsoDateTimeFromToRangeFilter,
    LookupChoiceFilter,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
    NumberFilter,
    OrderingFilter,
    RangeFilter,
    TimeFilter,
    TimeRangeFilter,
    UUIDFilter,
]

CHOICE_FILTER_LIST = [
    ChoiceFilter,
    MultipleChoiceFilter,
    TypedChoiceFilter,
    TypedMultipleChoiceFilter,
]

PROPERTY_FILTER_LIST = [
    PropertyAllValuesFilter,
    PropertyAllValuesMultipleFilter,
    PropertyBaseCSVFilter,
    PropertyBaseInFilter,
    PropertyBaseRangeFilter,
    PropertyBooleanFilter,
    PropertyCharFilter,
    PropertyDateFilter,
    PropertyDateFromToRangeFilter,
    PropertyDateRangeFilter,
    PropertyDateTimeFilter,
    PropertyDateTimeFromToRangeFilter,
    PropertyDurationFilter,
    PropertyIsoDateTimeFilter,
    PropertyIsoDateTimeFromToRangeFilter,
    PropertyLookupChoiceFilter,
    PropertyNumberFilter,
    PropertyOrderingFilter,
    PropertyRangeFilter,
    PropertyTimeFilter,
    PropertyTimeRangeFilter,
    PropertyUUIDFilter,
]

PROPERTY_CHOICE_FILTER_LIST = [
    PropertyChoiceFilter,
    PropertyMultipleChoiceFilter,
    PropertyTypedChoiceFilter,
    PropertyTypedMultipleChoiceFilter,
]

class AllFiltersNumberFilterSet(FilterSet):

    class Meta:
        model = MultiFilterTestModel
        exclude = ['number', 'text', 'is_true', 'date', 'date_time']

    def __init__(self, *args, **kwargs):
        for filt in FILTER_LIST + CHOICE_FILTER_LIST:
            lookup = 'exact'
            if lookup not in filt.supported_lookups:
                lookup = filt.supported_lookups[0]

            choices = None
            if filt in CHOICE_FILTER_LIST:
                choices = NUMBER_CHOICES
            add_supported_filters(self, filt, 'number', [lookup], choices=choices)

        super().__init__(*args, **kwargs)

        filter_type_list = [f__class__.__name__ for f in self.filters]
        for filt in FILTER_LIST + CHOICE_FILTER_LIST:
            assert filt in filter_type_list


class AllFiltersNumberPropertyFilterSet(PropertyFilterSet):

    class Meta:
        model = MultiFilterTestModel
        exclude = ['number', 'text', 'is_true', 'date', 'date_time']

    def __init__(self, *args, **kwargs):
        for filt in PROPERTY_FILTER_LIST + PROPERTY_CHOICE_FILTER_LIST:
            lookup = 'exact'
            if lookup not in filt.supported_lookups:
                lookup = filt.supported_lookups[0]

            choices = None
            if filt in CHOICE_FILTER_LIST:
                choices = PROPERTY_CHOICE_FILTER_LIST
            add_supported_filters(self, filt, 'number', [lookup], choices=choices)

        super().__init__(*args, **kwargs)

        filter_type_list = [f__class__.__name__ for f in self.filters]
        for filt in PROPERTY_FILTER_LIST + PROPERTY_CHOICE_FILTER_LIST:
            assert filt in filter_type_list

