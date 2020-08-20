
import datetime
import random

import pytest

from django.db import transaction
from django.test import TestCase
from django.utils import timezone

from django_filters import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    DateFilter,
    DateTimeFilter,
    NumberFilter
)

from django_property_filter import (
    PropertyFilterSet,
    PropertyBooleanFilter,
    PropertyCharFilter,
    PropertyDateFilter,
    PropertyDateTimeFilter,
    PropertyNumberFilter
)

from property_filter.models import MultiFilterTestModel


class MultiFilterFilterSet(FilterSet):

    class Meta:
        model = MultiFilterTestModel
        fields = ['number', 'text', 'is_true', 'date', 'date_time']


class PropertyMultiFilterFilterSet(PropertyFilterSet):

    class Meta:
        model = MultiFilterTestModel
        exclude = ['id']
        property_fields = [
            ('prop_number', PropertyNumberFilter, ['exact']),
            ('prop_text', PropertyCharFilter, ['exact']),
            ('prop_is_true', PropertyBooleanFilter, ['exact']),
            ('prop_date', PropertyDateFilter, ['exact']),
            ('prop_date_time', PropertyDateTimeFilter, ['exact']),
        ]


class MixedFilterFilterSet(PropertyFilterSet):

    class Meta:
        model = MultiFilterTestModel
        fields = ['number', 'date_time']
        property_fields = [
            ('prop_text', PropertyCharFilter, ['exact']),
            ('prop_is_true', PropertyBooleanFilter, ['exact']),
            ('prop_date', PropertyDateFilter, ['exact']),
        ]


class SequentialMultipleFilterTests(TestCase):

    def setUp(self):
        tz = timezone.get_default_timezone()

        MultiFilterTestModel.objects.create(
            id=1, number=5, text='Five', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=2, number=999, text='Five', is_true=True,  # Different number
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=3, number=5, text='One Million', is_true=True,  # Different text
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=4, number=5, text='Five', is_true=False,  # Different is_true
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=5, number=5, text='Five', is_true=True,
            date=datetime.date(2050, 2, 1),  # Different date
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=6, number=5, text='Five', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2066, 3, 2, 12, tzinfo=tz))  # Different DateTime

        self.filter_number = 5
        self.filter_text = 'Five'
        self.filter_is_true = True
        self.filter_date = datetime.date(2018, 2, 1)
        self.filter_date_time = datetime.datetime(2019, 3, 2, 12)

        self.expected_id_list_left = [1]

    def test_multiple_filters_applied(self):

        # Using a normal Filter
        filter_fs = MultiFilterFilterSet(
            {
                'number': self.filter_number,
                'text': self.filter_text,
                'is_true': self.filter_is_true,
                'date': self.filter_date,
                'date_time': self.filter_date_time
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        assert set(filter_fs.qs.values_list('id', flat=True)) == set(self.expected_id_list_left)

        # Using property filter
        property_filter_fs = PropertyMultiFilterFilterSet(
            {
                'prop_number__exact': self.filter_number,
                'prop_text__exact': self.filter_text,
                'prop_is_true__exact': self.filter_is_true,
                'prop_date__exact': self.filter_date,
                'prop_date_time__exact': self.filter_date_time
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        assert set(filter_fs.qs) == set(property_filter_fs.qs)

        # Using mixed filters
        mixed_filter_fs = MixedFilterFilterSet(
            {
                'number': self.filter_number,
                'prop_text__exact': self.filter_text,
                'prop_is_true__exact': self.filter_is_true,
                'prop_date__exact': self.filter_date,
                'date_time': self.filter_date_time
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        assert set(filter_fs.qs) == set(mixed_filter_fs.qs)


class VolumeMultipleFilterTests(TestCase):

    def setUp(self):
        tz = timezone.get_default_timezone()
        max_entries = 40000
        self.number_range = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.text_range = ['One', 'Two', 'Three', 'Four', 'Five'' Six', 'Seven', 'Eight', 'Nine']
        self.is_true_range = [True, False]
        self.date_range = [
            datetime.date(2018, 2, 1),
            datetime.date(2018, 3, 1),
            datetime.date(2018, 4, 1),
            datetime.date(2018, 5, 1),
            datetime.date(2018, 6, 1)
        ]
        self.date_time_range = [
            datetime.datetime(2066, 3, 2, 12, tzinfo=tz),
            datetime.datetime(2066, 3, 3, 12, tzinfo=tz),
            datetime.datetime(2066, 3, 4, 12, tzinfo=tz),
            datetime.datetime(2066, 3, 5, 12, tzinfo=tz),
            datetime.datetime(2066, 3, 6, 12, tzinfo=tz),
        ]

        bulk_list = []
        with transaction.atomic():
            for _ in range(1, max_entries + 1):
                bulk_list.append(
                    MultiFilterTestModel(
                        number=random.choice(self.number_range),
                        text=random.choice(self.text_range),
                        is_true=random.choice(self.is_true_range),
                        date=random.choice(self.date_range),
                        date_time=random.choice(self.date_time_range)
                    )
                )

            MultiFilterTestModel.objects.bulk_create(bulk_list)

    def test_volume_same_result(self):

        filter_fs = MultiFilterFilterSet(
            {
                'number': self.number_range[0],
                'text': self.text_range[0],
                'is_true': self.is_true_range[0],
                'date': self.date_range[0],
                'date_time': self.date_time_range[0]
            },
            queryset=MultiFilterTestModel.objects.all()
        )


        property_filter_fs = PropertyMultiFilterFilterSet(
            {
                'prop_number__exact': self.number_range[0],
                'prop_text__exact': self.text_range[0],
                'prop_is_true__exact': self.is_true_range[0],
                'prop_date__exact': self.date_range[0],
                'prop_date_time__exact': self.date_time_range[0]
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        mixed_filter_fs = MixedFilterFilterSet(
            {
                'number': self.number_range[0],
                'prop_text__exact': self.text_range[0],
                'prop_is_true__exact': self.is_true_range[0],
                'prop_date__exact': self.date_range[0],
                'date_time': self.date_time_range[0]
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        fs_qs = filter_fs.qs
        pfs_qs = property_filter_fs.qs
        mixed_qs = mixed_filter_fs.qs

        assert set(fs_qs) == set(pfs_qs)
        assert set(fs_qs) == set(mixed_qs)
