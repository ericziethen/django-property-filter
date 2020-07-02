
import pytest

from django_filters import FilterSet, BooleanFilter

from django_property_filter import PropertyFilterSet, PropertyBooleanFilter

from property_filter.models import BooleanFilterModel


@pytest.mark.parametrize('lookup', PropertyBooleanFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyBooleanFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyBooleanFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_boolean_filter():
    BooleanFilterModel.objects.create(id=-1, is_true=True)
    BooleanFilterModel.objects.create(id=0, is_true=False)
    BooleanFilterModel.objects.create(id=1, is_true=False)
    BooleanFilterModel.objects.create(id=2, is_true=True)
    BooleanFilterModel.objects.create(id=3, is_true=False)
    BooleanFilterModel.objects.create(id=4)
    BooleanFilterModel.objects.create(id=5)

TEST_LOOKUPS = [
    ('exact', True, [-1, 2]),
    ('exact', False, [0, 1, 3]),
    ('isnull', True, [4, 5]),
    ('isnull', False, [-1, 0, 1, 2, 3]),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_boolean_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class BooleanFilterSet(FilterSet):
        is_true = BooleanFilter(field_name='is_true', lookup_expr=lookup_xpr)

        class Meta:
            model = BooleanFilterModel
            fields = ['is_true']

    filter_fs = BooleanFilterSet({'is_true': lookup_val}, queryset=BooleanFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyBooleanFilterSet(FilterSet):
        prop_is_true = PropertyBooleanFilter(property_fld_name='prop_is_true', lookup_expr=lookup_xpr)

        class Meta:
            model = BooleanFilterModel
            fields = ['prop_is_true']

    prop_filter_fs = PropertyBooleanFilterSet({'prop_is_true': lookup_val}, queryset=BooleanFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a PropertyFilterset
    class PropertyBooleanFilterSet(PropertyFilterSet):
        prop_is_true = PropertyBooleanFilter(property_fld_name='prop_is_true', lookup_expr=lookup_xpr)

        class Meta:
            model = BooleanFilterModel
            fields = ['prop_is_true']

    prop_filter_fs = PropertyBooleanFilterSet({'prop_is_true': lookup_val}, queryset=BooleanFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = BooleanFilterModel
            exclude = ['is_true']
            property_fields = [('prop_is_true', PropertyBooleanFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_is_true__{lookup_xpr}': lookup_val}, queryset=BooleanFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyBooleanFilter.supported_lookups)
