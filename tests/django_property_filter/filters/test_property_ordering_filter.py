
import os

import pytest

from unittest.mock import patch

from django.db.models.query import QuerySet
from django.db.utils import OperationalError

from django_filters import FilterSet, OrderingFilter

from django_property_filter import PropertyFilterSet, PropertyOrderingFilter
from django_property_filter.utils import get_max_params_for_db

from property_filter.models import OrderingFilterModel


@pytest.mark.parametrize('lookup', PropertyOrderingFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyOrderingFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyOrderingFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyOrderingFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'exact'


def test_default_label():
    my_filter = PropertyOrderingFilter(field_name='fake_field')
    assert my_filter.label == 'Property Ordering'


@pytest.fixture
def fixture_property_number_filter():
        OrderingFilterModel.objects.create(id=-1, first_name='Bart', last_name='Simpson', username='El Barto', age=10)
        OrderingFilterModel.objects.create(id=0, first_name='Walter', last_name='White', username='Heisenberg', age=55)
        OrderingFilterModel.objects.create(id=1, first_name='Eric', last_name='Cartman', username='KylesMom', age=8)
        OrderingFilterModel.objects.create(id=2, first_name='Sonic', last_name='the Hedgehog', username='The Flash', age=16)
        OrderingFilterModel.objects.create(id=3, first_name='Lester', last_name='Nygaard', username='Innocent', age=45)
        OrderingFilterModel.objects.create(id=4, first_name='Lionel', last_name='Messi', username='Bola', age=35)
        OrderingFilterModel.objects.create(id=5, first_name='Misato', last_name='Katsuragi', username='Shinji', age=28)


@pytest.mark.django_db
def test_sorted_pk_list_ascending(fixture_property_number_filter):
    qs = OrderingFilterModel.objects.all()
    assert list(qs)[0].id == -1

    sorted_pk_list = PropertyOrderingFilter(field_name='fake_field').sorted_pk_list_from_property('prop_age', qs)
    assert sorted_pk_list == [1, -1, 2, 5, 4, 3, 0]


@pytest.mark.django_db
def test_sorted_pk_list_descending(fixture_property_number_filter):
    qs = OrderingFilterModel.objects.all()
    assert list(qs)[0].id == -1

    sorted_pk_list = PropertyOrderingFilter(field_name='fake_field').sorted_pk_list_from_property('-prop_age', qs)
    assert sorted_pk_list == [0, 3, 4, 5, 2, -1, 1]


TEST_LOOKUPS = [
    ('exact', '', '', [-1, 0, 1, 2, 3, 4, 5]),
    ('exact', 'age', 'prop_age', [1, -1, 2, 5, 4, 3, 0]),
    ('exact', '-age', '-prop_age', [0, 3, 4, 5, 2, -1, 1]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, lookup_val_prop, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_number_filter, lookup_xpr, lookup_val, lookup_val_prop, result_list):

    # Test using Normal Django Filter
    class OrderingFilterSet(FilterSet):
        age = OrderingFilter(fields=('age', 'age'))

        class Meta:
            model = OrderingFilterModel
            exclude = ['first_name', 'last_name', 'username']

    filter_fs = OrderingFilterSet({'age': lookup_val}, queryset=OrderingFilterModel.objects.all())

    # Keep order
    assert list(filter_fs.qs.values_list('id', flat=True)) == list(result_list)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyOrderingFilterSet(PropertyFilterSet):
        age = OrderingFilter(fields=('age', 'age'))
        prop_age = PropertyOrderingFilter(fields=('prop_age', 'prop_age'))

        class Meta:
            model = OrderingFilterModel
            exclude = ['first_name', 'last_name', 'username', 'age']

    filter_fs_mixed = PropertyOrderingFilterSet({'age': lookup_val}, queryset=OrderingFilterModel.objects.all())
    prop_filter_fs_mixed = PropertyOrderingFilterSet({'prop_age': lookup_val_prop}, queryset=OrderingFilterModel.objects.all())
    assert list(filter_fs_mixed.qs.values_list('id', flat=True)) == list(result_list)
    assert list(prop_filter_fs_mixed.qs.values_list('id', flat=True)) == list(result_list)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = OrderingFilterModel
            exclude = ['age']
            property_fields = [('prop_age', PropertyOrderingFilter, ['exact'])]

    with pytest.raises(ValueError):
        ImplicitFilterSet({F'prop_age__{lookup_xpr}': lookup_val_prop}, queryset=OrderingFilterModel.objects.all())


MAX_PARAM_TESTS = [
    (5, [1]),
    (6, [1, -1]),
]
@pytest.mark.django_db
@pytest.mark.parametrize('max_params, expected_result_list', MAX_PARAM_TESTS)
def test_ordering_max_limit_exceeded(fixture_property_number_filter, monkeypatch, max_params, expected_result_list):
    monkeypatch.setenv('USER_DB_MAX_PARAMS', str(max_params), prepend=False)

    assert get_max_params_for_db() == max_params

    class PropertyOrderingFilterSet(PropertyFilterSet):
        prop_age = PropertyOrderingFilter(fields=('prop_age', 'prop_age'))

        class Meta:
            model = OrderingFilterModel
            exclude = ['first_name', 'last_name', 'username', 'age']

    prop_filter_fs = PropertyOrderingFilterSet({'prop_age': 'prop_age'}, queryset=OrderingFilterModel.objects.all())

    with patch.object(QuerySet, 'count') as mock_method:
        mock_method.side_effect = (OperationalError(), None)
        assert list(prop_filter_fs.qs.values_list('id', flat=True)) == expected_result_list


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyOrderingFilter.supported_lookups)
