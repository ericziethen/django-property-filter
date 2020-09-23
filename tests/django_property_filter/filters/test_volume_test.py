
import datetime
import random

import pytest

from django.db import transaction
from django.test import TestCase
from django.utils import timezone

from property_filter.benchmark_utils import (
    SINGLE_FILTER_LOOKUP_LIST,
    BenchmarkModel,
    create_test_filtersets, remove_unneeded_filters_from_fs,
)

from tests.common import all_filter_volume_test_enabled

NUMBER_RANGE = range(100)
TEXT_RANGE = [str(x) for x in range(100)]
IS_TRUE_RANGE = [True, False]
DATE_RANGE = [
    datetime.date(2018, 2, 1),
    datetime.date(2018, 3, 1),
    datetime.date(2018, 4, 1),
    timezone.now().date()
]
# Unaware Times because not important for benchmarking, but easier for lookup because of str convertion
DATE_TIME_RANGE = [
    datetime.datetime(2066, 3, 2, 12),
    datetime.datetime(2070, 3, 3, 15),
    datetime.datetime(2076, 3, 4, 18)
]
ISO_DATE_TIME_RANGE = [
    '2020-01-03T12:00:00+12:00',
    '2020-01-03T12:00:00+11:00',
    '2021-12-03T12:00:00+10:00'
]
TIME_RANGE = [
    datetime.time(8, 0, 0),
    datetime.time(15, 15, 15),
    datetime.time(18, 30)
]

NUMBER_CHOICES = [(c, F'Number: {c}') for c in NUMBER_RANGE]
DURATION_RANGE = [
    datetime.timedelta(days=15),
    datetime.timedelta(days=30),
    datetime.timedelta(days=200)
]
UUID_RANGE = [
    '40828e84-66c7-46ee-a94a-1f2087970a68',
    'df4078eb-67ca-49fe-b86d-742e0feaf3ad',
    'aaaa78eb-67ca-49fe-b86d-742e0feaf3ad'
]


class LargeVolumeTests(TestCase):

    def setUp(self):
        db_entry_count = 350000

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

    @pytest.mark.skipif(not all_filter_volume_test_enabled(), reason='Large Volume Test only on Travis')
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')  # DayTime shows a Runtime Warning, ignore
    def test_large_volume_tests(self):  # Just making sure large filtering causes no issue
        for filter_name, prop_filter_name, lookup_value in SINGLE_FILTER_LOOKUP_LIST:
            _, _, property_filter_fs, _ = create_test_filtersets([(filter_name, prop_filter_name, lookup_value)])

            cleaned_property_filter_fs = remove_unneeded_filters_from_fs(property_filter_fs, [prop_filter_name])
            result_qs = cleaned_property_filter_fs.qs

            print(F'{result_qs.count():<100} ({prop_filter_name})')
