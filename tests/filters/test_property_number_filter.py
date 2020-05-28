

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
    ('exact', 5, [8, 9, 10, 11]),
    #('iexact', 5, [8, 9, 10, 11]),
    #('contains', 4, [6, 7]),
    #('icontains', 4, [6, 7]),
    #('in', , []),
    #('gt', , []),
    #('gte', , []),
    #('lt', , []),
    #'lte', , []),
    #'startswith', , []),
    #('istartswith', , []),
    #('endswith', , []),
    #('iendswith', , []),
    #('range', , []),
    #('isnull', , []),
]


from django_filters import FilterSet
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_number_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class NumberFilterSet(FilterSet):
        field = NumberFilter(field_name='number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumberClass
            # Including field directly doesn't work so workaround by excluding id
            exclude = ('id')

    filter_fs = NumberFilterSet({'number': lookup_val}, queryset=NumberClass.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Property Filter
    class PropertyNumberFilterSet(FilterSet):
        field = PropertyNumberFilter(property_fld_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumberClass
            # Including field directly doesn't work so workaround by excluding id
            exclude = ('id')

    prop_filter_fs = PropertyNumberFilterSet({'prop_number': lookup_val}, queryset=NumberClass.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    #assert set(tested_expressions) == set(SUPPORTED_LOOKUPS)
