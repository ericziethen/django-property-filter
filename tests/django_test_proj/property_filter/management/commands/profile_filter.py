
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from property_filter.benchmark_utils import (
    NUMBER_RANGE, TEXT_RANGE, IS_TRUE_RANGE, DATE_RANGE, DATE_TIME_RANGE, ISO_DATE_TIME_RANGE,
    TIME_RANGE, DURATION_RANGE, UUID_RANGE,
    BenchmarkModel, create_test_filtersets,
)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--skipSetupDb', action='store_true', help='Skip Setup the DB')
        parser.add_argument('--skipFilter', action='store_true', help='Skip Filter')
        parser.add_argument('--skipPropertyFilter', action='store_true', help='Skip Property Filter')

    def handle(self, *args, **options):  # pylint: disable=too-many-locals,too-many-branches

        skip_db = options['skipSetupDb']
        self.skip_filter = options['skipFilter']
        self.skip_property_filter = options['skipPropertyFilter']

        print('skip_db', skip_db)
        print('self.skip_filter', self.skip_filter)
        print('self.skip_property_filter', self.skip_property_filter)

        if not skip_db:
            db_entry_count = 100000
            print('db_entry_count', db_entry_count)

            # Use the same seed for each run, depending on number for consistent results
            random.seed(db_entry_count)

            # Setup The Database for Tests
            self.setup_test_db(db_entry_count)
        else:
            print('Skip DB Setup')

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

    def profile_filterset(self, prof_fs):
        print('>>> profile_filterset')

        # code you want to profile
        prof_fs.qs

        print('<<< profile_filterset')

    def run_profiler(self):
        print('>>> run_filter')
        filter_name = 'number_MultipleChoiceFilter'
        prop_filter_name = 'prop_number_PropertyMultipleChoiceFilter'
        lookup_value = [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[1])]

        filter_fs, filter_names, property_filter_fs, prop_filter_names = create_test_filtersets(
            [(filter_name, prop_filter_name, lookup_value)])

        if not self.skip_filter:
            # Normal Filtering
            print('filter_names', filter_names)
            self.profile_filterset(filter_fs)
        else:
            print('Skip Filter profiling')

        if not self.skip_property_filter:
            # Property Filtering
            print('prop_filter_names', prop_filter_names)
            self.profile_filterset(property_filter_fs)
        else:
            print('Skip Property Filter profiling')

        print('<<< run_filter')
