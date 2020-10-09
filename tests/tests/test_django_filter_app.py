
"""

These tests try to help identify if the django-filter app changed it's Filterclasses
that might impact us.

It might only detect if new functions are overwritten and not changes to function signatures,
but better than nothing.

"""

import pytest

from django_filters import (
    AllValuesFilter,
    AllValuesMultipleFilter,
    BaseCSVFilter,
    BaseInFilter,
    BaseRangeFilter,
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFilter,
    DateFromToRangeFilter,
    DateRangeFilter,
    DateTimeFilter,
    DateTimeFromToRangeFilter,
    DurationFilter,
    Filter,
    IsoDateTimeFilter,
    IsoDateTimeFromToRangeFilter,
    LookupChoiceFilter,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
    MultipleChoiceFilter,
    NumberFilter,
    NumericRangeFilter,
    OrderingFilter,
    RangeFilter,
    TimeFilter,
    TimeRangeFilter,
    TypedChoiceFilter,
    TypedMultipleChoiceFilter,
    UUIDFilter,
)

from django_filters.filters import QuerySetRequestMixin

from tests.common import class_functions_diff_dic


DJANGO_FILTER_NO_OVERWRITTEN_FUNCTIONS = [
    (BooleanFilter, Filter),
    (CharFilter, Filter),
    (DateFilter, Filter),
    (DurationFilter, Filter),
    (NumberFilter, Filter),
    (TimeFilter, Filter),
    (UUIDFilter, Filter),
    (DateTimeFilter, Filter),
    (IsoDateTimeFilter, DateTimeFilter),
    (DateFromToRangeFilter, RangeFilter),
    (DateTimeFromToRangeFilter, RangeFilter),
    (IsoDateTimeFromToRangeFilter, RangeFilter),
    (TimeRangeFilter, RangeFilter),
    (TypedChoiceFilter, Filter),
    (AllValuesFilter, ChoiceFilter),
    (AllValuesMultipleFilter, MultipleChoiceFilter),
    (TypedMultipleChoiceFilter, MultipleChoiceFilter),
]
@pytest.mark.parametrize('filter_class, compare_class', DJANGO_FILTER_NO_OVERWRITTEN_FUNCTIONS)
def test_django_filter_no_overwritten_functions(filter_class, compare_class):
    assert class_functions_diff_dic(filter_class, compare_class, ignore=['field_class', 'get_max_validator']) == {}


DJANGO_FILTER_OVERWRITTEN_FUNCTIONS = [
    (NumericRangeFilter, Filter, ['filter']),
    (RangeFilter, Filter, ['filter']),
    (ChoiceFilter, Filter, ['__init__', 'filter']),
    (DateRangeFilter, ChoiceFilter, ['__init__', 'filter']),
    (MultipleChoiceFilter, Filter, ['__init__', 'is_noop', 'filter' ,'get_filter_predicate']),
    (LookupChoiceFilter, Filter, ['outer_class', '__init__', 'normalize_lookup', 'get_lookup_choices', 'filter']),
    (BaseCSVFilter, Filter, ['base_field_class', '__init__', '_field_class_name', '_field_class_name']),
    (BaseInFilter, BaseCSVFilter, ['__init__', '_field_class_name']),
    (BaseRangeFilter, BaseCSVFilter, ['_field_class_name', 'base_field_class', '__init__']),
]
@pytest.mark.parametrize('filter_class, compare_class, ignore_list', DJANGO_FILTER_OVERWRITTEN_FUNCTIONS)
def test_django_filter_overwritten_functions(filter_class, compare_class, ignore_list):
    assert class_functions_diff_dic(filter_class, compare_class, ignore=ignore_list + ['field_class']) == {}


DJANGO_FILTER_MULTI_INHERITANCE_CLASSES = [
    (ModelChoiceFilter, QuerySetRequestMixin, ['__init__', 'get_request', 'get_queryset'] + ['filter', 'get_method']),
    (ModelChoiceFilter, ChoiceFilter, ['__init__', 'filter'] + ['get_queryset', 'get_request']),
    (ModelMultipleChoiceFilter, QuerySetRequestMixin, ['__init__', 'get_request', 'get_queryset'] +
        ['filter', 'get_filter_predicate', 'get_method', 'is_noop']),
    (ModelMultipleChoiceFilter, ChoiceFilter, ['__init__', 'filter'] +
        ['get_filter_predicate', 'get_queryset', 'get_request', 'is_noop']),
    (OrderingFilter, BaseCSVFilter, ['__init__', 'filter', '_field_class_name'] +
        ['build_choices', 'get_ordering_value', 'normalize_fields']),
    (OrderingFilter, ChoiceFilter, ['__init__', 'filter'] +
        ['_field_class_name', 'base_field_class', 'build_choices', 'get_ordering_value', 'normalize_fields']),
]
@pytest.mark.parametrize('filter_class, compare_class, ignore_list', DJANGO_FILTER_MULTI_INHERITANCE_CLASSES)
def test_django_filter_multi_inheritance_classes(filter_class, compare_class, ignore_list):
    assert class_functions_diff_dic(filter_class, compare_class, ignore=ignore_list + ['field_class']) == {}
