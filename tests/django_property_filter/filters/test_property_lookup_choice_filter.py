
import pytest
from django_filters import FilterSet, LookupChoiceFilter

from django_property_filter import PropertyFilterSet, PropertyLookupChoiceFilter

from property_filter.models import LookupChoiceFilterModel


@pytest.mark.parametrize('lookup', PropertyLookupChoiceFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyLookupChoiceFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyLookupChoiceFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_no_lookup_expressions():
    test_filter = PropertyLookupChoiceFilter(field_name='fake_field')

    assert set(map(lambda x: x[0], test_filter.get_lookup_choices())) == set(PropertyLookupChoiceFilter.supported_lookups)


def test_specify_lookups():
    lookup_choices = ['exact', 'gt']
    test_filter = PropertyLookupChoiceFilter(field_name='fake_field', lookup_choices=lookup_choices)

    assert set(map(lambda x: x[0], test_filter.get_lookup_choices())) == set(lookup_choices)


def test_specify_lookups_with_invalid():
    lookup_choices = ['exact', 'invalid', 'gt']

    test_filter = PropertyLookupChoiceFilter(field_name='fake_field', lookup_choices=lookup_choices)
    with pytest.raises(ValueError):
        test_filter.get_lookup_choices()


@pytest.fixture
def fixture_property_lookup_choice_filter():
    LookupChoiceFilterModel.objects.create(id=-1, number=-1)
    LookupChoiceFilterModel.objects.create(id=0, number=0)
    LookupChoiceFilterModel.objects.create(id=1, number=1)
    LookupChoiceFilterModel.objects.create(id=2, number=2)
    LookupChoiceFilterModel.objects.create(id=3, number=2)
    LookupChoiceFilterModel.objects.create(id=4, number=2)
    LookupChoiceFilterModel.objects.create(id=5, number=3)
    LookupChoiceFilterModel.objects.create(id=6, number=4)
    LookupChoiceFilterModel.objects.create(id=7, number=4)
    LookupChoiceFilterModel.objects.create(id=8, number=5)
    LookupChoiceFilterModel.objects.create(id=9, number=5)
    LookupChoiceFilterModel.objects.create(id=10, number=5)
    LookupChoiceFilterModel.objects.create(id=11, number=5)
    LookupChoiceFilterModel.objects.create(id=12, number=10)
    LookupChoiceFilterModel.objects.create(id=13, number=20)
    LookupChoiceFilterModel.objects.create(id=14)

TEST_LOOKUPS = [
    ('exact', -1, [-1]),
    #('exact', 0, [0]),
    #('exact', None, [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),  # None returns full queryset
    #('exact', 15, []),
    #('exact', 5, [8, 9, 10, 11]),
    #('contains', 100, []),
    #('contains', 4, [6, 7]),
    #('gt', 20, []),
    #('gt', 4, [8, 9, 10, 11, 12, 13]),
    #('gte', 4, [6, 7, 8, 9, 10, 11, 12, 13]),
    #('gte', 21, []),
    #('lt', 1, [-1, 0]),
    #('lt', 4, [-1, 0, 1, 2, 3, 4, 5]),
    #('lte', 0.9, [-1, 0]),
    #('lte', 4, [-1, 0, 1, 2, 3, 4, 5, 6, 7]),
    #('startswith', 7, []),
    #('startswith', 2, [2, 3, 4, 13]),
    #('startswith', 3, [5]),
    #('endswith', 7, []),
    #('endswith', 0, [0, 12, 13]),
    #('endswith', 3, [5]),
]




@pytest.mark.debug



@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_lookup_choice_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class LookupChoiceFilterSet(FilterSet):
        number = LookupChoiceFilter(field_name='number')

        class Meta:
            model = LookupChoiceFilterModel
            fields = ['number']

    filter_fs = LookupChoiceFilterSet({'number': lookup_val, 'number_lookup': lookup_xpr}, queryset=LookupChoiceFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyLookupChoiceFilterSet(FilterSet):
        prop_number = PropertyLookupChoiceFilter(field_name='prop_number')

        class Meta:
            model = LookupChoiceFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyLookupChoiceFilterSet({'prop_number': lookup_val, 'prop_number_lookup': lookup_xpr}, queryset=LookupChoiceFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyLookupChoiceFilterSet(PropertyFilterSet):
        prop_number = PropertyLookupChoiceFilter(field_name='prop_number')

        class Meta:
            model = LookupChoiceFilterModel
            fields = ['prop_number']

    prop_filter_fs = PropertyLookupChoiceFilterSet({'prop_number': lookup_val, 'prop_number_lookup': lookup_xpr}, queryset=LookupChoiceFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = LookupChoiceFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyLookupChoiceFilter, PropertyLookupChoiceFilter.supported_lookups)]

    with pytest.raises(ValueError):
        ImplicitFilterSet({F'prop_number__{lookup_xpr}': lookup_val, 'prop_number_lookup': lookup_xpr}, queryset=LookupChoiceFilterModel.objects.all())


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyLookupChoiceFilter.supported_lookups)
