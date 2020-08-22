"""Filters to extend Django-Filter filters to support property filtering."""

import datetime
import logging

from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone

from django_filters.filters import (
    Filter,
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
    IsoDateTimeFilter,
    IsoDateTimeFromToRangeFilter,
    LookupChoiceFilter,
    MultipleChoiceFilter,
    NumberFilter,
    OrderingFilter,
    RangeFilter,
    TimeFilter,
    TimeRangeFilter,
    TypedChoiceFilter,
    TypedMultipleChoiceFilter,
    UUIDFilter,
)

from django_property_filter.utils import (
    compare_by_lookup_expression,
    get_value_for_db_field,
    sort_queryset
)

logger = logging.getLogger(__name__)


class PropertyBaseFilter(Filter):
    """Property Base Filter."""

    supported_lookups = [
        'exact', 'iexact', 'contains', 'icontains', 'gt', 'gte',
        'lt', 'lte', 'startswith', 'istartswith', 'endswith', 'iendswith',
    ]

    def __init__(self, *args, **kwargs):
        """Shared Constructor for Property Filters."""
        label = kwargs.get('label')
        lookup_expr = kwargs.get('lookup_expr')

        # Use a different field name for properties to avoid conflicts with property_filter implementation
        self.property_fld_name = kwargs.get('field_name')
        kwargs['field_name'] = None

        # Set the default lookup if none is specified
        if lookup_expr is None:
            lookup_expr = self.supported_lookups[0]
            kwargs['lookup_expr'] = lookup_expr

        # Set the Label
        if label is None:
            label = F'{self.property_fld_name} [{lookup_expr}]'
            kwargs['label'] = label

        super().__init__(*args, **kwargs)

        # Verify lookup after initializing since django-filter can set it as well
        self.verify_lookup(lookup_expr)

    def filter(self, qs, value):
        """Filter the queryset, stub to raise exception for misuse."""
        # Filtering is done via filter_pks() via PropertyFilterset, raise Exception if wrongly configured
        raise ImproperlyConfigured('Invalid call to filter(), make sure to use PropertyFilterSet instead of Filterset')

    def filter_pks(self, initial_pk_list, queryset, value):
        """
        Filter the Given Queryset against the given value and return a list of matching Primary Keys.

        if initial_pk_list is not None only those Primary Keys will be considered
        """
        # If no Value given we don't need to filter at all
        if not value and value != 0:
            return initial_pk_list

        # Not None but empty List, Nothing to do, No chance for a find
        if initial_pk_list is not None and not initial_pk_list:
            return []

        # Filter all values from queryset, get the pk list
        wanted_pks = set()
        for obj in queryset:
            property_value = get_value_for_db_field(obj, self.property_fld_name)
            if self._compare_lookup_with_qs_entry(self.lookup_expr, value, property_value):
                wanted_pks.add(obj.pk)

        # Find Entries in both lists if original provided
        if initial_pk_list is not None:  # We have initial pk list, only return joined results
            wanted_pks = wanted_pks & set(initial_pk_list)

        return list(wanted_pks)

    def verify_lookup(self, lookup_expr):
        """Check if lookup_expr is supported."""
        if lookup_expr not in self.supported_lookups:
            raise ValueError(F'Lookup "{lookup_expr}" not supported"')

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):  # pylint: disable=no-self-use
        """Compare the lookup value with the property value."""
        result = False

        # Convert any of the Lookups, e.g. for Range with only 1 value
        lookup_expr, lookup_value, property_value = self._lookup_convertion(
            lookup_expr, lookup_value, property_value)

        try:
            result = compare_by_lookup_expression(lookup_expr, lookup_value, property_value)
        except (TypeError) as error:
            logging.info(F'Error during comparing property value "{property_value}" with'
                         F'filter value "{lookup_value}" with error: "{error}"')

        return result

    def _lookup_convertion(self, lookup_expr, lookup_value, property_value):  # pylint: disable=no-self-use
        return lookup_expr, lookup_value, property_value


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


