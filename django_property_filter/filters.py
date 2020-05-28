"""Filters to extend Django-FIlter filters to support property filtering."""

from django_filters.filters import (
    NumberFilter,
)

from django_filters.utils import verbose_lookup_expr

from django_property_filter.conf import SUPPORTED_LOOKUPS
from django_property_filter.utils import (
    get_value_for_db_field,
    compare_by_lookup_expression
)


class PropertyBaseFilterMixin():
    """Mixin for Property Filters."""

    _unsupported_lookups = []

    @property
    def supported_lookups(self):
        """List supported lookups."""
        return list(set(SUPPORTED_LOOKUPS) - set(self._unsupported_lookups))

    def __init__(self, field_name=None, lookup_expr=None, *, label=None,
                 method=None, distinct=False, exclude=False, property_fld_name, **kwargs):
        """Shared Constructor for Property Filters."""
        label = F'{label} {verbose_lookup_expr(lookup_expr)}'
        self.property_fld_name = property_fld_name
        self.verify_lookup(lookup_expr)
        super().__init__(field_name=field_name, lookup_expr=lookup_expr, label=label,
                         method=method, distinct=distinct, exclude=exclude, **kwargs)

    def filter(self, qs, value):  # pylint: disable=invalid-name
        """Filter the queryset by property."""
        # Carefull, a filter value of 0 will be Valid so can't just do 'if value:'
        if value is not None and value != '':
            wanted_ids = set()
            for obj in qs:
                property_value = get_value_for_db_field(obj, self.property_fld_name)
                if property_value:
                    if compare_by_lookup_expression(self.lookup_expr, value, property_value):
                        wanted_ids.add(obj.pk)
            return qs.filter(pk__in=wanted_ids)

        return qs

    def verify_lookup(self, lookup_expr):
        """Check if lookup_expr is supported."""
        if lookup_expr not in self.supported_lookups:
            raise ValueError(F'Lookup "{lookup_expr}" not supported"')


class PropertyNumberFilter(PropertyBaseFilterMixin, NumberFilter):
    """Adding Property Support to NumberFilter."""

    _unsupported_lookups = ['range', 'isnull', 'in']
