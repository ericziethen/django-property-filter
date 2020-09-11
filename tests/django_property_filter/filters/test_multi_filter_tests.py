
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
    NumberFilter,
    OrderingFilter,
)

from django_property_filter import (
    PropertyFilterSet,
    PropertyBooleanFilter,
    PropertyCharFilter,
    PropertyDateFilter,
    PropertyDateTimeFilter,
    PropertyMultipleChoiceFilter,
    PropertyNumberFilter,
    PropertyOrderingFilter,
    PropertyRangeFilter,
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

    def test_mixed_filters_all_applied(self):
        filter_number = 5
        filter_text = 'Five'
        filter_is_true = True
        filter_date = datetime.date(2018, 2, 1)
        filter_date_time = datetime.datetime(2019, 3, 2, 12)

        # Using a normal Filter
        filter_fs = MultiFilterFilterSet(
            {
                'number': filter_number,
                'text': filter_text,
                'is_true': filter_is_true,
                'date': filter_date,
                'date_time': filter_date_time
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        assert set(filter_fs.qs.values_list('id', flat=True)) == set([1])

        # Using property filter
        property_filter_fs = PropertyMultiFilterFilterSet(
            {
                'prop_number__exact': filter_number,
                'prop_text__exact': filter_text,
                'prop_is_true__exact': filter_is_true,
                'prop_date__exact': filter_date,
                'prop_date_time__exact': filter_date_time
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        assert set(filter_fs.qs) == set(property_filter_fs.qs)

        # Using mixed filters
        mixed_filter_fs = MixedFilterFilterSet(
            {
                'number': filter_number,
                'prop_text__exact': filter_text,
                'prop_is_true__exact': filter_is_true,
                'prop_date__exact': filter_date,
                'date_time': filter_date_time
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        assert set(filter_fs.qs) == set(mixed_filter_fs.qs)

    def test_filters_only_some_applied(self):
        property_filter_fs = PropertyMultiFilterFilterSet(
            {
                'prop_number__exact': 5,
                'prop_date_time__exact': datetime.datetime(2019, 3, 2, 12)
            },
            queryset=MultiFilterTestModel.objects.all()
        )

    def test_property_filters_only_some_applied(self):
        filter_fs = MultiFilterFilterSet(
            {
                'number': 5,
                'date_time': datetime.datetime(2019, 3, 2, 12)
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        assert set(filter_fs.qs.values_list('id', flat=True)) == set([1, 3, 4, 5])

    def test_mixed_filters_only_filters_applied(self):
        mixed_filter_fs = MixedFilterFilterSet(
            {
                'number': 5,
                'date_time': datetime.datetime(2019, 3, 2, 12)
            },
            queryset=MultiFilterTestModel.objects.all()
        )

        assert set(mixed_filter_fs.qs.values_list('id', flat=True)) == set([1, 3, 4, 5])

    def test_mixed_filters_only_property_filters_applied(self):
        mixed_filter_fs = MixedFilterFilterSet(
            {
                'prop_text__exact': 'Five',
                'prop_is_true__exact': True,
                'prop_date__exact': datetime.date(2018, 2, 1)
            },
            queryset=MultiFilterTestModel.objects.all()
        )
        assert set(mixed_filter_fs.qs.values_list('id', flat=True)) == set([1, 2, 6])

    def test_mixed_filters_only_some_of_each_filters_applied(self):
        mixed_filter_fs = MixedFilterFilterSet(
            {
                'number': 5,
                'prop_text__exact': 'Five',
            },
            queryset=MultiFilterTestModel.objects.all()
        )
        assert set(mixed_filter_fs.qs.values_list('id', flat=True)) == set([1, 4, 5, 6])


class MultiFilterMultipleChoiceTests(TestCase):

    def setUp(self):
        tz = timezone.get_default_timezone()

        MultiFilterTestModel.objects.create(
            id=1, number=5, text='Five', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=2, number=100, text='Five', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=3, number=500, text='Five', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))

        self.choices = [(c.number, F'Number: {c.number}') for c in MultiFilterTestModel.objects.order_by('id')]

    def test_multiple_choice_only(self):

        class MixedFilterWithMultipleChoiceFilterSet(PropertyFilterSet):
            prop_number = PropertyMultipleChoiceFilter(
                field_name='prop_number', lookup_expr='exact', conjoined=False,  # OR
                choices=self.choices)

            class Meta:
                model = MultiFilterTestModel
                fields = ['text', 'is_true', 'date', 'date_time']

        mixed_multi_choice_filter_fs = MixedFilterWithMultipleChoiceFilterSet(
            {
                'prop_number': [5, 500],
            },
            queryset=MultiFilterTestModel.objects.all()
        )
        assert set(mixed_multi_choice_filter_fs.qs.values_list('id', flat=True)) == set([1, 3])

    def test_multiple_choice_after_filter_found_nothing(self):

        class MixedFilterWithMultipleChoiceFilterSet(PropertyFilterSet):
            prop_number = PropertyMultipleChoiceFilter(
                field_name='prop_number', lookup_expr='exact', conjoined=False,  # OR
                choices=self.choices)

            class Meta:
                model = MultiFilterTestModel
                fields = ['text', 'is_true', 'date', 'date_time']

        mixed_multi_choice_filter_fs = MixedFilterWithMultipleChoiceFilterSet(
            {
                'text': 'NOT IN OUR LIST',
                'prop_number': [5, 500],
            },
            queryset=MultiFilterTestModel.objects.all()
        )
        assert not mixed_multi_choice_filter_fs.qs


class MultiFilterWithOrderingFilterTests(TestCase):

    def setUp(self):
        tz = timezone.get_default_timezone()

        MultiFilterTestModel.objects.create(id=1, number=1)
        MultiFilterTestModel.objects.create(id=2, number=3)
        MultiFilterTestModel.objects.create(id=3, number=5)
        MultiFilterTestModel.objects.create(id=4, number=4)
        MultiFilterTestModel.objects.create(id=5, number=2)

    @pytest.mark.debug
    def test_filtering(self):
        class TestFilterSet(PropertyFilterSet):
            prop_number_range = PropertyRangeFilter(field_name='prop_number', lookup_expr='range')
            number_order = OrderingFilter(fields=('number', 'number'))

            class Meta:
                model = MultiFilterTestModel
                exclude = ['id']

        # Filter Ordering
        filter_fs_order = TestFilterSet({'number_order': 'number'}, queryset=MultiFilterTestModel.objects.all())
        assert list(filter_fs_order.qs.values_list('id', flat=True)) == [1, 5, 2, 4, 3]

        # Prop Range Filter
        prop_filter_fs_order = TestFilterSet({'prop_number_range_min': 2, 'prop_number_range_max': 4}, queryset=MultiFilterTestModel.objects.all())
        assert set(prop_filter_fs_order.qs.values_list('id', flat=True)) == set([2, 4, 5])

        # Filter Ordering & Range Filter
        mixed_fs = TestFilterSet(
            {'prop_number_range_min': 2, 'prop_number_range_max': 4, 'number_order': 'number'},
            queryset=MultiFilterTestModel.objects.all())
        assert list(mixed_fs.qs.values_list('id', flat=True)) == [5, 2, 4]


class VolumeMultipleFilterTests(TestCase):

    def setUp(self):
        tz = timezone.get_default_timezone()
        max_entries = 40000
        self.number_range = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.text_range = ['One', 'Two', 'Three', 'Four', 'Five', ' Six', 'Seven', 'Eight', 'Nine']
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
