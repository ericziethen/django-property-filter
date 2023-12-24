
import datetime
import logging

import pytest

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.utils import timezone

from property_filter.models import NumberFilterModel, MultiFilterTestModel, RelatedMultiFilterTestModel

from django_filters import FilterSet
from django_filters.filters import NumberFilter

from django_property_filter import PropertyNumberFilter


def test_label_set():
    my_filter_label = PropertyNumberFilter(label='test label', field_name='field_name', lookup_expr='gte')
    assert my_filter_label.label == 'test label'

    my_filter_no_label = PropertyNumberFilter(field_name='field_name', lookup_expr='gte')
    assert my_filter_no_label.label == 'field_name [gte]'

def test_handle_invalid_type_comparison(caplog):

    num_filter = PropertyNumberFilter(field_name='field_name', lookup_expr='lt')

    with caplog.at_level(logging.DEBUG):
        result = num_filter._compare_lookup_with_qs_entry(num_filter.lookup_expr, 'text', 15)

        assert not result
        assert 'Error during comparing ' in caplog.text


class FilterFunctionalityTests(TestCase):

    def setUp(self):
        NumberFilterModel.objects.create(id=1, number=1)
        NumberFilterModel.objects.create(id=2, number=2)
        NumberFilterModel.objects.create(id=3, number=3)
        NumberFilterModel.objects.create(id=4, number=4)
        NumberFilterModel.objects.create(id=5, number=5)

    def test_calling_filter_directly_raises_exception(self):
        my_filter = PropertyNumberFilter(label='test label', field_name='prop_number', lookup_expr='gte')

        with pytest.raises(ImproperlyConfigured):
            my_filter.filter(NumberFilterModel.objects.all(), 15)

    def test_filter_pks_no_initial_list(self):
        my_filter = PropertyNumberFilter(field_name='prop_number', lookup_expr='gt')
        initial_pk_list = None
        pk_list = my_filter.filter_pks(initial_pk_list, NumberFilterModel.objects.all(), 2)

        assert set(pk_list) == set([3, 4, 5])

    def test_filter_pks_initial_list(self):
        my_filter = PropertyNumberFilter(field_name='prop_number', lookup_expr='gt')
        initial_pk_list = [1, 4, 5]
        pk_list = my_filter.filter_pks(initial_pk_list, NumberFilterModel.objects.all(), 2)

        assert set(pk_list) == set([4, 5])

    def test_filter_pks_initial_list_empty(self):
        my_filter = PropertyNumberFilter(field_name='prop_number', lookup_expr='gt')
        initial_pk_list = []
        pk_list = my_filter.filter_pks(initial_pk_list, NumberFilterModel.objects.all(), 2)

        assert pk_list == []  # Specific test for an Empty List

    def test_filter_pks_no_testing_value(self):
        my_filter = PropertyNumberFilter(field_name='prop_number', lookup_expr='gt')
        initial_pk_list = [1, 5, 9]
        pk_list = my_filter.filter_pks(initial_pk_list, NumberFilterModel.objects.all(), None)

        assert set(pk_list) == set([1, 5, 9])


class RelatedModelFilterTests(TestCase):
    def setUp(self):
        tz = timezone.get_default_timezone()

        MultiFilterTestModel.objects.create(
            id=1, number=5, text='Five', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))

        MultiFilterTestModel.objects.create(
            id=2, number=5, text='Five', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))

        MultiFilterTestModel.objects.create(
            id=3, number=1, text='One', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))

        RelatedMultiFilterTestModel.objects.create(
            id=1, multi_filter=MultiFilterTestModel.objects.get(id=1))
        RelatedMultiFilterTestModel.objects.create(
            id=2, multi_filter=None)
        RelatedMultiFilterTestModel.objects.create(
            id=3, multi_filter=None)
        RelatedMultiFilterTestModel.objects.create(
            id=4, multi_filter=MultiFilterTestModel.objects.get(id=2))


    def test_filter_related_object_find_numbers(self):
        # Setup django_filter for comparison
        class NumberFilterSet(FilterSet):
            number = NumberFilter(field_name='multi_filter__number', lookup_expr='exact')

            class Meta:
                model = RelatedMultiFilterTestModel
                fields = ['multi_filter__number']

        filter_fs = NumberFilterSet({'multi_filter__number': 5}, queryset=RelatedMultiFilterTestModel.objects.all())
        filter_pk_list = filter_fs.qs.values_list('id', flat=True)

        # Test filter result
        assert set(filter_pk_list) == set([1, 4])

        # Setup Property Filter
        my_prop_filter = PropertyNumberFilter(field_name='multi_filter__prop_number', lookup_expr='exact')
        prop_filter_pk_list = my_prop_filter.filter_pks(None, RelatedMultiFilterTestModel.objects.all(), 5)

        # Test Property Filter result
        assert set(filter_pk_list) == set(prop_filter_pk_list)
