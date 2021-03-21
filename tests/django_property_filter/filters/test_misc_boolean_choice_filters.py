
'''
Boolean Comparison is somewhat special as the str() method on a boolean doesn't make it
comparable because it always returns true.
'''

import pytest

from django_filters import (
    FilterSet,
    ChoiceFilter,
    MultipleChoiceFilter,
    AllValuesFilter,
    AllValuesMultipleFilter,
    TypedChoiceFilter,
    TypedMultipleChoiceFilter,
)

from django_property_filter import (
    PropertyFilterSet,
    PropertyChoiceFilter,
    PropertyMultipleChoiceFilter,
    PropertyAllValuesFilter,
    PropertyAllValuesMultipleFilter,
    PropertyTypedChoiceFilter,
    PropertyTypedMultipleChoiceFilter,
)

from property_filter.models import BooleanFilterModel


@pytest.fixture
def fixture_boolean_filter_model():
    BooleanFilterModel.objects.create(id=-1, is_true=True)
    BooleanFilterModel.objects.create(id=0, is_true=False)
    BooleanFilterModel.objects.create(id=1, is_true=False)
    BooleanFilterModel.objects.create(id=2, is_true=True)
    BooleanFilterModel.objects.create(id=3, is_true=True)


TEST_LOOKUPS = [
    ('is_true_ChoiceFilter',                'prop_is_true_PropertyChoiceFilter',                'exact', True, [-1, 2, 3]),
    ('is_true_ChoiceFilter',                'prop_is_true_PropertyChoiceFilter',                'exact', False, [0, 1]),
    ('is_true_MultipleChoiceFilter',        'prop_is_true_PropertyMultipleChoiceFilter',        'exact', [True], [-1, 2, 3]),
    ('is_true_MultipleChoiceFilter',        'prop_is_true_PropertyMultipleChoiceFilter',        'exact', [False], [0, 1]),
    ('is_true_AllValuesFilter',             'prop_is_true_PropertyAllValuesFilter',             'exact', True, [-1, 2, 3]),
    ('is_true_AllValuesFilter',             'prop_is_true_PropertyAllValuesFilter',             'exact', False, [0, 1]),
    ('is_true_AllValuesMultipleFilter',     'prop_is_true_PropertyAllValuesMultipleFilter',     'exact', [True], [-1, 2, 3]),
    ('is_true_AllValuesMultipleFilter',     'prop_is_true_PropertyAllValuesMultipleFilter',     'exact', [False], [0, 1]),
    ('is_true_TypedChoiceFilter',           'prop_is_true_PropertyTypedChoiceFilter',           'exact', True, [-1, 2, 3]),
    ('is_true_TypedChoiceFilter',           'prop_is_true_PropertyTypedChoiceFilter',           'exact', False, [0, 1]),
    ('is_true_TypedMultipleChoiceFilter',   'prop_is_true_PropertyTypedMultipleChoiceFilter',   'exact', [True], [-1, 2, 3]),
    ('is_true_TypedMultipleChoiceFilter',   'prop_is_true_PropertyTypedMultipleChoiceFilter',   'exact', [False], [0, 1]),
]
@pytest.mark.parametrize('filter_to_test, prop_filter_to_test, lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_boolean_filter_model, filter_to_test, prop_filter_to_test, lookup_xpr, lookup_val, result_list):

    LOOKUP_CHOICES = [
        (True, 'GiveMeYes'),
        (False, 'GiveMeNo'),
    ]

    # Test using Normal Django Filter
    class ChoicesFilterSet(FilterSet):
        is_true_ChoiceFilter = ChoiceFilter(field_name='is_true', lookup_expr=lookup_xpr, choices=LOOKUP_CHOICES)
        is_true_MultipleChoiceFilter = MultipleChoiceFilter(field_name='is_true', lookup_expr=lookup_xpr, conjoined=False, choices=LOOKUP_CHOICES)
        is_true_AllValuesFilter = AllValuesFilter(field_name='is_true', lookup_expr=lookup_xpr)
        is_true_AllValuesMultipleFilter = AllValuesMultipleFilter(field_name='is_true', lookup_expr=lookup_xpr, conjoined=False)
        is_true_TypedChoiceFilter = TypedChoiceFilter(field_name='is_true', lookup_expr=lookup_xpr, choices=LOOKUP_CHOICES, coerce=str)
        is_true_TypedMultipleChoiceFilter = TypedMultipleChoiceFilter(field_name='is_true', lookup_expr=lookup_xpr, conjoined=False, choices=LOOKUP_CHOICES, coerce=str)

        class Meta:
            model = BooleanFilterModel
            fields = ['is_true']

    filter_fs = ChoicesFilterSet({filter_to_test: lookup_val}, queryset=BooleanFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyChoicesFilterSet(PropertyFilterSet):
        prop_is_true_PropertyChoiceFilter = PropertyChoiceFilter(field_name='prop_is_true', lookup_expr=lookup_xpr, choices=LOOKUP_CHOICES)
        prop_is_true_PropertyMultipleChoiceFilter = PropertyMultipleChoiceFilter(field_name='prop_is_true', lookup_expr=lookup_xpr, conjoined=False, choices=LOOKUP_CHOICES)
        prop_is_true_PropertyAllValuesFilter = PropertyAllValuesFilter(field_name='prop_is_true', lookup_expr=lookup_xpr)
        prop_is_true_PropertyAllValuesMultipleFilter = PropertyAllValuesMultipleFilter(field_name='prop_is_true', lookup_expr=lookup_xpr, conjoined=False)
        prop_is_true_PropertyTypedChoiceFilter = PropertyTypedChoiceFilter(field_name='prop_is_true', lookup_expr=lookup_xpr, choices=LOOKUP_CHOICES, coerce=str)
        prop_is_true_PropertyTypedMultipleChoiceFilter = PropertyTypedMultipleChoiceFilter(field_name='prop_is_true', lookup_expr=lookup_xpr, conjoined=False, choices=LOOKUP_CHOICES, coerce=str)

        class Meta:
            model = BooleanFilterModel
            exclude = ['is_true']

    prop_filter_fs = PropertyChoicesFilterSet({prop_filter_to_test: lookup_val}, queryset=BooleanFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)







