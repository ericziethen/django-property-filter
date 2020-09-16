
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from pyinstrument import Profiler

from property_filter.benchmark_utils import (
    NUMBER_RANGE, TEXT_RANGE, IS_TRUE_RANGE, DATE_RANGE, DATE_TIME_RANGE, ISO_DATE_TIME_RANGE,
    TIME_RANGE, DURATION_RANGE, UUID_RANGE,
    BenchmarkModel, create_test_filtersets, remove_unneeded_filters_from_fs,
)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('html_base_name_no_ext', type=str)


    def handle(self, *args, **options):  # pylint: disable=too-many-locals,too-many-branches
        self.db_entry_count = 100000

        self.html_base_name_no_ext = options['html_base_name_no_ext']

        print('db_entry_count', self.db_entry_count)
        print('self.html_base_name_no_ext', self.html_base_name_no_ext)

        # Use the same seed for each run, depending on number for consistent results
        random.seed(self.db_entry_count)

        # Setup The Database for Tests
        self.setup_test_db(self.db_entry_count)

        # run the Profiler
        self.run_profiler()

    def setup_test_db(self, db_entry_count):
        print('>>> setup_test_db')
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
        print('<<< setup_test_db')

    def profile_filterset(self, prof_fs, html_name_suffix_no_ext):
        print('>>> profile_filterset')

        profiler = Profiler()
        profiler.start()

        # code  profile
        result_qs = prof_fs.qs

        profiler.stop()

        #print('>>>', result_qs.values_list('number', flat=True))
        len(result_qs)  # Make sure no errors when evaluating the qs

        # Reset the Queryset to run the filters again
        delattr(prof_fs, '_qs')

        # Write to HTML
        with open(F'{self.html_base_name_no_ext}_{html_name_suffix_no_ext}_{self.db_entry_count}.html', 'w') as fptr:
            fptr.write(profiler.output_html())

        print('<<< profile_filterset')

    def run_profiler(self):
        profile_list = [
            ('number_NumberFilter', 'prop_number_PropertyNumberFilter', NUMBER_RANGE[0]),
            ('number_MultipleChoiceFilter_OR', 'prop_number_PropertyMultipleChoiceFilter_OR', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[1])]),
            ('number_MultipleChoiceFilter_AND', 'prop_number_PropertyMultipleChoiceFilter_AND', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[0])]),
            #('number_AllValuesFilter', 'prop_number_AllValuesFilter', NUMBER_RANGE[0]),
            #('number_AllValuesMultipleFilter_AND', 'prop_number_PropertyAllValuesMultipleFilter_AND', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[0])]),
            #('number_OrderingFilter', 'prop_number_PropertyOrderingFilter', ('number', 'prop_number')),
        ]

        for filter_name, prop_filter_name, lookup_value in profile_list:
            self.profile_filter(filter_name, prop_filter_name, lookup_value)

    def profile_filter(self, filter_name, prop_filter_name, lookup_value):
        print('>>> run_filter', filter_name, prop_filter_name, lookup_value)
        filter_fs, filter_names, property_filter_fs, prop_filter_names = create_test_filtersets(
            [(filter_name, prop_filter_name, lookup_value)])

        # Normal Filtering
        print('filter_names', filter_names)
        self.profile_filterset(filter_fs, filter_name)

        print('prop_filter_names', prop_filter_names)
        # Property Filtering large fs
        self.profile_filterset(property_filter_fs, prop_filter_name + '_large_fs')

        # Property Filtering smnall fs
        cleaned_property_filter_fs = remove_unneeded_filters_from_fs(property_filter_fs, [prop_filter_name])
        self.profile_filterset(cleaned_property_filter_fs, prop_filter_name + '_small_fs')

        print('<<< run_filter')