class PropertyBaseCSVFilter(PropertyBaseFilter, BaseCSVFilter):
    """Adding Property Support to BaseCSVFilter."""

    supported_lookups = ['in', 'range']

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):

        # Converting the types everytime might be a bit inefficient but we don't know for
        # sure what type the property value is unlike with db fields
        if lookup_expr == 'range' and len(lookup_value) != 2:
            raise ValueError(F'2 values needed for range lookup but got {len(lookup_value)} - {lookup_value}')

        converted_values = []

        for entry in lookup_value:
            converted_field = entry

            # django-filter falls back to None if ranges are missing string values otherwise an exception is raised
            if not entry and not isinstance(property_value, str):
                raise ValueError(F'Empty value not allowed for type "{type(property_value)}"')

            if type(entry) != type(property_value):  # pylint: disable=unidiomatic-typecheck
                try:
                    convert_lookup_value = type(property_value)(entry)
                except (ValueError, TypeError):
                    # Use original if can't convert
                    pass
                else:
                    converted_field = convert_lookup_value
            converted_values.append(converted_field)

        if lookup_expr == 'in':
            new_lookup_value = converted_values
        elif lookup_expr == 'range':
            new_lookup_value = slice(converted_values[0], converted_values[1], None)

        return super()._compare_lookup_with_qs_entry(lookup_expr, new_lookup_value, property_value)


class PropertyBooleanFilter(PropertyBaseFilter, BooleanFilter):
    """Adding Property Support to BooleanFilter."""

    supported_lookups = ['exact', 'isnull']


class PropertyCharFilter(PropertyBaseFilter, CharFilter):
    """Adding Property Support to BooleanFilter."""


class PropertyChoiceFilter(ChoiceConvertionMixin, PropertyBaseFilter, ChoiceFilter):
    """Adding Property Support to ChoiceFilter."""


class PropertyDateFilter(PropertyBaseFilter, DateFilter):
    """Adding Property Support to DateFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyDateTimeFilter(PropertyBaseFilter, DateTimeFilter):
    """Adding Property Support to DateTimeFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyDurationFilter(PropertyBaseFilter, DurationFilter):
    """Adding Property Support to DurationFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyLookupChoiceFilter(ChoiceConvertionMixin, PropertyBaseFilter, LookupChoiceFilter):
    """Adding Property Support to LookupChoiceFilter."""

    def get_lookup_choices(self):
        """Get th Lookup choices in the correct format."""
        lookups = self.lookup_choices
        if lookups is None:
            lookups = self.supported_lookups

        lookup_tup_list = [self.normalize_lookup(lookup) for lookup in lookups]

        for lookup_expr, _ in lookup_tup_list:
            self.verify_lookup(lookup_expr)

        return lookup_tup_list

    def filter_pks(self, initial_pk_list, queryset, value):
        """Perform the custom filtering."""
        if not value:
            return super().filter_pks(initial_pk_list, queryset, None)

        self.lookup_expr = value.lookup_expr
        return super().filter_pks(initial_pk_list, queryset, value.value)


class PropertyMultipleChoiceFilter(ChoiceConvertionMixin, PropertyBaseFilter, MultipleChoiceFilter):
    """Adding Property Support to MultipleChoiceFilter."""

    def filter_pks(self, initial_pk_list, queryset, value):
        """Filter Multiple Choice Property Values."""
        # If no Value given we don't need to filter at all
        if not value:
            return initial_pk_list

        # Not None but empty List, Nothing to do, No chance for a find
        if not queryset:
            return []

        result_pks = None
        for sub_value in value:
            filter_result = set(super().filter_pks(None, queryset, sub_value))
            if self.conjoined:  # AND
                if result_pks is None:
                    result_pks = set(initial_pk_list)
                result_pks &= filter_result
            else:  # OR
                if result_pks is None:
                    result_pks = set()
                result_pks |= filter_result

        return list(result_pks) if result_pks is not None else []


class PropertyNumberFilter(PropertyBaseFilter, NumberFilter):
    """Adding Property Support to NumberFilter."""

    supported_lookups = [
        'exact', 'contains', 'gt', 'gte', 'lt', 'lte', 'startswith', 'endswith']


class PropertyRangeFilter(PropertyBaseFilter, RangeFilter):
    """Adding Property Support to RangeFilter."""

    supported_lookups = ['range']

    def _lookup_convertion(self, lookup_expr, lookup_value, property_value):  # pylint: disable=no-self-use

        if lookup_expr == 'range':
            if lookup_value.start is None:
                lookup_expr = 'lte'
                lookup_value = lookup_value.stop
            elif lookup_value.stop is None:
                lookup_expr = 'gte'
                lookup_value = lookup_value.start

        return lookup_expr, lookup_value, property_value


class PropertyTimeFilter(PropertyBaseFilter, TimeFilter):
    """Adding Property Support to TimeFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyTypedChoiceFilter(PropertyBaseFilter, TypedChoiceFilter):
    """Adding Property Support to TypedChoiceFilter."""


class PropertyUUIDFilter(PropertyBaseFilter, UUIDFilter):
    """Adding Property Support to UUIDFilter."""

    supported_lookups = ['exact']


# Filter Inheriting from other Property Filters #


