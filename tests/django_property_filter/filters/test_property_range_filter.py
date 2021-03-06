

import pytest
from django_filters import FilterSet, RangeFilter

from django_property_filter import PropertyFilterSet, PropertyRangeFilter

from property_filter.models import RangeFilterModel


@pytest.mark.parametrize('lookup', PropertyRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyRangeFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyRangeFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyRangeFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'range'


@pytest.fixture
def fixture_property_number_filter():
    RangeFilterModel.objects.create(id=-1, number=-1)
    RangeFilterModel.objects.create(id=0, number=0)
    RangeFilterModel.objects.create(id=1, number=1)
    RangeFilterModel.objects.create(id=2, number=2)
    RangeFilterModel.objects.create(id=3, number=2)
    RangeFilterModel.objects.create(id=4, number=2)
    RangeFilterModel.objects.create(id=5, number=5)
    RangeFilterModel.objects.create(id=6, number=7)


TEST_LOOKUPS = [
    ('range', (-1, 7), [-1, 0, 1, 2, 3, 4, 5, 6]),
    ('range', (2, 2), [2, 3, 4]),
    ('range', (3, 2), []),
    ('range', (7, 9), [6]),
    ('range', (8, 9), []),
    ('range', (2, None), [2, 3, 4, 5, 6]),
    ('range', (None, 2), [-1, 0, 1, 2, 3, 4]),
    ('range', (None, None), [-1, 0, 1, 2, 3, 4, 5, 6]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_number_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class RangeFilterSet(FilterSet):
        number = RangeFilter(field_name='number', lookup_expr=lookup_xpr)

        class Meta:
            model = RangeFilterModel
            fields = ['number']

    filter_fs = RangeFilterSet({'number_min': lookup_val[0], 'number_max': lookup_val[1]}, queryset=RangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyRangeFilterSet(PropertyFilterSet):
        number = RangeFilter(field_name='number', lookup_expr=lookup_xpr)
        prop_number = PropertyRangeFilter(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = RangeFilterModel
            fields = ['prop_number']

    filter_fs_mixed = RangeFilterSet({'number_min': lookup_val[0], 'number_max': lookup_val[1]}, queryset=RangeFilterModel.objects.all())
    prop_filter_fs_mixed = PropertyRangeFilterSet({'prop_number_min': lookup_val[0], 'prop_number_max': lookup_val[1]}, queryset=RangeFilterModel.objects.all())
    assert set(filter_fs_mixed.qs) == set(filter_fs.qs)
    assert set(prop_filter_fs_mixed.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({'prop_number__range_min': lookup_val[0], 'prop_number__range_max': lookup_val[1]}, queryset=RangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyRangeFilter.supported_lookups)
