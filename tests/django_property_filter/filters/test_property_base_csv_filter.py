

import pytest
from django_filters import FilterSet, BaseCSVFilter, CharFilter

from django_property_filter import PropertyFilterSet, PropertyBaseCSVFilter, PropertyCharFilter

from property_filter.models import BaseCSVFilterModel


@pytest.mark.parametrize('lookup', PropertyBaseCSVFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyBaseCSVFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyBaseCSVFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyBaseCSVFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'in'

@pytest.fixture
def fixture_property_base_csv_filter():
    BaseCSVFilterModel.objects.create(id=-1, number=-1, text='Another')
    BaseCSVFilterModel.objects.create(id=0, number=0, text='Best')
    BaseCSVFilterModel.objects.create(id=1, number=1, text='Clear')
    BaseCSVFilterModel.objects.create(id=2, number=2, text='date')
    BaseCSVFilterModel.objects.create(id=3, number=2, text='date')
    BaseCSVFilterModel.objects.create(id=4, number=3)
    BaseCSVFilterModel.objects.create(id=5, number=4)
    BaseCSVFilterModel.objects.create(id=6, number=10)
    BaseCSVFilterModel.objects.create(id=7, number=20)
    BaseCSVFilterModel.objects.create(id=8)

TEST_LOOKUPS = [
    ('in', '', [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]),
    ('in', '2', [2, 3]),
    ('in', ' 2 ', [2, 3]),
    ('in', '8', []),
    ('in', '0,1', [0, 1]),
    ('in', '2,10,30', [2, 3, 6]),
    ('range', '', [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]),
    ('range', '50, 100', []),
    ('range', '2, 10', [2, 3, 4, 5, 6]),
    ('range', '10,2', []),
    ('range', '8,25', [6, 7]),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_base_csv_filter, lookup_xpr, lookup_val, result_list):

    class BaseCSVFilterNumber(BaseCSVFilter, CharFilter):
        pass
    class PropertyBaseCSVFilterNumber(PropertyBaseCSVFilter, PropertyCharFilter):
        pass

    # Test using Normal Django Filter
    class BaseCSVFilterSet(FilterSet):
        number = BaseCSVFilterNumber(field_name='number', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseCSVFilterModel
            fields = ['number']

    filter_fs = BaseCSVFilterSet({'number': lookup_val}, queryset=BaseCSVFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyBaseCSVFilterSet(PropertyFilterSet):
        prop_number = PropertyBaseCSVFilterNumber(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseCSVFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyBaseCSVFilterSet({'prop_number': lookup_val}, queryset=BaseCSVFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = BaseCSVFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyBaseCSVFilterNumber, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_number__{lookup_xpr}': lookup_val}, queryset=BaseCSVFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)



INVALID_VALUES_FOR_NUMBER = [
    ('in', ',', ),
    ('in', '1,', ),
    ('range', '1', ),
    ('range', '1,2,3', ),
    ('range', '1,', ),
    ('range', ',', ),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val', INVALID_VALUES_FOR_NUMBER)
@pytest.mark.django_db
def test_invalid_range_for_numbers(fixture_property_base_csv_filter, lookup_xpr, lookup_val):
    class PropertyBaseCSVFilterNumber(PropertyBaseCSVFilter, PropertyCharFilter):
        pass

    class PropertyBaseCSVFilterSet(PropertyFilterSet):
        prop_number = PropertyBaseCSVFilterNumber(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseCSVFilterModel
            fields = ['prop_number']

    property_filter = PropertyBaseCSVFilterSet({'prop_number': lookup_val}, queryset=BaseCSVFilterModel.objects.all())
    with pytest.raises(ValueError):
        property_filter.qs


VALID_VALUES_FOR_STRING = [
    ('in', ',', ),
    ('in', '1,', ),
    ('range', ',1', ),
    ('range', ',', ),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val', VALID_VALUES_FOR_STRING)
@pytest.mark.django_db
def test_valid_string_value_for_invalid_number_value(fixture_property_base_csv_filter, lookup_xpr, lookup_val):

    class PropertyBaseCSVFilterNumber(PropertyBaseCSVFilter, PropertyCharFilter):
        pass

    class PropertyBaseCSVFilterSet(PropertyFilterSet):
        prop_text = PropertyBaseCSVFilterNumber(field_name='prop_text', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseCSVFilterModel
            fields = ['prop_text']

    property_filter = PropertyBaseCSVFilterSet({'prop_text': lookup_val}, queryset=BaseCSVFilterModel.objects.all())
    # Test no Exception Raised
    property_filter.qs


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyBaseCSVFilter.supported_lookups)
