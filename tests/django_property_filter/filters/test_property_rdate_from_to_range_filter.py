




# MAKE SURE TO TEST 
# - compare datetime with date objects
# - compare datetime with datetime objects










'''
import pytest
from django_filters import FilterSet, RangeFilter

from django_property_filter import PropertyFilterSet, PropertyRangeFilter

from property_filter.models import NumberClass


@pytest.mark.parametrize('lookup', PropertyRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyRangeFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyRangeFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_number_filter():
    NumberClass.objects.create(id=-1, number=-1)
    NumberClass.objects.create(id=0, number=0)
    NumberClass.objects.create(id=1, number=1)
    NumberClass.objects.create(id=2, number=2)
    NumberClass.objects.create(id=3, number=2)
    NumberClass.objects.create(id=4, number=2)
    NumberClass.objects.create(id=5, number=5)
    NumberClass.objects.create(id=6, number=7)


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
            model = NumberClass
            fields = ['number']

    filter_fs = RangeFilterSet({'number_min': lookup_val[0], 'number_max': lookup_val[1]}, queryset=NumberClass.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyRangeFilterSet(FilterSet):
        prop_number = PropertyRangeFilter(property_fld_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumberClass
            fields = ['prop_number']

    prop_filter_fs = PropertyRangeFilterSet({'prop_number_min': lookup_val[0], 'prop_number_max': lookup_val[1]}, queryset=NumberClass.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = NumberClass
            exclude = ['number']
            property_fields = [('prop_number', PropertyRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({'prop_number__range_min': lookup_val[0], 'prop_number__range_max': lookup_val[1]}, queryset=NumberClass.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyRangeFilter.supported_lookups)
'''