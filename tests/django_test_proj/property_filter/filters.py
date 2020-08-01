
import os
import sys

sys.path.append(os.path.abspath(R'..\..'))

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
    PropertyRangeFilter,
    PropertyTimeFilter,
    PropertyTimeRangeFilter,
    PropertyTypedChoiceFilter,
    PropertyTypedMultipleChoiceFilter,
    PropertyUUIDFilter,
)

from property_filter import models


def add_filter(filterset_ref, filter_class, field_name, lookup_expr, **kwargs):
    filter_name = field_name + lookup_expr
    label = F'{field_name} [{lookup_expr}]'
    filterset_ref.base_filters[filter_name] = filter_class(label=label, field_name=field_name,
                                                           lookup_expr=lookup_expr, **kwargs)

def add_supported_filters(filterset_ref, filter_class, field_name, expression_list, **kwargs):
    for lookup in expression_list:
        add_filter(filterset_ref, filter_class, field_name, lookup, **kwargs)


def add_property_filter(filterset_ref, filter_class, field_name, lookup_expr, **kwargs):
    filter_name = field_name + lookup_expr
    filterset_ref.base_filters[filter_name] = filter_class(
        field_name=field_name, lookup_expr=lookup_expr, **kwargs)


def add_supported_property_filters(filterset_ref, filter_class, field_name, expression_list, **kwargs):
    for lookup in expression_list:
        add_property_filter(filterset_ref, filter_class, field_name, lookup, **kwargs)


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


class BaseCSVFilterNumer(BaseCSVFilter, CharFilter):
    pass
class PropertyBaseCSVFilterNumer(PropertyBaseCSVFilter, PropertyCharFilter):
    pass
class PropertyBaseCSVFilterSet(PropertyFilterSet):

    class Meta:
        model = models.BaseCSVFilterModel
        exclude = ['number', 'text']
        property_fields = [
            ('prop_number', PropertyBaseCSVFilterNumer, PropertyBaseCSVFilter.supported_lookups),
            ('prop_text', PropertyBaseCSVFilterNumer, PropertyBaseCSVFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, BaseCSVFilterNumer, 'number', PropertyBaseCSVFilter.supported_lookups)
        add_supported_filters(self, BaseCSVFilterNumer, 'text', PropertyBaseCSVFilter.supported_lookups)
        super().__init__(*args, **kwargs)


class BaseInFilterNumer(BaseInFilter, CharFilter):
    pass
class PropertyBaseInFilterNumer(PropertyBaseInFilter, PropertyCharFilter):
    pass
class PropertyBaseInFilterSet(PropertyFilterSet):

    class Meta:
        model = models.BaseInFilterModel
        exclude = ['number']
        property_fields = [('prop_number', PropertyBaseInFilterNumer, PropertyBaseInFilter.supported_lookups)]

    def __init__(self, *args, **kwargs):
        add_supported_filters(self, BaseInFilterNumer, 'number', PropertyBaseInFilter.supported_lookups)
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
