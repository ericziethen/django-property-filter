

import pytest
from django_filters import FilterSet, CharFilter

from django_property_filter import PropertyFilterSet, PropertyCharFilter

from property_filter.models import TextClass


@pytest.mark.parametrize('lookup', PropertyCharFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyCharFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyCharFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_char_filter():
    TextClass.objects.create(id=-1, name='Tom')
    TextClass.objects.create(id=0, name='tom')
    TextClass.objects.create(id=1, name='TOM')
    TextClass.objects.create(id=2, name='Tom')
    TextClass.objects.create(id=3, name='Tom')
    TextClass.objects.create(id=4, name='Tomm')
    TextClass.objects.create(id=5, name='Harry')
    TextClass.objects.create(id=6)
    TextClass.objects.create(id=7)

# Sqlite will use the same for e.g. contains and icontains. oth are either case
# sensitive or not depending on 'case_sensitive_like' pragma setting
TEST_LOOKUPS = [
    ('exact', 'No Name', [], []),
    ('exact', 'Tom', [-1, 2, 3], [-1, 2, 3]),
    ('exact', 'TOM', [1], [1]),
    ('iexact', 'Tom', [-1, 0, 1, 2, 3], [-1, 0, 1, 2, 3]),
    ('iexact', 'TOM', [-1, 0, 1, 2, 3], [-1, 0, 1, 2, 3]),
    ('contains', 'OM', [1], [-1, 0, 1, 2, 3, 4]),
    ('contains', 'o', [-1, 0, 2, 3, 4], [-1, 0, 1, 2, 3, 4]),
    ('contains', 'rR', [], [5]),
    ('icontains', 'rR', [5], [5]),
    ('icontains', 'o', [-1, 0, 1, 2, 3, 4], [-1, 0, 1, 2, 3, 4]),
    ('startswith', 'T', [-1, 1, 2, 3, 4], [-1, 0, 1, 2, 3, 4]),
    ('istartswith', 'T', [-1, 0, 1, 2, 3, 4], [-1, 0, 1, 2, 3, 4]),
    ('endswith', 'om', [-1, 0, 2, 3], [-1, 0, 1, 2, 3]),
    ('iendswith', 'om', [-1, 0, 1, 2, 3], [-1, 0, 1, 2, 3]),
    ('gt', 'Harry', [-1, 0, 1, 2, 3, 4], [-1, 0, 1, 2, 3, 4]),
    ('gte', 'Harry', [-1, 0, 1, 2, 3, 4, 5], [-1, 0, 1, 2, 3, 4, 5]),
    ('lt', 'TOM', [5, 6, 7], [5, 6, 7]),
    ('lte', 'TOM', [1, 5, 6, 7], [1, 5, 6, 7]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, property_result_list, filter_result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_char_filter, lookup_xpr, lookup_val, property_result_list, filter_result_list):

    # Test using Normal Django Filter
    class CharFilterSet(FilterSet):
        name = CharFilter(field_name='name', lookup_expr=lookup_xpr)

        class Meta:
            model = TextClass
            fields = ['name']

    filter_fs = CharFilterSet({'name': lookup_val}, queryset=TextClass.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(filter_result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyCharFilterSet(FilterSet):
        prop_name = PropertyCharFilter(property_fld_name='prop_name', lookup_expr=lookup_xpr)

        class Meta:
            model = TextClass
            fields = ['prop_name']

    prop_filter_fs = PropertyCharFilterSet({'prop_name': lookup_val}, queryset=TextClass.objects.all())
    assert set(prop_filter_fs.qs.values_list('id', flat=True)) == set(property_result_list)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = TextClass
            exclude = ['name']
            property_fields = [('prop_name', PropertyCharFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_name__{lookup_xpr}': lookup_val}, queryset=TextClass.objects.all())
    assert set(implicit_filter_fs.qs) == set(prop_filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyCharFilter.supported_lookups)
