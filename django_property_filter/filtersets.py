"""Filterstest for Property Filtering."""

from django.db import models

from django_filters import Filter, FilterSet

from django_property_filter.filters import EXPLICIT_ONLY_FILTERS, PropertyBaseFilter
from django_property_filter.utils import filter_qs_by_pk_list


class PropertyFilterSet(FilterSet):
    """Generic Filterset for Property Filters."""

    def __init__(self, *args, **kwargs):
        """Construct a PropertyFilterSet."""
        self._setup_property_filters()
        super().__init__(*args, **kwargs)

    def filter_queryset(self, queryset):
        """Filter the Given Queryset."""
        property_filter_list = []

        # Filter by django_filter filters first so we can control the number of sql parameters
        for name, value in self.form.cleaned_data.items():
            if isinstance(self.filters[name], PropertyBaseFilter):
                property_filter_list.append((name, value))
            else:
                queryset = self.filters[name].filter(queryset, value)
                assert isinstance(  # Assert taken from parent function #nosec
                    queryset, models.QuerySet), \
                    "Expected '%s.%s' to return a QuerySet, but got a %s instead." \
                    % (type(self).__name__, name, type(queryset).__name__)

        # Filter By Property Filters
        if property_filter_list:
            pk_list = list(queryset.model.objects.all().values_list('pk', flat=True))
            for name, value in property_filter_list:
                pk_list = self.filters[name].filter_pks(pk_list, queryset, value)

            # Generate the SQL for the property filter result
            queryset = filter_qs_by_pk_list(queryset, list(pk_list))

        return queryset

    def _add_filter(self, filter_class, field_name, lookup_expr):
        """Add a Filter."""
        filter_name = F'{field_name}__{lookup_expr}'
        self.base_filters[filter_name] = filter_class(  # pylint: disable=no-member
            field_name=field_name, lookup_expr=lookup_expr)

    def _setup_property_filters(self):
        """Set up implicit filters."""
        if 'property_fields' in self.__class__.Meta.__dict__:  # pylint: disable=no-member
            prop_fields = self.__class__.Meta.__dict__['property_fields']  # pylint: disable=no-member

            for field in prop_fields:
                prop_fld_name = field[0]
                prop_filter_class = field[1]
                lookup_xpr_list = field[2]

                # Validate the attributes
                if not issubclass(prop_filter_class, Filter):
                    raise ValueError(F'{prop_filter_class} is not a subclass of {Filter}')

                if prop_filter_class in EXPLICIT_ONLY_FILTERS:
                    raise ValueError(F'{prop_filter_class} can only be declared Explicitely')

                if not isinstance(prop_fld_name, str):
                    raise ValueError(F'Property field "{prop_fld_name}" is not a str')

                if not isinstance(lookup_xpr_list, list) or not lookup_xpr_list:
                    raise ValueError(F'Lookup list "{lookup_xpr_list}" is not a valid list of lookups')

                # Create all Filters
                for lookup in lookup_xpr_list:
                    self._add_filter(prop_filter_class, prop_fld_name, lookup)
