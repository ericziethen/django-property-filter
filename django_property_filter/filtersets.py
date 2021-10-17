"""Filterstest for Property Filtering."""

import logging

from django.db import models

from django_filters import Filter, FilterSet

from django_property_filter.constants import EMPTY_VALUES
from django_property_filter.filters import EXPLICIT_ONLY_FILTERS, PRESERVE_ORDER_FILTERS, PropertyBaseFilter
from django_property_filter.utils import filter_qs_by_pk_list

logger = logging.getLogger(__name__)


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
                logger.debug(F'Filtering value "{value}" with Filter: "{self.filters[name].__class__.__name__}", '
                             F'DATA: "{self.filters[name].__dict__}"')
                queryset = self.filters[name].filter(queryset, value)
                assert isinstance(  # Assert taken from parent function #nosec
                    queryset, models.QuerySet), \
                    F'''Expected '{type(self).__name__}.{name}' to return a QuerySet,''' +\
                    F''' but got a {type(queryset).__name__} instead.'''

        # Filter By Property Filters
        if property_filter_list:
            qs_pk_list = queryset.values_list('pk', flat=True)
            pk_list = set(qs_pk_list)

            # Check if we need to preserve the order from the normal Filter filtering
            preserve_order = None
            if queryset.ordered:
                preserve_order = list(qs_pk_list)

            logger.debug(F'pk_list after normal Filter Filtering {pk_list}')

            for name, value in property_filter_list:
                if value not in EMPTY_VALUES:
                    logger.debug(F'Filtering pk_list against value "{value}" with Property Filter: '
                                 F'"{self.filters[name].__class__.__name__}", DATA: "{self.filters[name].__dict__}"')
                    pk_list = self.filters[name].filter_pks(pk_list, queryset, value)
                    logger.debug(F'>>> Resulting pk_list {pk_list}')

                    # If we need to preserve order keep track of the latest order list
                    if self.filters[name].__class__ in PRESERVE_ORDER_FILTERS:
                        preserve_order = pk_list.copy()

            logger.debug('Filtering Property Filter queryset')
            queryset = filter_qs_by_pk_list(queryset, pk_list, preserve_order=preserve_order)

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
