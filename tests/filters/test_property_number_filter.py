

import pytest
from django.test import TestCase

from django_filters.filters import NumberFilter

from django_property_filter.conf import SUPPORTED_LOOKUPS
from django_property_filter.filters import PropertyNumberFilter

from tests.models import NumberClass, Delivery

@pytest.fixture
def fixture_property_number_filter():
    NumberClass.objects.create(id=1, number=1)
    NumberClass.objects.create(id=2, number=2)
    NumberClass.objects.create(id=3, number=2)
    NumberClass.objects.create(id=4, number=2)
    NumberClass.objects.create(id=5, number=3)
    NumberClass.objects.create(id=6, number=4)
    NumberClass.objects.create(id=7, number=4)
    NumberClass.objects.create(id=8, number=5)
    NumberClass.objects.create(id=9, number=5)
    NumberClass.objects.create(id=10, number=5)
    NumberClass.objects.create(id=11, number=5)
    NumberClass.objects.create(id=12, number=10)
    NumberClass.objects.create(id=13, number=20)

TEST_LOOKUPS = [
    ('exact', 15, []),
    ('exact', 5, [8, 9, 10, 11]),
    ('iexact', 15, []),
    ('iexact', 5, [8, 9, 10, 11]),
    ('contains', 100, []),
    ('contains', 4, [6, 7]),
    ('icontains', 100, []),
    ('icontains', 4, [6, 7]),
    ('gt', 20, []),
    ('gt', 4, [8, 9, 10, 11, 12, 13]),
    ('gte', 4, [6, 7, 8, 9, 10, 11, 12, 13]),
    ('gte', 21, []),
    ('lt', 1, []),
    ('lt', 4, [1, 2, 3, 4, 5]),
    ('lte', 0.9, []),
    ('lte', 4, [1, 2, 3, 4, 5, 6, 7]),
    ('startswith', 7, []),
    ('startswith', 2, [2, 3, 4, 13]),
    ('startswith', 3, [5]),
    ('istartswith', 7, []),
    ('istartswith', 3, [5]),
    ('endswith', 7, []),
    ('endswith', 0, [12, 13]),
    ('endswith', 3, [5]),
    ('iendswith', 7, []),
    ('iendswith', 3, [5]),
    #('range', , []),
    #('range', , []),
    #('isnull', , []),
    #('isnull', , []),
    #('in', , []),
    #('in', , []),
]


from django_filters import FilterSet
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_number_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class NumberFilterSet(FilterSet):
        number = NumberFilter(field_name='number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumberClass
            fields = ['number']

    filter_fs = NumberFilterSet({'number': lookup_val}, queryset=NumberClass.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Property Filter
    class PropertyNumberFilterSet(FilterSet):
        prop_number = PropertyNumberFilter(property_fld_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumberClass
            fields = ['prop_number']

    prop_filter_fs = PropertyNumberFilterSet({'prop_number': lookup_val}, queryset=NumberClass.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    #assert set(tested_expressions) == set(SUPPORTED_LOOKUPS)
