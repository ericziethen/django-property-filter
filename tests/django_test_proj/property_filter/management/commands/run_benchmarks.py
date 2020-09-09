import configparser
import datetime
import logging
import os
import pandas
import random
import sys

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone, dateformat

sys.path.insert(1, '../../')  # Find our main project

from django_property_filter.utils import get_db_vendor, get_db_version

from property_filter.benchmark_utils import (
    NUMBER_RANGE, TEXT_RANGE, IS_TRUE_RANGE, DATE_RANGE, DATE_TIME_RANGE, ISO_DATE_TIME_RANGE,
    TIME_RANGE, DURATION_RANGE, UUID_RANGE,
    SINGLE_FILTER_LOOKUP_LIST, MULTI_FILTER_LOOKUP_LIST, LOOKUP_FILTER_TYPES,
    BenchmarkModel,
    get_filtertype_from_filter_name, get_filter_types_from_filter_names, get_range_suffixes_for_filter_type,
    create_test_filtersets, remove_unneeded_filters_from_fs,
)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('db_entry_count', type=int)
        parser.add_argument('csv_out_path', type=str)

    def handle(self, *args, **options):  # pylint: disable=too-many-locals,too-many-branches
        self.csv_path = options['csv_out_path']
        db_entry_count = options['db_entry_count']

        self.repeat_count = 3

        # Use the same seed for each run, depending on number for consistent results
        random.seed(db_entry_count)

        # Setup The Database for Tests
        self.setup_test_db(db_entry_count)

        result_dic_list = []

        # Setup the Base Result Data
        base_test_dic = {}
        base_test_dic['version'] = get_plugin_version()
        base_test_dic['database'] = F'{get_db_vendor()} ({get_db_version()})'
        base_test_dic['Target DB Entries'] = db_entry_count
        base_test_dic['Actual DB Entries'] = BenchmarkModel.objects.all().count()

        # Run the Tests for each Filter as a Single Filter
        self.run_all_filter_tests(base_test_dic.copy())

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

        # Normal Filter
        for filter_name, prop_filter_name, lookup_value in SINGLE_FILTER_LOOKUP_LIST:
            result_list = []

            filter_fs, filter_names, property_filter_fs, prop_filter_names = create_test_filtersets([(filter_name, prop_filter_name, lookup_value)])

            # Run the Tests
            result_list.append(
                self._run_filter_comparison(
                    filter_fs, property_filter_fs, base_data_dic.copy(), [filter_name], [prop_filter_name]))

            append_data_to_csv(self.csv_path, result_list)

        # Multi Filter
        for filter_info in MULTI_FILTER_LOOKUP_LIST:
            result_list = []

            filter_fs, filter_names, property_filter_fs, prop_filter_names = create_test_filtersets(filter_info)

            # Run the Tests
            result_list.append(
                self._run_filter_comparison(
                    filter_fs, property_filter_fs, base_data_dic.copy(),
                    filter_names, prop_filter_names))

            append_data_to_csv(self.csv_path, result_list)

    def _time_filterset(self, fs, repeat_count):
        duration = datetime.timedelta(0)

        for _ in range(repeat_count):

            filter_start_time = timezone.now()
            fs_qs = fs.qs
            filter_end_time = timezone.now()
            duration += (filter_end_time - filter_start_time)
            count = fs_qs.count()

            # Reset the Queryset to run the filters again
            delattr(fs, '_qs')

        return ((duration / repeat_count).total_seconds(), count)

    def _run_filter_comparison(self, filter_fs, property_filter_fs, test_dic, filters_used, prop_filters_used):

        # Filtering with all Filters Enabled
        filer_duration, filter_count = self._time_filterset(filter_fs, self.repeat_count)
        prop_filter_duration, prop_filter_count = self._time_filterset(property_filter_fs, self.repeat_count)

        # Filtering with only a single Filter - This will remove Filters from the Filterset
        cleaned_filter_fs = remove_unneeded_filters_from_fs(filter_fs, filters_used)
        single_filter_duration, _ = self._time_filterset(cleaned_filter_fs, self.repeat_count)
        cleaned_property_filter_fs = remove_unneeded_filters_from_fs(property_filter_fs, prop_filters_used)
        single_prop_filter_duration, _ = self._time_filterset(cleaned_property_filter_fs, self.repeat_count)


        # Update Results
        test_dic['date/time'] = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        test_dic['Repetitions'] = self.repeat_count
        test_dic['Filter Results'] = filter_count
        test_dic['Filter Time large fs'] = F'{filer_duration:.2f}'
        test_dic['Filter Time small fs'] = F'{single_filter_duration:.2f}'

        test_dic['Prop Filter Results'] = prop_filter_count
        test_dic['Prop Filter Time large fs'] = F'{prop_filter_duration:.2f}'
        test_dic['Prop Filter Time small fs'] = F'{single_prop_filter_duration:.2f}'

        if filer_duration:
            test_dic['Prop Time Factor'] = F'{prop_filter_duration / filer_duration:.2f}'
        else:
            test_dic['Prop Time Factor'] = 'N/A'

        filter_list = get_filter_types_from_filter_names(filter_fs, filters_used)
        test_dic['Filters Used'] = sorted(filter_list)
        filter_list = get_filter_types_from_filter_names(property_filter_fs, prop_filters_used)
        test_dic['Prop Filters Used'] = sorted(filter_list)

        full_qs_always = test_dic['Filters Used'] == ['OrderingFilter']
        if not full_qs_always:  # e.g. ordering Filter only sorts, doesn't filter
            assert 0 < test_dic['Filter Results'] < test_dic['Actual DB Entries'],\
                F'''{test_dic['Filters Used']}, {test_dic['Filter Results']}, {test_dic['Actual DB Entries']})'''

        full_qs_always = test_dic['Prop Filters Used'] == ['PropertyOrderingFilter']
        if not full_qs_always:  # e.g. ordering Filter only sorts, doesn't filter
            assert 0 < test_dic['Prop Filter Results'] < test_dic['Actual DB Entries'],\
                F'''{test_dic['Prop Filters Used']}, {test_dic['Prop Filter Results']}, {test_dic['Actual DB Entries']}'''

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
