

import pytest
from django_filters import FilterSet, CharFilter

from django_property_filter import PropertyFilterSet, PropertyCharFilter

from property_filter.models import CharFilterModel

from tests.common import db_is_sqlite, db_is_postgresql


@pytest.mark.parametrize('lookup', PropertyCharFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyCharFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyCharFilter(field_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_char_filter():
    CharFilterModel.objects.create(id=-1, name='Aa')
    CharFilterModel.objects.create(id=0, name='BB')
    CharFilterModel.objects.create(id=1, name='bb')
    CharFilterModel.objects.create(id=2, name='C')
    CharFilterModel.objects.create(id=3, name='c')
    CharFilterModel.objects.create(id=4)

# Sqlite by default is always case insensitive
# it's case sensitive if 'case_sensitive_like' pragma setting is set
# We use the default as case insensitive
TEST_LOOKUPS = [
    ('exact', 'Aa', [-1], [-1]),
    ('exact', 'C', [2], [2]),
    ('iexact', 'bB', [0, 1], [0, 1]),
    ('contains', 'A', [-1], [-1]),
    ('icontains', 'c', [2, 3], [2, 3]),
    ('startswith', 'A', [-1], [-1]),
    ('istartswith', 'B', [0, 1], [0, 1]),
    ('endswith', 'a', [-1], [-1]),
    ('iendswith', 'b', [0, 1], [0, 1]),
    ('gt', 'Aa', [0, 1, 2, 3], [0, 1, 2, 3]),
    ('gte', 'Aa', [-1, 0, 1, 2, 3], [-1, 0, 1, 2, 3]),
    ('lt', 'Aa', [4], [4]),
    ('lte', 'Aa', [-1, 4], [-1, 4]),

    # Tests for sqlite (checking as not for postgresql in case adding more databases so not to skip)
    pytest.param(
        'contains', 'B', [0], [0, 1],
        marks=pytest.mark.skipif(db_is_postgresql(), reason='Sqlite ignoring case sensitivity')),
    pytest.param(
        'startswith', 'C', [2], [2, 3],
        marks=pytest.mark.skipif(db_is_postgresql(), reason='Sqlite ignoring case sensitivity')),
    pytest.param(
        'endswith', 'b', [1], [0, 1],
        marks=pytest.mark.skipif(db_is_postgresql(), reason='Sqlite ignoring case sensitivity')),
    pytest.param(
        'gt', 'BB', [1, 2, 3], [1, 2, 3],
        marks=pytest.mark.skipif(db_is_postgresql(), reason='Different Postgresql Behaviour')),
    pytest.param(
        'lt', 'bb', [-1, 0, 2, 4], [-1, 0, 2, 4],
        marks=pytest.mark.skipif(db_is_postgresql(), reason='Different Postgresql Behaviour')),

    # Tests for postgresql (checking as not for sqlite in case adding more databases so not to skip)
    pytest.param(
        'contains', 'B', [0], [0],
        marks=pytest.mark.skipif(db_is_sqlite(), reason='Sqlite ignoring case sensitivity')),
    pytest.param(
        'startswith', 'C', [2], [2],
        marks=pytest.mark.skipif(db_is_sqlite(), reason='Sqlite ignoring case sensitivity')),
    pytest.param(
        'endswith', 'b', [1], [1],
        marks=pytest.mark.skipif(db_is_sqlite(), reason='Sqlite ignoring case sensitivity')),
    pytest.param(
        'gt', 'BB', [1, 2, 3], [2, 3],
        marks=pytest.mark.skipif(db_is_sqlite(), reason='Postgresql string sorting different then python pure ascii sorting')),
    pytest.param(
        'lt', 'bb', [-1, 0, 2, 4], [-1, 4],
        marks=pytest.mark.skipif(db_is_sqlite(), reason='Postgresql string sorting different then python pure ascii sorting')),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, property_result_list, filter_result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_char_filter, lookup_xpr, lookup_val, property_result_list, filter_result_list):

    # Test using Normal Django Filter
    class CharFilterSet(FilterSet):
        name = CharFilter(field_name='name', lookup_expr=lookup_xpr)

        class Meta:
            model = CharFilterModel
            fields = ['name']

    filter_fs = CharFilterSet({'name': lookup_val}, queryset=CharFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(filter_result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyCharFilterSet(FilterSet):
        prop_name = PropertyCharFilter(field_name='prop_name', lookup_expr=lookup_xpr)

        class Meta:
            model = CharFilterModel
            fields = ['prop_name']

    prop_filter_fs = PropertyCharFilterSet({'prop_name': lookup_val}, queryset=CharFilterModel.objects.all())
    assert set(prop_filter_fs.qs.values_list('id', flat=True)) == set(property_result_list)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyCharFilterSet(PropertyFilterSet):
        prop_name = PropertyCharFilter(field_name='prop_name', lookup_expr=lookup_xpr)

        class Meta:
            model = CharFilterModel
            fields = ['prop_name']

    prop_filter_fs = PropertyCharFilterSet({'prop_name': lookup_val}, queryset=CharFilterModel.objects.all())
    assert set(prop_filter_fs.qs.values_list('id', flat=True)) == set(property_result_list)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = CharFilterModel
            exclude = ['name']
            property_fields = [('prop_name', PropertyCharFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_name__{lookup_xpr}': lookup_val}, queryset=CharFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(prop_filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS if isinstance(x[0], str)]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyCharFilter.supported_lookups)
