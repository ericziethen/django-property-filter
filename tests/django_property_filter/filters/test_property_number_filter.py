

import pytest
from django_filters import FilterSet, NumberFilter

from django_property_filter import PropertyFilterSet, PropertyNumberFilter

from property_filter.models import NumberFilterModel


@pytest.mark.parametrize('lookup', PropertyNumberFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyNumberFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyNumberFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyNumberFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'exact'


@pytest.fixture
def fixture_property_number_filter():
    NumberFilterModel.objects.create(id=-1, number=-1)
    NumberFilterModel.objects.create(id=0, number=0)
    NumberFilterModel.objects.create(id=1, number=1)
    NumberFilterModel.objects.create(id=2, number=2)
    NumberFilterModel.objects.create(id=3, number=2)
    NumberFilterModel.objects.create(id=4, number=2)
    NumberFilterModel.objects.create(id=5, number=3)
    NumberFilterModel.objects.create(id=6, number=4)
    NumberFilterModel.objects.create(id=7, number=4)
    NumberFilterModel.objects.create(id=8, number=5)
    NumberFilterModel.objects.create(id=9, number=5)
    NumberFilterModel.objects.create(id=10, number=5)
    NumberFilterModel.objects.create(id=11, number=5)
    NumberFilterModel.objects.create(id=12, number=10)
    NumberFilterModel.objects.create(id=13, number=20)
    NumberFilterModel.objects.create(id=14)

TEST_LOOKUPS = [
    ('exact', -1, [-1]),
    ('exact', 0, [0]),
    ('exact', None, [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),  # None returns full queryset
    ('exact', 15, []),
    ('exact', 5, [8, 9, 10, 11]),
    ('contains', 100, []),
    ('contains', 4, [6, 7]),
    ('gt', 20, []),
    ('gt', 4, [8, 9, 10, 11, 12, 13]),
    ('gte', 4, [6, 7, 8, 9, 10, 11, 12, 13]),
    ('gte', 21, []),
    ('lt', 1, [-1, 0]),
    ('lt', 4, [-1, 0, 1, 2, 3, 4, 5]),
    ('lte', 0.9, [-1, 0]),
    ('lte', 4, [-1, 0, 1, 2, 3, 4, 5, 6, 7]),
    ('startswith', 7, []),
    ('startswith', 2, [2, 3, 4, 13]),
    ('startswith', 3, [5]),
    ('endswith', 7, []),
    ('endswith', 0, [0, 12, 13]),
    ('endswith', 3, [5]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_number_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class NumberFilterSet(FilterSet):
        number = NumberFilter(field_name='number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumberFilterModel
            fields = ['number']

    filter_fs = NumberFilterSet({'number': lookup_val}, queryset=NumberFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyNumberFilterSet(FilterSet):
        prop_number = PropertyNumberFilter(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumberFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyNumberFilterSet({'prop_number': lookup_val}, queryset=NumberFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyNumberFilterSet(PropertyFilterSet):
        prop_number = PropertyNumberFilter(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = NumberFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyNumberFilterSet({'prop_number': lookup_val}, queryset=NumberFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = NumberFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_number__{lookup_xpr}': lookup_val}, queryset=NumberFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyNumberFilter.supported_lookups)