class PropertyBaseInFilter(PropertyBaseCSVFilter, BaseInFilter):
    """Adding Property Support to BaseInFilter."""

    supported_lookups = ['in']


class PropertyBaseRangeFilter(PropertyBaseCSVFilter, BaseRangeFilter):
    """Adding Property Support to BaseRangeFilter."""

    supported_lookups = ['range']


class PropertyAllValuesFilter(PropertyChoiceFilter, AllValuesFilter):
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


class PropertyAllValuesMultipleFilter(PropertyMultipleChoiceFilter, AllValuesMultipleFilter):
    """Adding Property Support to AllValuesFilter."""

    @property
    def field(self):
        """Filed Property to setup default choices."""
        queryset = self.model._default_manager.distinct()  # pylint: disable=no-member,protected-access

        value_list = []
        for obj in queryset:
            property_value = get_value_for_db_field(obj, self.property_fld_name)
            value_list.append(property_value)

        value_list = sorted(set(value_list), key=lambda x: (x is None, x))

        self.extra['choices'] = [(prop, str(prop)) for prop in value_list]

        # Need to Call parent's Parent since our Parent uses DB fields directly
        return super(AllValuesMultipleFilter, self).field


class PropertyDateFromToRangeFilter(PropertyRangeFilter, DateFromToRangeFilter):
    """Adding Property Support to DateFromToRangeFilter."""

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


class PropertyDateTimeFromToRangeFilter(PropertyRangeFilter, DateTimeFromToRangeFilter):
    """Adding Property Support to DateTimeFromToRangeFilter."""


class PropertyDateRangeFilter(PropertyChoiceFilter, DateRangeFilter):
    """Adding Property Support to DateRangeFilter."""

    supported_lookups = ['exact']

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):

        new_lookup_exp = lookup_expr
        new_lookup_value = lookup_value
        new_property_value = property_value

        # Convert DateTime values to Date only
        if property_value and isinstance(property_value, datetime.datetime):
            new_property_value = property_value.date()

        # Convert our Custom Expression and Value to Supported the Hardcoded Expressions
        today_datetime = timezone.now()

        if lookup_value == 'today':
            new_lookup_value = today_datetime.date()
        elif lookup_value == 'yesterday':
            new_lookup_value = today_datetime.date() - datetime.timedelta(days=1)
        elif lookup_value == 'week':
            new_lookup_exp = 'range'
            new_lookup_value = slice(
                today_datetime.date() - datetime.timedelta(days=7),
                today_datetime.date()
            )
        elif lookup_value == 'month':
            new_lookup_exp = 'exact'
            new_lookup_value = today_datetime.date().month
            new_property_value = property_value.month
        elif lookup_value == 'year':
            new_lookup_exp = 'exact'
            new_lookup_value = today_datetime.date().year
            new_property_value = property_value.year

        return super()._compare_lookup_with_qs_entry(new_lookup_exp, new_lookup_value, new_property_value)


class PropertyIsoDateTimeFilter(PropertyDateTimeFilter, IsoDateTimeFilter):
    """Adding Property Support to IsoDateTimeFilter."""


class PropertyIsoDateTimeFromToRangeFilter(PropertyRangeFilter, IsoDateTimeFromToRangeFilter):
    """Adding Property Support to IsoDateTimeFromToRangeFilter."""


class PropertyOrderingFilter(  # pylint: disable=too-many-ancestors
        PropertyBaseCSVFilter, PropertyChoiceFilter, OrderingFilter):
    """Adding Property Support to OrderingFilter."""

    supported_lookups = ['exact']

    def filter_pks(self, initial_pk_list, queryset, value):
        """Filter the PropertyOrderingFilter."""
        # If no value is set just return this queryset
        if not value:
            return initial_pk_list

        # Only sort by the first parameter
        sorted_qs = sort_queryset(self.get_ordering_value(value[0]), queryset)

        return list(sorted_qs.values_list('pk', flat=True))


class PropertyTimeRangeFilter(PropertyRangeFilter, TimeRangeFilter):
    """Adding Property Support to TimeRangeFilter."""


class PropertyTypedMultipleChoiceFilter(PropertyMultipleChoiceFilter, TypedMultipleChoiceFilter):
    """Adding Property Support to TypedMultipleChoiceFilter."""


EXPLICIT_ONLY_FILTERS = [
    PropertyChoiceFilter,
    PropertyLookupChoiceFilter,
    PropertyMultipleChoiceFilter,
    PropertyOrderingFilter,
    PropertyTypedChoiceFilter,
    PropertyTypedMultipleChoiceFilter,
]
