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
        X Results Found
        X Filters Used
        x Filters Timing
        x Property Timing
        x Filter Result Count
        x Property FIlter Result Count
        - Average Time / 10000 Tests (To compare different sample sizes with each other)

    TimeFilterAndPropetime_filters(filter_dic, property_filter_dic, ???)  filter_dic/property_filter_dic = {'filter_name': lookup_value, 'name2': lookup_value...}
        time filterset.qs
        time propertyfilterset.qs
        log timing
'''

import configparser
import logging
import os
import random
import sys
import pandas

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone, dateformat

sys.path.insert(1, '../../')  # Find our main project

from django_property_filter.utils import get_db_vendor, get_db_version

from property_filter.benchmark_utils import (
    NUMBER_RANGE, TEXT_RANGE, IS_TRUE_RANGE, DATE_RANGE, DATE_TIME_RANGE, ISO_DATE_TIME_RANGE,
    TIME_RANGE, DURATION_RANGE, UUID_RANGE,
    BenchmarkModel,
    ALL_VALUE_FILTER_LOOKUP_LIST, LOOKUP_CHOICE_FILTER_LOOKUP_LIST, FROM_TO_RANGE_FILTER_LOOKUP_LIST,
    MultiFilterFilterSet, PropertyMultiFilterFilterSet,
    AllFiltersFilterSet, AllFiltersPropertyFilterSet,
)


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
        base_test_dic['date/time'] = formatted_date = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        base_test_dic['version'] = get_plugin_version()
        base_test_dic['database'] = F'{get_db_vendor()} ({get_db_version()})'
        base_test_dic['Target DB Entries'] = db_entry_count
        base_test_dic['Actual DB Entries'] = BenchmarkModel.objects.all().count()

        # Run the Tests for each Filter as a Single Filter
        result_dic_list += self.run_all_filter_tests(base_test_dic.copy())

        # Run The combined Test with multiple filters
        result_dic_list += self.run_multi_filter_comparison(base_test_dic.copy())

        # Log the Result/Csv Entries
        append_data_to_csv(csv_path, result_dic_list)

    def setup_test_db(self, db_entry_count):
        with transaction.atomic():
            # Clear Existing DB
            BenchmarkModel.objects.all().delete()

            # Generate Random Data
            bulk_list = []
            with transaction.atomic():
                for _ in range(1, db_entry_count + 1):
                    bulk_list.append(
                        BenchmarkModel(
                            number=random.choice(NUMBER_RANGE),
                            text=random.choice(TEXT_RANGE),
                            is_true=random.choice(IS_TRUE_RANGE),
                            date=random.choice(DATE_RANGE),
                            date_time=random.choice(DATE_TIME_RANGE),
                            iso_date_time=random.choice(ISO_DATE_TIME_RANGE),
                            time=random.choice(TIME_RANGE),
                            duration=random.choice(DURATION_RANGE),
                            uuid=random.choice(UUID_RANGE)
                        )
                    )

                BenchmarkModel.objects.bulk_create(bulk_list)

    def run_all_filter_tests(self, base_data_dic):
        result_list = []

        # Normal Filter
        for filter_name, prop_filter_name, lookup_value in ALL_VALUE_FILTER_LOOKUP_LIST:
            filter_fs = AllFiltersFilterSet(
                {filter_name: lookup_value},
                queryset=BenchmarkModel.objects.all()
            )
            property_filter_fs = AllFiltersPropertyFilterSet(
                {prop_filter_name: lookup_value},
                queryset=BenchmarkModel.objects.all()
            )
            result_list.append(
                self._run_filter_comparison(
                    filter_fs, property_filter_fs, base_data_dic.copy(), [filter_name], [prop_filter_name]))

        # Special Case - Lookup Choice Filter
        for filter_name, prop_filter_name, lookup_value, lookup_expr in LOOKUP_CHOICE_FILTER_LOOKUP_LIST:
            filter_fs = AllFiltersFilterSet(
                {filter_name: lookup_value, F'{filter_name}_lookup': lookup_expr},
                queryset=BenchmarkModel.objects.all()
            )
            property_filter_fs = AllFiltersPropertyFilterSet(
                {prop_filter_name: lookup_value, F'{prop_filter_name}_lookup': lookup_expr},
                queryset=BenchmarkModel.objects.all()
            )
            result_list.append(
                self._run_filter_comparison(
                    filter_fs, property_filter_fs, base_data_dic.copy(), [filter_name], [prop_filter_name]))

        # Special Case - Range Filter
        for filter_name, prop_filter_name, from_name, range_from, to_name, range_to in FROM_TO_RANGE_FILTER_LOOKUP_LIST:
            filter_fs = AllFiltersFilterSet(
                {F'{filter_name}_{from_name}': range_from, F'{filter_name}_{to_name}': range_to},
                queryset=BenchmarkModel.objects.all()
            )
            property_filter_fs = AllFiltersPropertyFilterSet(
                {F'{prop_filter_name}_{from_name}': range_from, F'{prop_filter_name}_{to_name}': range_to},
                queryset=BenchmarkModel.objects.all()
            )
            result_list.append(
                self._run_filter_comparison(
                    filter_fs, property_filter_fs, base_data_dic.copy(), [filter_name], [prop_filter_name]))

        return result_list

    def run_multi_filter_comparison(self, base_data_dic):
        filter_fs = MultiFilterFilterSet(
            {
                'number': [NUMBER_RANGE[0], NUMBER_RANGE[1]],
                'text': TEXT_RANGE[0],
                'is_true': IS_TRUE_RANGE[0],
                'date': DATE_RANGE[0],
                'date_time': DATE_TIME_RANGE[0]
            },
            queryset=BenchmarkModel.objects.all()
        )

        property_filter_fs = PropertyMultiFilterFilterSet(
            {
                'prop_number': [NUMBER_RANGE[0], NUMBER_RANGE[1]],
                'prop_text__exact': TEXT_RANGE[0],
                'prop_is_true__exact': IS_TRUE_RANGE[0],
                'prop_date__exact': DATE_RANGE[0],
                'prop_date_time__exact': DATE_TIME_RANGE[0]
            },
            queryset=BenchmarkModel.objects.all()
        )

        return [self._run_filter_comparison(
            filter_fs, property_filter_fs, base_data_dic, filter_fs.data.keys(), property_filter_fs.data.keys())]

    def _run_filter_comparison(self, filter_fs, property_filter_fs, test_dic, filters_used, prop_filters_used):
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
        filer_duration_100k = filer_duration / test_dic['Actual DB Entries'] * 100000

        # Property Filtering
        property_filter_start_time = timezone.now()
        pfs_qs = property_filter_fs.qs
        property_filter_end_time = timezone.now()
        property_filer_duration = (property_filter_end_time - property_filter_start_time).total_seconds()
        property_filer_duration_100k = property_filer_duration / test_dic['Actual DB Entries'] * 100000

        # Update Results
        test_dic['Filter Result Count'] = fs_qs.count()
        test_dic['Filter Time sec'] = F'{filer_duration:.2f}'
        test_dic['Filter Time sec / 100k'] = F'{filer_duration_100k:.2f}'

        test_dic['Property Filter Result Count'] = pfs_qs.count()
        test_dic['Property Filter Time sec'] = F'{property_filer_duration:.2f}'
        test_dic['Property Filter Time sec / 100k'] = F'{property_filer_duration_100k:.2f}'

        if filer_duration:
            test_dic['Property Time Factor'] = F'{property_filer_duration / filer_duration:.2f}'
        else:
            test_dic['Property Time Factor'] = 'Null Time for Filter'

        filter_list = get_filter_types_from_filter_names(filter_fs, filters_used)
        test_dic['Filters Used'] = sorted(filter_list)
        filter_list = get_filter_types_from_filter_names(property_filter_fs, prop_filters_used)
        test_dic['Property Filters Used'] = sorted(filter_list)

        # Sqlite doesn't always return all values
        #assert test_dic['Filter Result Count'] == test_dic['Property Filter Result Count']

        full_qs_always = test_dic['Filters Used'] == ['OrderingFilter']
        if not full_qs_always:  # e.g. ordering Filter only sorts, doesn't filter
            assert 0 < test_dic['Filter Result Count'] < test_dic['Actual DB Entries'],\
                F'''{test_dic['Filters Used']}, {test_dic['Filter Result Count']}, {test_dic['Actual DB Entries']})'''

        full_qs_always = test_dic['Property Filters Used'] == ['PropertyOrderingFilter']
        if not full_qs_always:  # e.g. ordering Filter only sorts, doesn't filter
            assert 0 < test_dic['Property Filter Result Count'] < test_dic['Actual DB Entries'],\
                F'''{test_dic['Property Filters Used']}, {test_dic['Property Filter Result Count']}, {test_dic['Actual DB Entries']}'''

        return test_dic

def append_data_to_csv(csv_file_path, data_dic_list):
    for data in data_dic_list:
        print(data)

    header = not os.path.exists(csv_file_path)

    df = pandas.DataFrame(data_dic_list)
    df.to_csv(csv_file_path, mode='a', encoding='utf-8', index=False, header=header)


def get_plugin_version():
    config = configparser.RawConfigParser()
    config.read('../../setup.cfg')
    version = config.get('metadata', 'version')
    return version

def get_filter_types_from_filter_names(filterset, filter_name_list=None):
    type_list = []
    unknown_list = []

    if not filter_name_list:
        filter_name_list = filterset.data.keys()

    for name in filter_name_list:
        qualified_name = None

        # Check name as is
        if name in filterset.filters:
            qualified_name = name

        # Get name
        if qualified_name:
            type_list.append(filterset.filters[qualified_name].__class__.__name__)
        else:
            unknown_list.append(F'Unknown Type for "{name}"')

    # In some cases  has multiple entries, not all are the filternames but could be expressions
    if not type_list:
        type_list = unknown_list

    # TODO
    #    = Lookup FIlter even if has suffix e.g. after, from ...
    #    = Only Return a Single one of Each i.e set
    #print(filterset.filters.keys())
    #print(filterset.data.keys())
    #raise ValueError('ERIC')


    return list(set(type_list))
