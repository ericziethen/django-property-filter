"""Filters to extend Django-FIlter filters to support property filtering."""

import datetime
import logging

from django_filters.filters import (
    AllValuesFilter,
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFilter,
    DateFromToRangeFilter,
    DateRangeFilter,
    DateTimeFilter,
    DateTimeFromToRangeFilter,
    DurationFilter,
    IsoDateTimeFilter,
    IsoDateTimeFromToRangeFilter,
    NumberFilter,
    RangeFilter,
    TimeFilter,
    TimeRangeFilter,
    TypedChoiceFilter,
    UUIDFilter,
)

from django_property_filter.utils import (
    get_value_for_db_field,
    compare_by_lookup_expression
)

logger = logging.getLogger(__name__)


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

    def filter(self, queryset, value):
        """Filter the queryset by property."""
        # Carefull, a filter value of 0 will be Valid so can't just do 'if value:'
        if value is not None and value != '':
            wanted_ids = set()
            for obj in queryset:
                property_value = get_value_for_db_field(obj, self.property_fld_name)
                if self._compare_lookup_with_qs_entry(self.lookup_expr, value, property_value):
                    wanted_ids.add(obj.pk)
            return queryset.filter(pk__in=wanted_ids)

        return queryset

    def verify_lookup(self, lookup_expr):
        """Check if lookup_expr is supported."""
        if lookup_expr not in self.supported_lookups:
            raise ValueError(F'Lookup "{lookup_expr}" not supported"')

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):
        """Compare the lookup value with the property value."""
        result = False
        try:
            result = compare_by_lookup_expression(self.lookup_expr, lookup_value, property_value)
        except (TypeError) as error:
            logging.info(F'Error during comparing property value "{property_value}" with'
                         F'filter value "{lookup_value}" with error: "{error}"')

        return result


class ChoiceConvertionMixin():  # pylint: disable=too-few-public-methods
    """Provide Comparison Convertion for Choice Filters."""

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):

        new_lookup_value = lookup_value
        new_property_value = property_value

        if type(lookup_value) != type(property_value):  # pylint: disable=unidiomatic-typecheck
            try:
                convert_lookup_value = type(property_value)(lookup_value)
            except (ValueError, TypeError):
                pass
            else:
                new_lookup_value = convert_lookup_value

        return super()._compare_lookup_with_qs_entry(lookup_expr, new_lookup_value, new_property_value)


class PropertyAllValuesFilter(ChoiceConvertionMixin, PropertyBaseFilterMixin, AllValuesFilter):
    """Adding Property Support to AllValuesFilter."""

    @property
    def field(self):
        """Filed Property to setup default choices."""
        queryset = self.model._default_manager.distinct()  # pylint: disable=no-member,protected-access

        value_list = []
        for obj in queryset:
            property_value = get_value_for_db_field(obj, self.property_fld_name)
            value_list.append(property_value)

        value_list = sorted(value_list, key=lambda x: (x is None, x))

        self.extra['choices'] = [(prop, str(prop)) for prop in value_list]

        # Need to Call parent's Parent since our Parent uses DB fields directly
        return super(AllValuesFilter, self).field


class PropertyBooleanFilter(PropertyBaseFilterMixin, BooleanFilter):
    """Adding Property Support to BooleanFilter."""

    supported_lookups = ['exact', 'isnull']


class PropertyCharFilter(PropertyBaseFilterMixin, CharFilter):
    """Adding Property Support to BooleanFilter."""


class PropertyChoiceFilter(ChoiceConvertionMixin, PropertyBaseFilterMixin, ChoiceFilter):
    """Adding Property Support to ChoiceFilter."""


class PropertyDateFilter(PropertyBaseFilterMixin, DateFilter):
    """Adding Property Support to DateFilter."""

    supported_lookups = ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte']


