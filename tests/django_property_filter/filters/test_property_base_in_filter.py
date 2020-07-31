

import pytest
from django_filters import FilterSet, BaseInFilter, CharFilter

from django_property_filter import PropertyFilterSet, PropertyBaseInFilter, PropertyCharFilter

from property_filter.models import BaseInFilterModel


@pytest.mark.parametrize('lookup', PropertyBaseInFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyBaseInFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyBaseInFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyBaseInFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'in'

@pytest.fixture
def fixture_property_base_csv_filter():
    BaseInFilterModel.objects.create(id=-1, number=-1.25)
    BaseInFilterModel.objects.create(id=0, number=0.0)
    BaseInFilterModel.objects.create(id=1, number=0)
    BaseInFilterModel.objects.create(id=2, number=1.0)
    BaseInFilterModel.objects.create(id=3, number=1.1)
    BaseInFilterModel.objects.create(id=4, number=3.5)
    BaseInFilterModel.objects.create(id=5, number=20.99)

TEST_LOOKUPS = [
    ('in', '', [-1, 0, 1, 2, 3, 4, 5]),
    ('in', '1.1', [3]),
    ('in', ' 1 ', [2]),
    ('in', '8', []),
    ('in', '0,1', [0, 1, 2]),
    ('in', '2,3.5,30', [4]),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_base_csv_filter, lookup_xpr, lookup_val, result_list):

    class BaseInFilterNumer(BaseInFilter, CharFilter):
        pass
    class PropertyBaseInFilterNumer(PropertyBaseInFilter, PropertyCharFilter):
        pass

    # Test using Normal Django Filter
    class BaseInFilterSet(FilterSet):
        number = BaseInFilterNumer(field_name='number', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseInFilterModel
            fields = ['number']

    filter_fs = BaseInFilterSet({'number': lookup_val}, queryset=BaseInFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyBaseInFilterSet(FilterSet):
        prop_number = PropertyBaseInFilterNumer(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseInFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyBaseInFilterSet({'prop_number': lookup_val}, queryset=BaseInFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyBaseInFilterSet(PropertyFilterSet):
        prop_number = PropertyBaseInFilterNumer(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseInFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyBaseInFilterSet({'prop_number': lookup_val}, queryset=BaseInFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = BaseInFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyBaseInFilterNumer, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_number__{lookup_xpr}': lookup_val}, queryset=BaseInFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


INVALID_VALUES_FOR_NUMBER = [
    ('in', ',', ),
    ('in', '1,', ),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val', INVALID_VALUES_FOR_NUMBER)
@pytest.mark.django_db
def test_invalid_range_for_numbers(fixture_property_base_csv_filter, lookup_xpr, lookup_val):
    class PropertyBaseInFilterNumer(PropertyBaseInFilter, PropertyCharFilter):
        pass

    class PropertyBaseInFilterSet(FilterSet):
        prop_number = PropertyBaseInFilterNumer(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseInFilterModel
            fields = ['prop_number']

    property_filter = PropertyBaseInFilterSet({'prop_number': lookup_val}, queryset=BaseInFilterModel.objects.all())
    with pytest.raises(ValueError):
        property_filter.qs


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyBaseInFilter.supported_lookups)
