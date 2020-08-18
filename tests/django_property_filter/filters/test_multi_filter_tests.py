
import datetime

import pytest

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

    @pytest.mark.debug
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
        # TODO - Setup Vulume Data, e.g. 100000
        pass

    @pytest.mark.debug
    def test_volume_test_comparison(self):

        # Using a normal Filter

        # Using property filter

        # Using mixed filters

        assert False