class PropertyDateFromToRangeFilter(PropertyBaseFilterMixin, DateFromToRangeFilter):
    """Adding Property Support to DateFromToRangeFilter."""

    supported_lookups = ['range']

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):
        """Convert all datetime to date and then compare."""
        # Convert the Lookup Value if needed
        new_lookup_value = lookup_value
        if lookup_value:
            start = lookup_value.start
            stop = lookup_value.stop

            if start and isinstance(start, datetime.datetime):
                start = start.date()
            if stop and isinstance(stop, datetime.datetime):
                stop = stop.date()

            new_lookup_value = slice(start, stop)

        # Convert the Property Value if needed
        new_property_value = property_value
        if new_property_value and isinstance(new_property_value, datetime.datetime):
            new_property_value = new_property_value.date()

        return super()._compare_lookup_with_qs_entry(lookup_expr, new_lookup_value, new_property_value)


class PropertyDateRangeFilter(PropertyBaseFilterMixin, DateRangeFilter):
    """Adding Property Support to DateRangeFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']






    '''
        DateRangeFilter defines
        ('today', _('Today')),
        ('yesterday', _('Yesterday')),
        ('week', _('Past 7 days')),
        ('month', _('This month')),
        ('year', _('This year')),

        Need the following new lookup_xpr to support
            - "year"
            - "month"
            - "day"

        Can Calculate
            - today
            - yesterday

        Need to convert the following to Ranges
            - week
            - month
            - year

        !!! Also might need to do convertion like PropertyDateFromToRangeFilter._compare_lookup_with_qs_entry_compare_lookup_with_qs_entry

    '''


    '''
    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):

        # Convert DateTime values to Date only
        if lookup_value and isinstance(lookup_value, datetime.datetime):
            lookup_value = lookup_value.date()
        if property_value and isinstance(property_value, datetime.datetime):
            property_value = property_value.date()

        # Convert our Custom Expression to Supported Expressions
        new_lookup_exp



        result = super()._compare_lookup_with_qs_entry(lookup_expr, lookup_value, property_value)
        print('PropertyDateRangeFilter._compare_lookup_with_qs_entry(lookup_expr, lookup_value, property_value, result)',
            lookup_value, property_value, result)
        return result
    '''





class PropertyDateTimeFilter(PropertyBaseFilterMixin, DateTimeFilter):
    """Adding Property Support to DateTimeFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyDateTimeFromToRangeFilter(PropertyBaseFilterMixin, DateTimeFromToRangeFilter):
    """Adding Property Support to DateTimeFromToRangeFilter."""

    supported_lookups = ['range']


class PropertyDurationFilter(PropertyBaseFilterMixin, DurationFilter):
    """Adding Property Support to DurationFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyIsoDateTimeFilter(PropertyBaseFilterMixin, IsoDateTimeFilter):
    """Adding Property Support to IsoDateTimeFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyIsoDateTimeFromToRangeFilter(PropertyBaseFilterMixin, IsoDateTimeFromToRangeFilter):
    """Adding Property Support to IsoDateTimeFromToRangeFilter."""

    supported_lookups = ['range']


class PropertyNumberFilter(PropertyBaseFilterMixin, NumberFilter):
    """Adding Property Support to NumberFilter."""


class PropertyRangeFilter(PropertyBaseFilterMixin, RangeFilter):
    """Adding Property Support to RangeFilter."""

    supported_lookups = ['range']


class PropertyTimeFilter(PropertyBaseFilterMixin, TimeFilter):
    """Adding Property Support to TimeFilter."""

    supported_lookups = ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte']


class PropertyTimeRangeFilter(PropertyBaseFilterMixin, TimeRangeFilter):
    """Adding Property Support to TimeRangeFilter."""

    supported_lookups = ['range']


class PropertyTypedChoiceFilter(ChoiceConvertionMixin, PropertyBaseFilterMixin, TypedChoiceFilter):
    """Adding Property Support to TypedChoiceFilter."""


class PropertyUUIDFilter(PropertyBaseFilterMixin, UUIDFilter):
    """Adding Property Support to UUIDFilter."""

    supported_lookups = ['exact']


EXPLICIST_ONLY_FILTERS = [
    PropertyChoiceFilter,
    PropertyTypedChoiceFilter,
]
