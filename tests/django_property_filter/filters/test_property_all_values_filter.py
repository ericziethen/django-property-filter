
import pytest
from django_filters import FilterSet, AllValuesFilter

from django_property_filter import PropertyFilterSet, PropertyAllValuesFilter

from property_filter.models import AllValuesFilterModel


@pytest.mark.parametrize('lookup', PropertyAllValuesFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyAllValuesFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyAllValuesFilter(field_name='fake_field', lookup_expr='fake-lookup')


LOOKUP_CHOICES = []
@pytest.fixture
def fixture_property_choice_filter():
    AllValuesFilterModel.objects.create(id=-1, number=-1)
    AllValuesFilterModel.objects.create(id=0, number=0)
    AllValuesFilterModel.objects.create(id=1, number=1)
    AllValuesFilterModel.objects.create(id=2, number=2)
    AllValuesFilterModel.objects.create(id=3, number=2)
    AllValuesFilterModel.objects.create(id=4, number=2)
    AllValuesFilterModel.objects.create(id=5, number=3)
    AllValuesFilterModel.objects.create(id=6, number=4)
    AllValuesFilterModel.objects.create(id=7, number=10)
    AllValuesFilterModel.objects.create(id=8, number=20)
    AllValuesFilterModel.objects.create(id=9)


TEST_LOOKUPS = [
    ('exact', '-1', [-1]),
    ('exact', None, [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),  # None returns full queryset
    ('iexact', '-1', [-1]),
    ('contains', '2', [2, 3, 4, 8]),
    ('icontains', '2', [2, 3, 4, 8]),
    ('gt', '20', []),
    ('gt', '2', [5, 6, 7, 8]),
    ('gte', '20', [8]),
    ('gte', '2', [2, 3, 4, 5, 6, 7, 8]),
    ('lt', '2', [-1, 0, 1]),
    ('lt', '-1', []),
    ('lte', '2', [-1, 0, 1, 2, 3, 4]),
    ('lte', '-1', [-1]),
    ('startswith', '2', [2, 3, 4, 8]),
    ('istartswith', '2', [2, 3, 4, 8]),
    ('endswith', '0', [0, 7, 8]),
    ('endswith', '3', [5]),
    ('iendswith', '0', [0, 7, 8]),
    ('iendswith', '3', [5]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_choice_filter, lookup_xpr, lookup_val, result_list):


    # Test using Normal Django Filter
    class AllValuesFilterSet(FilterSet):
        number = AllValuesFilter(field_name='number', lookup_expr=lookup_xpr)

        class Meta:
            model = AllValuesFilterModel
            fields = ['number']

    filter_fs = AllValuesFilterSet({'number': lookup_val}, queryset=AllValuesFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyAllValuesFilterSet(FilterSet):
        prop_number = PropertyAllValuesFilter(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = AllValuesFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyAllValuesFilterSet({'prop_number': lookup_val}, queryset=AllValuesFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyAllValuesFilterSet(PropertyFilterSet):
        prop_number = PropertyAllValuesFilter(field_name='prop_number', lookup_expr=lookup_xpr)

        class Meta:
            model = AllValuesFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyAllValuesFilterSet({'prop_number': lookup_val}, queryset=AllValuesFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = AllValuesFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyAllValuesFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_number__{lookup_xpr}': lookup_val}, queryset=AllValuesFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyAllValuesFilter.supported_lookups)
