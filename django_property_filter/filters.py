"""Filters to extend Django-FIlter filters to support property filtering."""

from django_filters.filters import (
    BooleanFilter,
    CharFilter,
    DateFilter,
    DateTimeFilter,
    DurationFilter,
    NumberFilter,
    TimeFilter,
)

from django_property_filter.utils import (
    get_value_for_db_field,
    compare_by_lookup_expression
)


class PropertyBaseFilterMixin():
    """Mixin for Property Filters."""

    supported_lookups = [
        'exact', 'iexact', 'contains', 'icontains', 'gt', 'gte',
        'lt', 'lte', 'startswith', 'istartswith', 'endswith', 'iendswith',
    ]

    def __init__(self, *args, property_fld_name, **kwargs):
        """Shared Constructor for Property Filters."""
        label = kwargs.get('label')
        lookup_expr = kwargs.get('lookup_expr')

        if label is None:
            label = F'{property_fld_name} [{lookup_expr}]'
            kwargs['label'] = label

        self.property_fld_name = property_fld_name
        self.verify_lookup(lookup_expr)
        super().__init__(*args, **kwargs)

    def filter(self, *args):  # pylint: disable=invalid-name
        """Filter the queryset by property."""
        # Looks a bit Ugly, but this way we don't have to worry about arguments
        # being added to the signature at the end, in the front will break
        # functionality anyway
        q_set = args[0]
        value = args[1]

        # Carefull, a filter value of 0 will be Valid so can't just do 'if value:'
        if value is not None and value != '':
            wanted_ids = set()
            for obj in q_set:
                property_value = get_value_for_db_field(obj, self.property_fld_name)
                if compare_by_lookup_expression(self.lookup_expr, value, property_value):
                    wanted_ids.add(obj.pk)
            return q_set.filter(pk__in=wanted_ids)

        return q_set

    def verify_lookup(self, lookup_expr):
        """Check if lookup_expr is supported."""
        if lookup_expr not in self.supported_lookups:
            raise ValueError(F'Lookup "{lookup_expr}" not supported"')


class PropertyNumberFilter(PropertyBaseFilterMixin, NumberFilter):
    """Adding Property Support to NumberFilter."""


class PropertyBooleanFilter(PropertyBaseFilterMixin, BooleanFilter):
    """Adding Property Support to BooleanFilter."""

    supported_lookups = ['exact', 'isnull']


class PropertyCharFilter(PropertyBaseFilterMixin, CharFilter):
    """Adding Property Support to BooleanFilter."""


class PropertyDateFilter(PropertyBaseFilterMixin, DateFilter):
    """Adding Property Support to DateFilter."""

    supported_lookups = ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte']


class PropertyDateTimeFilter(PropertyBaseFilterMixin, DateTimeFilter):
    """Adding Property Support to DateTimeFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyTimeFilter(PropertyBaseFilterMixin, TimeFilter):
    """Adding Property Support to TimeFilter."""

    supported_lookups = ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte']


class PropertyDurationFilter(PropertyBaseFilterMixin, DurationFilter):
    """Adding Property Support to DurationFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']
