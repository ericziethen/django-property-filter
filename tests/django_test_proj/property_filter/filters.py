
import os
import sys

sys.path.append(os.path.abspath(R'..\..'))

from django_filters import FilterSet

from django_property_filter.conf import SUPPORTED_LOOKUPS as SUPPORTED_PROPERTY_LOOKUPS
from django_property_filter.filters import (
    PropertyNumberFilter,
)

from property_filter import models


# TODO - THIS FUNCTIONALITY SHOULD BE AUTOMATICALLY IN AS PropertyFilterSet and CHECK IF GIVEN FILTERS ARE SUPPORTED
def add_property_filter(filter_list, filter_class, property_fld_name, lookup_expr):
    filter_name = property_fld_name + lookup_expr
    filter_list[filter_name] = filter_class(property_fld_name=property_fld_name, lookup_expr=lookup_expr)

def add_supported_filters(filter_list, filter_class, property_fld_name):
    supported_filters = list(set(SUPPORTED_PROPERTY_LOOKUPS) - set(filter_class._unsupported_lookups))
    for lookup in supported_filters:
        add_property_filter(filter_list, filter_class, property_fld_name, lookup)





class PropertyNumberFilterSet(FilterSet):
    prop_number = PropertyNumberFilter(property_fld_name='prop_number', lookup_expr='exact')

    class Meta:
        model = models.NumberClass
        fields = {'number': ['exact', 'endswith']}

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        add_supported_filters(self.filters, PropertyNumberFilter, 'prop_number')
