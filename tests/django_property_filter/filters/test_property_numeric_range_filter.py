

import pytest
from django_filters import FilterSet, NumericRangeFilter

from django_property_filter import PropertyFilterSet, PropertyNumericRangeFilter

from property_filter.models import NumericRangeFilterModel


@pytest.mark.parametrize('lookup', PropertyNumericRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyNumericRangeFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyNumericRangeFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyNumericRangeFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'range'


@pytest.fixture
def fixture_property_number_filter():
    NumericRangeFilterModel.objects.create(id=-1, number=-1)
    NumericRangeFilterModel.objects.create(id=0, number=0)
    NumericRangeFilterModel.objects.create(id=1, number=1)
    NumericRangeFilterModel.objects.create(id=2, number=2)
    NumericRangeFilterModel.objects.create(id=3, number=2)
    NumericRangeFilterModel.objects.create(id=4, number=2)
    NumericRangeFilterModel.objects.create(id=5, number=5)
    NumericRangeFilterModel.objects.create(id=6, number=7)


TEST_LOOKUPS = [
    ('range', (-1, 7), [-1, 0, 1, 2, 3, 4, 5, 6]),
    ('range', (2, 2), [2, 3, 4]),
    ('range', (3, 2), []),
    ('range', (7, 9), [6]),
    ('range', (8, 9), []),
    ('range', (2, None), []),
    ('range', (None, 2), []),
    ('range', (None, None), [-1, 0, 1, 2, 3, 4, 5, 6]),
]

@pytest.mark.debug
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_number_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class NumericRangeFilterSet(FilterSet):
        number = NumericRangeFilter(field_name='number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumericRangeFilterModel
            fields = ['number']

    filter_fs = NumericRangeFilterSet({'number_min': lookup_val[0], 'number_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyNumericRangeFilterSet(FilterSet):
        prop_number = PropertyNumericRangeFilter(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumericRangeFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyNumericRangeFilterSet({'prop_number_min': lookup_val[0], 'prop_number_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyNumericRangeFilterSet(PropertyFilterSet):
        prop_number = PropertyNumericRangeFilter(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumericRangeFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyNumericRangeFilterSet({'prop_number_min': lookup_val[0], 'prop_number_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = NumericRangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumericRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({'prop_number__range_min': lookup_val[0], 'prop_number__range_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyNumericRangeFilter.supported_lookups)
