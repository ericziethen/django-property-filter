
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..', '..')))

from django_filters.widgets import CSVWidget

from django_filters.filters import (
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

from django_property_filter import (
    PropertyFilterSet,
    PropertyAllValuesFilter,
    PropertyAllValuesMultipleFilter,
    PropertyBaseCSVFilter,
    PropertyBaseInFilter,
    PropertyBaseRangeFilter,
    PropertyBooleanFilter,
    PropertyCharFilter,
    PropertyChoiceFilter,
    PropertyDateFilter,
    PropertyDateFromToRangeFilter,
    PropertyDateRangeFilter,
    PropertyDateTimeFilter,
    PropertyDateTimeFromToRangeFilter,
    PropertyDurationFilter,
    PropertyIsoDateTimeFilter,
    PropertyIsoDateTimeFromToRangeFilter,
    PropertyLookupChoiceFilter,
    PropertyMultipleChoiceFilter,
    PropertyNumberFilter,
    PropertyNumericRangeFilter,
    PropertyOrderingFilter,
    PropertyRangeFilter,
    PropertyTimeFilter,
    PropertyTimeRangeFilter,
    PropertyTypedChoiceFilter,
    PropertyTypedMultipleChoiceFilter,
    PropertyUUIDFilter,
)

from property_filter import models


def add_filter(filterset_ref, filter_class, field_name, lookup_expr, **kwargs):
    filter_name = field_name + lookup_expr + str(filter_class.__name__)
    label = F'{field_name} [{lookup_expr}] ({str(filter_class.__name__)})'
    filterset_ref.base_filters[filter_name] = filter_class(label=label, field_name=field_name,
                                                           lookup_expr=lookup_expr, **kwargs)


def add_supported_filters(filterset_ref, filter_class, field_name, expression_list, **kwargs):
    for lookup in expression_list:
        add_filter(filterset_ref, filter_class, field_name, lookup, **kwargs)


def add_supported_property_filters(filterset_ref, filter_class, field_name, expression_list, **kwargs):
    for lookup in expression_list:
        add_filter(filterset_ref, filter_class, field_name, lookup, **kwargs)


class PropertyAllValuesFilterSet(PropertyFilterSet):

    class Meta:
        model = models.AllValuesFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyAllValuesFilter, PropertyAllValuesFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, AllValuesFilter, 'number', PropertyAllValuesFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyAllValuesMultipleFilterSet(PropertyFilterSet):

    number_contains_and = AllValuesMultipleFilter(field_name='number', lookup_expr='contains', label='Number Contains <AND>', conjoined=True)
    prop_number_contains_and = PropertyAllValuesMultipleFilter(field_name='prop_number', lookup_expr='contains', label='Prop Number Contains <AND>', conjoined=True)

    class Meta:
        model = models.AllValuesMultipleFilterModel
        exclude = ['number']
        fields = ['number_contains_and', 'prop_number_contains_and']
        property_fields = [('prop_number', PropertyAllValuesMultipleFilter, PropertyAllValuesMultipleFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, AllValuesMultipleFilter, 'number', PropertyAllValuesMultipleFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class BaseCSVFilterNumber(BaseCSVFilter, CharFilter):
    pass
class PropertyBaseCSVFilterNumber(PropertyBaseCSVFilter, PropertyCharFilter):
    pass
class PropertyBaseCSVFilterSet(PropertyFilterSet):

    class Meta:
        model = models.BaseCSVFilterModel
        exclude = ['number', 'text']
        property_fields = [
            ('prop_number', PropertyBaseCSVFilterNumber, PropertyBaseCSVFilter.supported_lookups),
            ('prop_text', PropertyBaseCSVFilterNumber, PropertyBaseCSVFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, BaseCSVFilterNumber, 'number', PropertyBaseCSVFilter.supported_lookups)
        add_supported_filters(self, BaseCSVFilterNumber, 'text', PropertyBaseCSVFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class BaseInFilterNumber(BaseInFilter, CharFilter):
    pass
class PropertyBaseInFilterNumber(PropertyBaseInFilter, PropertyCharFilter):
    pass
class PropertyBaseInFilterSet(PropertyFilterSet):

    class Meta:
        model = models.BaseInFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyBaseInFilterNumber, PropertyBaseInFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, BaseInFilterNumber, 'number', PropertyBaseInFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class BaseRangeFilterDate(BaseRangeFilter, DateFilter):
    pass
class PropertyBaseRangeFilterDate(PropertyBaseRangeFilter, PropertyDateFilter):
    pass
class PropertyBaseRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.BaseRangeFilterModel
        exclude = ['date']
        property_fields = [('prop_date', PropertyBaseRangeFilterDate, PropertyBaseRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, BaseRangeFilterDate, 'date', PropertyBaseRangeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyBooleanFilterSet(PropertyFilterSet):

    class Meta:
        model = models.BooleanFilterModel
        exclude = ['is_true']
        property_fields = [('prop_is_true', PropertyBooleanFilter, PropertyBooleanFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, BooleanFilter, 'is_true', PropertyBooleanFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyCharFilterSet(PropertyFilterSet):

    class Meta:
        model = models.CharFilterModel
        exclude = ['name']
        property_fields = [('prop_name', PropertyCharFilter, PropertyCharFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, CharFilter, 'name', PropertyCharFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyChoiceFilterSet(PropertyFilterSet):

    class Meta:
        model = models.ChoiceFilterModel
        exclude = ['number']

    def __init__(self, *args, **kwargs):
        choices = [(c.number, F'Number: {c.number}') for c in models.ChoiceFilterModel.objects.order_by('id')]
        choices.append((-1, 'Number: -1'))
        choices.append((666, 'Number: 666'))
        add_supported_filters(self, ChoiceFilter, 'number', PropertyChoiceFilter.supported_lookups, choices=choices)
        add_supported_property_filters(self, PropertyChoiceFilter, 'prop_number', PropertyChoiceFilter.supported_lookups, choices=choices)
        super().__init__(*args, **kwargs)


class PropertyDateFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateFilterModel
        exclude = ['date']
        property_fields = [('prop_date', PropertyDateFilter, PropertyDateFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, DateFilter, 'date', PropertyDateFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyDateFromToRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateFromToRangeFilterModel
        exclude = ['date', 'date_time']
        property_fields = [
            ('prop_date', PropertyDateFromToRangeFilter, PropertyDateFromToRangeFilter.supported_lookups),
            ('prop_date_time', PropertyDateFromToRangeFilter, PropertyDateFromToRangeFilter.supported_lookups)
            ]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, DateFromToRangeFilter, 'date', PropertyDateFromToRangeFilter.supported_lookups)
        add_supported_filters(self, DateFromToRangeFilter, 'date_time', PropertyDateFromToRangeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyDateRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateRangeFilterModel
        exclude = ['date', 'date_time']
        property_fields = [
            ('prop_date', PropertyDateRangeFilter, PropertyDateRangeFilter.supported_lookups),
            ('prop_date_time', PropertyDateRangeFilter, PropertyDateRangeFilter.supported_lookups)
            ]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, DateRangeFilter, 'date', PropertyDateRangeFilter.supported_lookups)
        add_supported_filters(self, DateRangeFilter, 'date_time', PropertyDateRangeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyDateTimeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateTimeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyDateTimeFilter, PropertyDateTimeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, DateTimeFilter, 'date_time', PropertyDateTimeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyDateTimeFromToRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DateTimeFromToRangeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyDateTimeFromToRangeFilter, PropertyDateTimeFromToRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, DateTimeFromToRangeFilter, 'date_time', PropertyDateTimeFromToRangeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyDurationFilterSet(PropertyFilterSet):

    class Meta:
        model = models.DurationFilterModel
        exclude = ['duration']
        property_fields = [('prop_duration', PropertyDurationFilter, PropertyDurationFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, DurationFilter, 'duration', PropertyDurationFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyIsoDateTimeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.IsoDateTimeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyIsoDateTimeFilter, PropertyIsoDateTimeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, IsoDateTimeFilter, 'date_time', PropertyIsoDateTimeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyIsoDateTimeFromToRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.IsoDateTimeFromToRangeFilterModel
        exclude = ['date_time']
        property_fields = [('prop_date_time', PropertyIsoDateTimeFromToRangeFilter, PropertyIsoDateTimeFromToRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, IsoDateTimeFromToRangeFilter, 'date_time', PropertyIsoDateTimeFromToRangeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyLookupChoiceFilterSet(PropertyFilterSet):
    lookup_choices = [(lookup, lookup) for lookup in PropertyLookupChoiceFilter.supported_lookups]
    number = LookupChoiceFilter(field_name='number', lookup_choices=lookup_choices)
    prop_number = PropertyLookupChoiceFilter(field_name='prop_number', lookup_choices=lookup_choices)

    class Meta:
        model = models.LookupChoiceFilterModel
        fields = ['number', 'prop_number']


class PropertyMultipleChoiceFilterSet(PropertyFilterSet):

    number_contains_and = MultipleChoiceFilter(field_name='number', lookup_expr='contains', label='Number Contains <AND>', conjoined=True, choices=[])
    prop_number_contains_and = PropertyMultipleChoiceFilter(field_name='prop_number', lookup_expr='contains', label='Prop Number Contains <AND>', conjoined=True, choices=[])

    class Meta:
        model = models.MultipleChoiceFilterModel
        exclude = ['number']

    def __init__(self, *args, **kwargs):
        choices = [(num, F'Number: {num}') for num in models.MultipleChoiceFilterModel.objects.values_list('number', flat=True).distinct()]
        choices.append((-5, 'Number: -5'))
        choices.append((666, 'Number: 666'))

        self.base_filters['number_contains_and'].extra['choices'] = choices
        self.base_filters['prop_number_contains_and'].extra['choices'] = choices

        add_supported_filters(self, MultipleChoiceFilter, 'number', PropertyMultipleChoiceFilter.supported_lookups, choices=choices)
        add_supported_property_filters(self, PropertyMultipleChoiceFilter, 'prop_number', PropertyMultipleChoiceFilter.supported_lookups, choices=choices)
        super().__init__(*args, **kwargs)


class PropertyModelChoiceFilterSet(PropertyFilterSet):

    # No Property filter since working directly with Foreign Keys

    related = ModelChoiceFilter(queryset=models.ModelChoiceFilterRelatedModel.objects.all())

    class Meta:
        model = models.ModelChoiceFilterModel
        fields = ['related']


class PropertyModelMultipleChoiceFilterSet(PropertyFilterSet):

    # No Property filter since working directly with Foreign Keys

    related = ModelMultipleChoiceFilter(queryset=models.ModelChoiceFilterRelatedModel.objects.all())

    class Meta:
        model = models.ModelChoiceFilterModel
        fields = ['related']


class PropertyNumberFilterSet(PropertyFilterSet):

    class Meta:
        model = models.NumberFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyNumberFilter, PropertyNumberFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, NumberFilter, 'number', PropertyNumberFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyNumericRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.NumericRangeFilterModel
        exclude = ['postgres_int_range', 'postgres_decimal_range']
        property_fields = [
            ('prop_postgres_int_range', PropertyNumericRangeFilter, PropertyNumericRangeFilter.supported_lookups),
            ('prop_postgres_decimal_range', PropertyNumericRangeFilter, PropertyNumericRangeFilter.supported_lookups)
            ]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, NumericRangeFilter, 'postgres_int_range', PropertyNumericRangeFilter.supported_lookups)
        add_supported_filters(self, NumericRangeFilter, 'postgres_decimal_range', PropertyNumericRangeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyOrderingFilterSet(PropertyFilterSet):

    first_last_name = OrderingFilter(
        label='first_last_name',
        fields=(
            ('first_name', 'first_name'),
            ('last_name', 'Last Name'),
            ('username', 'username'),
            ('age', 'age')

        ),
        field_labels={
            'first_name': 'First Name',
        }
    )
    property_first_last_name = PropertyOrderingFilter(
        label='property_first_last_name',
        fields=(
            ('prop_first_name', 'prop_first_name'),
            ('prop_last_name', 'Last Name'),
            ('prop_username', 'username'),
            ('prop_age', 'age')

        ),
        field_labels={
            'prop_first_name': 'First Name',
        }
    )

    class Meta:
        model = models.OrderingFilterModel
        exclude = ['first_name', 'last_name', 'username', 'age']


class PropertyRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.RangeFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyRangeFilter, PropertyRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, RangeFilter, 'number', PropertyRangeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyTimeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.TimeFilterModel
        exclude = ['time']
        property_fields = [('prop_time', PropertyTimeFilter, PropertyTimeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, TimeFilter, 'time', PropertyTimeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyTimeRangeFilterSet(PropertyFilterSet):

    class Meta:
        model = models.TimeRangeFilterModel
        exclude = ['time']
        property_fields = [('prop_time', PropertyTimeRangeFilter, PropertyTimeRangeFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, TimeRangeFilter, 'time', PropertyTimeRangeFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class PropertyTypedChoiceFilterSet(PropertyFilterSet):

    class Meta:
        model = models.TypedChoiceFilterModel
        exclude = ['text']

    def __init__(self, *args, **kwargs):
        choices = [(c.text, F'{c.text}') for c in models.TypedChoiceFilterModel.objects.order_by('id')]
        add_supported_filters(self, TypedChoiceFilter, 'text', PropertyTypedChoiceFilter.supported_lookups, choices=choices, coerce=str)
        add_supported_property_filters(self, PropertyTypedChoiceFilter, 'prop_text', PropertyTypedChoiceFilter.supported_lookups, choices=choices, coerce=str)
        super().__init__(*args, **kwargs)


class PropertyTypedMultipleChoiceFilterSet(PropertyFilterSet):

    text_iexact_and = TypedMultipleChoiceFilter(field_name='text', lookup_expr='iexact', label='Text iexact <AND>', conjoined=True, choices=[], coerce=int)
    prop_text_iexact_and = PropertyTypedMultipleChoiceFilter(field_name='prop_text', lookup_expr='iexact', label='Prop Text iexact <AND>', conjoined=True, choices=[], coerce=int)

    class Meta:
        model = models.TypedMultipleChoiceFilterModel
        exclude = ['text']
        fields = ['text_iexact_and', 'prop_text_iexact_and']

    def __init__(self, *args, **kwargs):
        choices = [(c.text, F'{c.text}') for c in models.TypedMultipleChoiceFilterModel.objects.order_by('id')]
        choices.append(('__NOT IN LIST__', '__NOT IN LIST__'))
        choices.append(('666', '666'))

        self.base_filters['text_iexact_and'].extra['choices'] = choices
        self.base_filters['prop_text_iexact_and'].extra['choices'] = choices

        add_supported_filters(self, TypedMultipleChoiceFilter, 'text', PropertyTypedMultipleChoiceFilter.supported_lookups, choices=choices, coerce=int)
        add_supported_property_filters(self, PropertyTypedMultipleChoiceFilter, 'prop_text', PropertyTypedMultipleChoiceFilter.supported_lookups, choices=choices, coerce=int)

        super().__init__(*args, **kwargs)


class PropertyUUIDFilterSet(PropertyFilterSet):

    class Meta:
        model = models.UUIDFilterModel
        exclude = ['uuid']
        property_fields = [('prop_uuid', PropertyUUIDFilter, PropertyUUIDFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, UUIDFilter, 'uuid', PropertyUUIDFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class VolumeTestFilterSet(PropertyFilterSet):

    class Meta:
        model = models.VolumeTestModel
        exclude = ['id', 'date', 'is_true', 'number', 'text']
        property_fields = [
            ('prop_is_true', PropertyBooleanFilter, ['exact']),
            ('prop_number', PropertyNumberFilter, ['exact', 'lt', 'gt']),
            ]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, BooleanFilter, 'is_true', ['exact'])
        add_supported_filters(self, NumberFilter, 'number', ['exact', 'lt', 'gt'])
        super().__init__(*args, **kwargs)


class MultiFilterTestFilterSet(PropertyFilterSet):
    number_order = OrderingFilter(fields=('number', 'number'))
    prop_number_order = PropertyOrderingFilter(fields=('prop_number', 'prop_number'))

    class Meta:
        model = models.MultiFilterTestModel
        fields = ['number', 'text', 'is_true', 'date', 'date_time']
        property_fields = [
            ('prop_number', PropertyNumberFilter, ['exact',]),
            ('prop_text', PropertyCharFilter, ['exact']),
            ('prop_is_true', PropertyBooleanFilter, ['exact']),
            ('prop_date', PropertyDateFilter, ['exact']),
            ('prop_date_time', PropertyDateTimeFilter, ['exact']),
            ]


class MiscBooleanChoiceFiltersFilterSet(PropertyFilterSet):
    LOOKUP_CHOICES = [
        (True, 'Yes'),
        # (True, 'True'),
        # (True, 'GiveMeYes'),
        (False, 'No'),
        # (False, 'False'),
        # (False, 'GiveMeNo'),
    ]

    is_true_ChoiceFilter = ChoiceFilter(field_name='is_true', lookup_expr='exact', choices=LOOKUP_CHOICES)
    is_true_MultipleChoiceFilter = MultipleChoiceFilter(field_name='is_true', lookup_expr='exact', conjoined=False, choices=LOOKUP_CHOICES)
    is_true_AllValuesFilter = AllValuesFilter(field_name='is_true', lookup_expr='exact')
    is_true_AllValuesMultipleFilter = AllValuesMultipleFilter(field_name='is_true', lookup_expr='exact', conjoined=False)
    # Typed Choice Filter might not have a blank option, skip
    #is_true_TypedChoiceFilter = TypedChoiceFilter(field_name='is_true', lookup_expr='exact', choices=LOOKUP_CHOICES, coerce=str)
    is_true_TypedMultipleChoiceFilter = TypedMultipleChoiceFilter(field_name='is_true', lookup_expr='exact', conjoined=False, choices=LOOKUP_CHOICES, coerce=str)

    prop_is_true_PropertyChoiceFilter = PropertyChoiceFilter(field_name='prop_is_true', lookup_expr='exact', choices=LOOKUP_CHOICES)
    prop_is_true_PropertyMultipleChoiceFilter = PropertyMultipleChoiceFilter(field_name='prop_is_true', lookup_expr='exact', conjoined=False, choices=LOOKUP_CHOICES)
    prop_is_true_PropertyAllValuesFilter = PropertyAllValuesFilter(field_name='prop_is_true', lookup_expr='exact')
    prop_is_true_PropertyAllValuesMultipleFilter = PropertyAllValuesMultipleFilter(field_name='prop_is_true', lookup_expr='exact', conjoined=False)
    # Typed Choice Filter might not have a blank option, skip
    #prop_is_true_PropertyTypedChoiceFilter = PropertyTypedChoiceFilter(field_name='prop_is_true', lookup_expr='exact', choices=LOOKUP_CHOICES, coerce=str)
    prop_is_true_PropertyTypedMultipleChoiceFilter = PropertyTypedMultipleChoiceFilter(field_name='prop_is_true', lookup_expr='exact', conjoined=False, choices=LOOKUP_CHOICES, coerce=str)

    class Meta:
        model = models.BooleanFilterModel
        exclude = ['is_true']
