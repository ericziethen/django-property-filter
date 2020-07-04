
import pytest
from django_filters import FilterSet, TypedChoiceFilter

from django_property_filter import PropertyFilterSet, PropertyTypedChoiceFilter

from property_filter.models import TypedChoiceFilterModel


@pytest.mark.parametrize('lookup', PropertyTypedChoiceFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyTypedChoiceFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyTypedChoiceFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


LOOKUP_CHOICES = []
@pytest.fixture
def fixture_property_typed_choice_filter():
    TypedChoiceFilterModel.objects.update_or_create(id=-1, text='1')
    TypedChoiceFilterModel.objects.update_or_create(id=0, text='One')
    TypedChoiceFilterModel.objects.update_or_create(id=1, text='2')
    TypedChoiceFilterModel.objects.update_or_create(id=2, text='2')
    TypedChoiceFilterModel.objects.update_or_create(id=3, text='Not a Number')
    TypedChoiceFilterModel.objects.update_or_create(id=4, text='2.3')
    TypedChoiceFilterModel.objects.update_or_create(id=5)

    global LOOKUP_CHOICES
    LOOKUP_CHOICES = [(c.text, c.text) for c in TypedChoiceFilterModel.objects.order_by('id')]
    LOOKUP_CHOICES.append(('666', '666'))


TEST_LOOKUPS = [
    ('exact', '1', [-1]),
    ('exact', '666', []),
    ('exact', 'One', [-1, 0, 1, 2, 3, 4, 5]),  # Invalid Input, not int
    ('exact', None, [-1, 0, 1, 2, 3, 4, 5]),  # None returns full queryset
    ('iexact', '1', [-1]),
    ('iexact', '666', []),
    ('contains', 'One', [-1, 0, 1, 2, 3, 4, 5]),
    ('icontains', '2', [1, 2, 4]),
    ('icontains', '666', []),
    ('gt', '1', [0, 1, 2, 3, 4]),  # Doing Text Comparison
    ('gte', '1', [-1, 0, 1, 2, 3, 4]),  # Doing Text Comparison
    ('lt', '2', [-1, 5]),  # Doing Text Comparison
    ('lte', '2', [-1, 1, 2, 5]),
    ('startswith', '666', []),
    ('startswith', '2', [1, 2, 4]),
    ('istartswith', '666', []),
    ('istartswith', '2', [1, 2, 4]),
    ('endswith', '2', [1, 2]),
    ('iendswith', '2', [1, 2]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_typed_choice_filter, lookup_xpr, lookup_val, result_list):


    # Test using Normal Django Filter
    class TypedChoiceFilterSet(FilterSet):
        text = TypedChoiceFilter(field_name='text', lookup_expr=lookup_xpr,
                                 choices=LOOKUP_CHOICES, coerce=int)

        class Meta:
            model = TypedChoiceFilterModel
            fields = ['text']

    filter_fs = TypedChoiceFilterSet({'text': lookup_val}, queryset=TypedChoiceFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyTypedChoiceFilterSet(FilterSet):
        prop_text = PropertyTypedChoiceFilter(property_fld_name='prop_text', lookup_expr=lookup_xpr,
                                              choices=LOOKUP_CHOICES, coerce=int)

        class Meta:
            model = TypedChoiceFilterModel
            fields = ['prop_text']

    prop_filter_fs = PropertyTypedChoiceFilterSet({'prop_text': lookup_val}, queryset=TypedChoiceFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyTypedChoiceFilterSet(PropertyFilterSet):
        prop_text = PropertyTypedChoiceFilter(property_fld_name='prop_text', lookup_expr=lookup_xpr,
                                              choices=LOOKUP_CHOICES, coerce=int)

        class Meta:
            model = TypedChoiceFilterModel
            fields = ['prop_text']

    prop_filter_fs = PropertyTypedChoiceFilterSet({'prop_text': lookup_val}, queryset=TypedChoiceFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = TypedChoiceFilterModel
            exclude = ['text']
            property_fields = [('prop_text', PropertyTypedChoiceFilter, [lookup_xpr])]

    # Since choices are required as argument we cannot create this filter explicitly
    with pytest.raises(ValueError):
        ImplicitFilterSet({F'prop_text__{lookup_xpr}': lookup_val}, queryset=TypedChoiceFilterModel.objects.all())


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyTypedChoiceFilter.supported_lookups)
