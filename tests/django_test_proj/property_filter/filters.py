
import os
import sys

sys.path.append(os.path.abspath(R'..\..'))

from django_filters.filters import (
    BooleanFilter,
    NumberFilter,
)

from django_property_filter import (
    PropertyFilterSet,
    PropertyBooleanFilter,
    PropertyNumberFilter,
)

from property_filter import models


def add_filter(filter_list, filter_class, field_name, lookup_expr):
    filter_name = field_name + lookup_expr
    label = F'{field_name} [{lookup_expr}]'
    filter_list[filter_name] = filter_class(label=label, field_name=field_name, lookup_expr=lookup_expr)

def add_supported_filters(filter_list, filter_class, field_name, expression_list):
    for lookup in expression_list:
        add_filter(filter_list, filter_class, field_name, lookup)


class PropertyNumberFilterSet(PropertyFilterSet):

    class Meta:
        model = models.NumberClass
        exclude = ['number']
        property_fields = [('prop_number', PropertyNumberFilter, PropertyNumberFilter.supported_lookups)]

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        add_supported_filters(self.filters, NumberFilter, 'number', PropertyNumberFilter.supported_lookups)


class PropertyBooleanFilterSet(PropertyFilterSet):

    class Meta:
        model = models.BooleanClass
        exclude = ['is_true']
        property_fields = [('prop_is_true', PropertyBooleanFilter, PropertyBooleanFilter.supported_lookups)]

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        add_supported_filters(self.filters, BooleanFilter, 'is_true', PropertyBooleanFilter.supported_lookups)
