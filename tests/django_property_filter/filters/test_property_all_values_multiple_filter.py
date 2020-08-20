
import pytest
from django_filters import FilterSet, AllValuesMultipleFilter

from django_property_filter import PropertyFilterSet, PropertyAllValuesMultipleFilter

from property_filter.models import AllValuesMultipleFilterModel


@pytest.mark.parametrize('lookup', PropertyAllValuesMultipleFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyAllValuesMultipleFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyAllValuesMultipleFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyAllValuesMultipleFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'exact'


@pytest.fixture
def fixture_property_all_values_multiple_filter():
    AllValuesMultipleFilterModel.objects.create(id=-1, number=-1)
    AllValuesMultipleFilterModel.objects.create(id=0, number=0)
    AllValuesMultipleFilterModel.objects.create(id=1, number=1)
    AllValuesMultipleFilterModel.objects.create(id=2, number=2)
    AllValuesMultipleFilterModel.objects.create(id=3, number=2)
    AllValuesMultipleFilterModel.objects.create(id=4, number=2)
    AllValuesMultipleFilterModel.objects.create(id=5, number=3)
    AllValuesMultipleFilterModel.objects.create(id=6, number=4)
    AllValuesMultipleFilterModel.objects.create(id=7, number=10)
    AllValuesMultipleFilterModel.objects.create(id=8, number=20)
    AllValuesMultipleFilterModel.objects.create(id=9)


@pytest.mark.django_db
def test_filter_no_values_skip_filtering(fixture_property_all_values_multiple_filter):

    class PropertyAllValuesMultipleFilterSet(PropertyFilterSet):
        prop_number = PropertyAllValuesMultipleFilter(field_name='prop_number', lookup_expr='exact')

        class Meta:
            model = AllValuesMultipleFilterModel
            fields = ['prop_number']


    prop_filter_fs = PropertyAllValuesMultipleFilterSet({'prop_number': None}, queryset=AllValuesMultipleFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(AllValuesMultipleFilterModel.objects.all())


TEST_LOOKUPS = [
    ('exact', ['2'], 'AND', [2, 3, 4]),
    ('exact', ['2'], 'OR', [2, 3, 4]),
    ('exact', ['1', '2'], 'AND', []),
    ('exact', ['1', '2'], 'OR', [1, 2, 3, 4]),
    ('iexact', ['2'], 'AND', [2, 3, 4]),
    ('iexact', ['2'], 'OR', [2, 3, 4]),
    ('iexact', ['1', '2'], 'AND', []),
    ('iexact', ['1', '2'], 'OR', [1, 2, 3, 4]),
    ('contains', ['1', '2'], 'AND', []),
    ('contains', ['2'], 'AND', [2, 3, 4, 8]),
    ('contains', ['0', '2'], 'AND', [8]),
    ('contains', ['0', '2'], 'OR', [0, 2, 3, 4, 7, 8]),
    ('contains', ['0', '1', '2', '3', '4', '10', '20'], 'OR', [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]),
    ('icontains', ['2'], 'AND', [2, 3, 4, 8]),
    ('icontains', ['1', '2'], 'AND', []),
    ('icontains', ['0', '2'], 'AND', [8]),
    ('icontains', ['0', '2'], 'OR', [0, 2, 3, 4, 7, 8]),
    ('gt', ['3', '10'], 'AND', [8]),
    ('gt', ['3', '10'], 'OR', [6, 7, 8]),
    ('gte', ['3', '10'], 'AND', [7, 8]),
    ('gte', ['3', '10'], 'OR', [5, 6, 7, 8]),
    ('lt', ['3', '10'], 'AND', [-1, 0, 1, 2, 3, 4]),
    ('lt', ['3', '10'], 'OR', [-1, 0, 1, 2, 3, 4, 5, 6]),
    ('lte', ['3', '10'], 'AND', [-1, 0, 1, 2, 3, 4, 5]),
    ('lte', ['3', '10'], 'OR', [-1, 0, 1, 2, 3, 4, 5, 6, 7]),
    ('startswith', ['2'], 'AND', [2, 3, 4, 8]),
    ('startswith', ['2', '3'], 'AND', []),
    ('startswith', ['2', '3'], 'OR', [2, 3, 4, 5, 8]),
    ('istartswith', ['2'], 'AND', [2, 3, 4, 8]),
    ('istartswith', ['2', '3'], 'AND', []),
    ('istartswith', ['2', '3'], 'OR', [2, 3, 4, 5, 8]),
    ('endswith', ['0'], 'AND', [0, 7, 8]),
    ('endswith', ['0', '3'], 'AND', []),
    ('endswith', ['0', '3'], 'OR', [0, 5, 7, 8]),
    ('iendswith', ['0'], 'AND', [0, 7, 8]),
    ('iendswith', ['0', '3'], 'AND', []),
    ('iendswith', ['0', '3'], 'OR', [0, 5, 7, 8]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, and_or, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_all_values_multiple_filter, lookup_xpr, lookup_val, and_or, result_list):
    if and_or == 'AND':
        conjoined = True
    elif and_or == 'OR':
        conjoined = False
    else:
        assert False

    # Test using Normal Django Filter
    class AllValuesMultipleFilterSet(FilterSet):
        number = AllValuesMultipleFilter(field_name='number', lookup_expr=lookup_xpr, conjoined=conjoined)

        class Meta:
            model = AllValuesMultipleFilterModel
            fields = ['number']

    filter_fs = AllValuesMultipleFilterSet({'number': lookup_val}, queryset=AllValuesMultipleFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyAllValuesMultipleFilterSet(PropertyFilterSet):
        prop_number = PropertyAllValuesMultipleFilter(field_name='prop_number', lookup_expr=lookup_xpr, conjoined=conjoined)

        class Meta:
            model = AllValuesMultipleFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyAllValuesMultipleFilterSet({'prop_number': lookup_val}, queryset=AllValuesMultipleFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = AllValuesMultipleFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyAllValuesMultipleFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_number__{lookup_xpr}': lookup_val}, queryset=AllValuesMultipleFilterModel.objects.all())

    # Implicit declaration has default OR so only test that
    if not conjoined:
        assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyAllValuesMultipleFilter.supported_lookups)
