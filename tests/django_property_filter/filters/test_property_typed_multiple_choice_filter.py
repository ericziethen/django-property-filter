
import pytest
from django_filters import FilterSet, TypedMultipleChoiceFilter

from django_property_filter import PropertyFilterSet, PropertyTypedMultipleChoiceFilter

from property_filter.models import TypedMultipleChoiceFilterModel


@pytest.mark.parametrize('lookup', PropertyTypedMultipleChoiceFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyTypedMultipleChoiceFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyTypedMultipleChoiceFilter(field_name='fake_field', lookup_expr='fake-lookup')


LOOKUP_CHOICES = []
@pytest.fixture
def fixture_property_typed_multiple_choice_filter():
    TypedMultipleChoiceFilterModel.objects.create(id=-1, text='1')
    TypedMultipleChoiceFilterModel.objects.create(id=0, text='One')
    TypedMultipleChoiceFilterModel.objects.create(id=1, text='2')
    TypedMultipleChoiceFilterModel.objects.create(id=2, text='2')
    TypedMultipleChoiceFilterModel.objects.create(id=3, text='Not a Number')
    TypedMultipleChoiceFilterModel.objects.create(id=4, text='3')
    TypedMultipleChoiceFilterModel.objects.create(id=5, text='3.3')
    TypedMultipleChoiceFilterModel.objects.create(id=6)

    global LOOKUP_CHOICES
    LOOKUP_CHOICES = [(c.text, c.text) for c in TypedMultipleChoiceFilterModel.objects.order_by('id')]
    LOOKUP_CHOICES.append(('666', '666'))


TEST_LOOKUPS = [
    #('exact', ['666'], 'AND', []),
    #('exact', ['666'], 'OR', []),
    #('exact', ['2'], 'AND', [1, 2]),
    ('exact', ['3'], 'OR', [4, 5]),
    #('exact', ['1', '2'], 'AND', []),
    #('exact', ['1', '2'], 'OR', [-1, 1, 2]),
    #('exact', ['1', '666'], 'AND', []),
    #'exact', ['1', '666'], 'OR', [1]),
    #('exact', ['1', 'One'], 'OR', [-1, 0, 1, 2, 3, 4, 5]),  # Invalid Input, not int
    #('exact', ['1', 'One'], 'AND', [-1, 0, 1, 2, 3, 4, 5]),  # Invalid Input, not int
    #('exact', ['1', None], 'OR', [-1, 0, 1, 2, 3, 4, 5]),  # None returns full queryset
    #('exact', ['1', None], 'AND', [-1, 0, 1, 2, 3, 4, 5]),  # None returns full queryset





    #('iexact', ['666'], 'AND', []),
    #('iexact', ['666'], 'OR', []),
    #('iexact', ['2'], 'AND', [2, 3, 4]),
    #('iexact', ['2'], 'OR', [2, 3, 4]),
    #('iexact', ['1', '2'], 'AND', []),
    #('iexact', ['1', '2'], 'OR', [1, 2, 3, 4]),
    #('iexact', ['1', '666'], 'AND', []),
    #('iexact', ['1', '666'], 'OR', [1]),
    #('contains', ['1', '2'], 'AND', []),
    #('contains', ['2'], 'AND', [2, 3, 4, 8]),
    #('contains', ['0', '2'], 'AND', [8]),
    #('contains', ['0', '2'], 'OR', [0, 2, 3, 4, 7, 8]),
    #('contains', ['1', '666'], 'AND', []),
    #('contains', ['1', '666'], 'OR', [-1, 1, 7]),
    #('contains', ['0', '1', '2', '3', '4', '10', '20'], 'OR', [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]),
    #('icontains', ['2'], 'AND', [2, 3, 4, 8]),
    #('icontains', ['1', '2'], 'AND', []),
    #('icontains', ['0', '2'], 'AND', [8]),
    #('icontains', ['0', '2'], 'OR', [0, 2, 3, 4, 7, 8]),
    #('icontains', ['1', '666'], 'AND', []),
    #('icontains', ['1', '666'], 'OR', [-1, 1, 7]),
    #('gt', ['3', '10'], 'AND', [8]),
    #('gt', ['3', '10'], 'OR', [6, 7, 8]),
    #('gte', ['3', '10'], 'AND', [7, 8]),
    #('gte', ['3', '10'], 'OR', [5, 6, 7, 8]),
    #('lt', ['3', '10'], 'AND', [-1, 0, 1, 2, 3, 4]),
    #('lt', ['3', '10'], 'OR', [-1, 0, 1, 2, 3, 4, 5, 6]),
    #('lte', ['3', '10'], 'AND', [-1, 0, 1, 2, 3, 4, 5]),
    #('lte', ['3', '10'], 'OR', [-1, 0, 1, 2, 3, 4, 5, 6, 7]),
    #('startswith', ['2'], 'AND', [2, 3, 4, 8]),
    #('startswith', ['2', '3'], 'AND', []),
    #('startswith', ['2', '3'], 'OR', [2, 3, 4, 5, 8]),
    #('istartswith', ['2'], 'AND', [2, 3, 4, 8]),
    #('istartswith', ['2', '3'], 'AND', []),
    #('istartswith', ['2', '3'], 'OR', [2, 3, 4, 5, 8]),
    #('endswith', ['0'], 'AND', [0, 7, 8]),
    #('endswith', ['0', '3'], 'AND', []),
    #('endswith', ['0', '3'], 'OR', [0, 5, 7, 8]),
    #('iendswith', ['0'], 'AND', [0, 7, 8]),
    #('iendswith', ['0', '3'], 'AND', []),
    #('iendswith', ['0', '3'], 'OR', [0, 5, 7, 8]),
]



@pytest.mark.debug



@pytest.mark.parametrize('lookup_xpr, lookup_val, and_or, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_typed_multiple_choice_filter, lookup_xpr, lookup_val, and_or, result_list):
    if and_or == 'AND':
        conjoined = True
    elif and_or == 'OR':
        conjoined = False
    else:
        assert False

    # Test using Normal Django Filter
    class TypedMultipleChoiceFilterSet(FilterSet):
        text = TypedMultipleChoiceFilter(
            field_name='text', lookup_expr=lookup_xpr, conjoined=conjoined, choices=LOOKUP_CHOICES, coerce=int)

        class Meta:
            model = TypedMultipleChoiceFilterModel
            fields = ['text']

    filter_fs = TypedMultipleChoiceFilterSet({'text': lookup_val}, queryset=TypedMultipleChoiceFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyTypedMultipleChoiceFilterSet(FilterSet):
        prop_text = PropertyTypedMultipleChoiceFilter(
            field_name='prop_text', lookup_expr=lookup_xpr, conjoined=conjoined, choices=LOOKUP_CHOICES, coerce=int)

        class Meta:
            model = TypedMultipleChoiceFilterModel
            fields = ['prop_text']

    prop_filter_fs = PropertyTypedMultipleChoiceFilterSet({'prop_text': lookup_val}, queryset=TypedMultipleChoiceFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyTypedMultipleChoiceFilterSet(PropertyFilterSet):
        prop_text = PropertyTypedMultipleChoiceFilter(
            field_name='prop_text', lookup_expr=lookup_xpr, conjoined=conjoined, choices=LOOKUP_CHOICES, coerce=int)

        class Meta:
            model = TypedMultipleChoiceFilterModel
            fields = ['prop_text']

    prop_filter_fs = PropertyTypedMultipleChoiceFilterSet({'prop_text': lookup_val}, queryset=TypedMultipleChoiceFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = TypedMultipleChoiceFilterModel
            exclude = ['text']
            property_fields = [('prop_text', PropertyTypedMultipleChoiceFilter, [lookup_xpr])]

    # Since choices are required as argument we cannot create this filter explicitly
    with pytest.raises(ValueError):
        ImplicitFilterSet({F'prop_text__{lookup_xpr}': lookup_val}, queryset=TypedMultipleChoiceFilterModel.objects.all())


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyTypedMultipleChoiceFilter.supported_lookups)
