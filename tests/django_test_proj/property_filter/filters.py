
import os
import sys

sys.path.append(os.path.abspath(R'..\..'))

from django_filters import FilterSet

from django_property_filter.filters import (
    PropertyNumberFilter,
)

from property_filter import models


class PropertyNumberFilterSet(FilterSet):
    prop_number = PropertyNumberFilter(property_fld_name='prop_number', lookup_expr='exact')

    class Meta:
        model = models.NumberClass
        fields = ['number']
