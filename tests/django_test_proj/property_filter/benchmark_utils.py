
import datetime
import sys

sys.path.insert(1, '../../')  # Find our main project

from django.utils import timezone

from django_filters import (
    FilterSet,
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
    PropertyOrderingFilter,
    PropertyRangeFilter,
    PropertyTimeFilter,
    PropertyTimeRangeFilter,
    PropertyTypedChoiceFilter,
    PropertyTypedMultipleChoiceFilter,
    PropertyUUIDFilter,
)

from property_filter.models import BenchmarkTestModel as BenchmarkModel


NUMBER_RANGE = [1, 2, 3]
TEXT_RANGE = ['One', 'Two', 'Three']
IS_TRUE_RANGE = [True, False]
DATE_RANGE = [
    datetime.date(2018, 2, 1),
    datetime.date(2018, 3, 1),
    datetime.date(2018, 4, 1),
    timezone.now().date()
]
# Unaware Times because not important for benchmarking, but easier for lookup because of str convertion
DATE_TIME_RANGE = [
    datetime.datetime(2066, 3, 2, 12),
    datetime.datetime(2070, 3, 3, 15),
    datetime.datetime(2076, 3, 4, 18)
]
NUMBER_CHOICES = [(c, F'Number: {c}') for c in NUMBER_RANGE]
DURATION_RANGE = [
    datetime.timedelta(days=15),
    datetime.timedelta(days=30),
    datetime.timedelta(days=200)
]
UUID_RANGE = [
    '40828e84-66c7-46ee-a94a-1f2087970a68',
    'df4078eb-67ca-49fe-b86d-742e0feaf3ad',
    'aaaa78eb-67ca-49fe-b86d-742e0feaf3ad'
]

class BaseCSVFilterNumber(BaseCSVFilter, CharFilter):
    pass
class PropertyBaseCSVFilterNumber(PropertyBaseCSVFilter, PropertyCharFilter):
    pass
class BaseInFilterNumber(BaseInFilter, CharFilter):
    pass
class PropertyBaseInFilterNumber(PropertyBaseInFilter, PropertyCharFilter):
    pass
class BaseRangeFilterNumber(BaseRangeFilter, NumberFilter):
    pass
class PropertyBaseRangeFilterNumber(PropertyBaseRangeFilter, PropertyNumberFilter):
    pass


class MultiFilterFilterSet(FilterSet):
    number = MultipleChoiceFilter(
        field_name='number', lookup_expr='exact', conjoined=False,  # OR
        choices=NUMBER_CHOICES)
    class Meta:
        model = BenchmarkModel
        fields = ['text', 'is_true', 'date', 'date_time', 'duration', 'uuid']


class PropertyMultiFilterFilterSet(PropertyFilterSet):
    prop_number = PropertyMultipleChoiceFilter(
        field_name='prop_number', lookup_expr='exact', conjoined=False,  # OR
        choices=NUMBER_CHOICES)

    class Meta:
        model = BenchmarkModel
        fields = ['prop_number']
        exclude = ['number', 'text', 'is_true', 'date', 'date_time', 'duration', 'uuid']
        property_fields = [
            ('prop_text', PropertyCharFilter, ['exact']),
            ('prop_is_true', PropertyBooleanFilter, ['exact']),
            ('prop_date', PropertyDateFilter, ['exact']),
            ('prop_date_time', PropertyDateTimeFilter, ['exact']),
        ]

class AllFiltersFilterSet(FilterSet):
    number_AllValuesFilter = AllValuesFilter(field_name='number', lookup_expr='exact')
    number_AllValuesMultipleFilter = AllValuesMultipleFilter(field_name='number', lookup_expr='exact', conjoined=False)  # OR
    number_BaseCSVFilterNumber = BaseCSVFilterNumber(field_name='number', lookup_expr='in')
    number_BaseInFilterNumber = BaseInFilterNumber(field_name='number', lookup_expr='in')
    number_BaseRangeFilterNumber = BaseRangeFilterNumber(field_name='number', lookup_expr='range')
    is_true_BooleanFilter = BooleanFilter(field_name='is_true', lookup_expr='exact')
    text_CharFilter_CharFilter = CharFilter(field_name='text', lookup_expr='exact')
    number_ChoiceFilter = ChoiceFilter(field_name='number', lookup_expr='exact', choices=NUMBER_CHOICES)
    date_DateFilter = DateFilter(field_name='date', lookup_expr='exact')
    date_DateFromToRangeFilter = DateFromToRangeFilter(field_name='date', lookup_expr='range')
    date_DateRangeFilter = DateRangeFilter(field_name='date', lookup_expr='exact')
    date_time_DateTimeFilter = DateTimeFilter(field_name='date_time', lookup_expr='exact')
    date_time_DateTimeFromToRangeFilter = DateTimeFromToRangeFilter(field_name='date_time', lookup_expr='range')
    duration_DurationFilter = DurationFilter(field_name='duration', lookup_expr='exact')
    date_time_IsoDateTimeFilter = IsoDateTimeFilter(field_name='date_time', lookup_expr='lt')
    date_time_IsoDateTimeFromToRangeFilter = IsoDateTimeFromToRangeFilter(field_name='date_time', lookup_expr='range')
    number_MultipleChoiceFilter = MultipleChoiceFilter(field_name='number', lookup_expr='exact', conjoined=False, choices=NUMBER_CHOICES)
    number_NumberFilter = NumberFilter(field_name='number', lookup_expr='exact')
    number_OrderingFilter = OrderingFilter(fields=('number', 'number'))
    number_RangeFilter = RangeFilter(field_name='number', lookup_expr='range')
    date_time_TimeFilter = TimeFilter(field_name='date_time', lookup_expr='exact')
    date_time_TimeRangeFilter = TimeRangeFilter(field_name='date_time', lookup_expr='range')
    number_TypedChoiceFilter = TypedChoiceFilter(field_name='number', lookup_expr='exact', choices=NUMBER_CHOICES)
    text_TypedMultipleChoiceFilter = TypedMultipleChoiceFilter(field_name='number', lookup_expr='exact', conjoined=False, choices=NUMBER_CHOICES)
    uuid_UUIDFilter = UUIDFilter(field_name='uuid', lookup_expr='exact')
    number_LookupChoiceFilter = LookupChoiceFilter(field_name='number')

    class Meta:
        model = BenchmarkModel
        exclude = ['number', 'text', 'is_true', 'date', 'date_time', 'duration']


class AllFiltersPropertyFilterSet(PropertyFilterSet):
    prop_number_AllValuesFilter = PropertyAllValuesFilter(field_name='prop_number', lookup_expr='exact')
    prop_number_PropertyAllValuesMultipleFilter = PropertyAllValuesMultipleFilter(field_name='prop_number', lookup_expr='exact', conjoined=False)  # OR
    prop_number_PropertyBaseCSVFilterNumber = PropertyBaseCSVFilterNumber(field_name='prop_number', lookup_expr='in')
    prop_number_PropertyBaseInFilterNumber = PropertyBaseInFilterNumber(field_name='prop_number', lookup_expr='in')
    prop_number_PropertyBaseRangeFilterNumber = PropertyBaseRangeFilterNumber(field_name='prop_number', lookup_expr='range')
    prop_is_true_PropertyBooleanFilter = PropertyBooleanFilter(field_name='prop_is_true', lookup_expr='exact')
    prop_text_PropertyCharFilter = PropertyCharFilter(field_name='prop_text', lookup_expr='exact')
    prop_number_PropertyChoiceFilter = PropertyChoiceFilter(field_name='prop_number', lookup_expr='exact', choices=NUMBER_CHOICES)
    prop_date_PropertyDateFilter = PropertyDateFilter(field_name='prop_date', lookup_expr='exact')
    prop_date_PropertyDateFromToRangeFilter = PropertyDateFromToRangeFilter(field_name='prop_date', lookup_expr='range')
    prop_date_PropertyDateRangeFilter = PropertyDateRangeFilter(field_name='prop_date', lookup_expr='exact')
    prop_date_time_PropertyDateTimeFilter = PropertyDateTimeFilter(field_name='prop_date_time', lookup_expr='exact')
    prop_date_time_PropertyDateTimeFromToRangeFilter = PropertyDateTimeFromToRangeFilter(field_name='prop_date_time', lookup_expr='range')
    prop_duration_PropertyDurationFilter = PropertyDurationFilter(field_name='prop_duration', lookup_expr='exact')
    prop_date_time_PropertyIsoDateTimeFilter = PropertyIsoDateTimeFilter(field_name='prop_date_time', lookup_expr='lt')
    prop_date_time_PropertyIsoDateTimeFromToRangeFilter = PropertyIsoDateTimeFromToRangeFilter(field_name='prop_date_time', lookup_expr='range')
    prop_number_PropertyMultipleChoiceFilter = PropertyMultipleChoiceFilter(field_name='prop_number', lookup_expr='exact', conjoined=False, choices=NUMBER_CHOICES)
    prop_number_PropertyNumberFilter = PropertyNumberFilter(field_name='prop_number', lookup_expr='exact')
    prop_number_PropertyOrderingFilter = PropertyOrderingFilter(fields=('prop_number', 'prop_number'))
    prop_number_PropertyRangeFilter = PropertyRangeFilter(field_name='prop_number', lookup_expr='range')
    prop_date_time_PropertyTimeFilter = PropertyTimeFilter(field_name='prop_date_time', lookup_expr='exact')
    prop_date_time_PropertyTimeRangeFilter = PropertyTimeRangeFilter(field_name='prop_date_time', lookup_expr='range')
    prop_number_PropertyTypedChoiceFilter = PropertyTypedChoiceFilter(field_name='prop_number', lookup_expr='exact', choices=NUMBER_CHOICES)
    prop_number_PropertyTypedMultipleChoiceFilter = PropertyTypedMultipleChoiceFilter(field_name='prop_number', lookup_expr='exact', conjoined=False, choices=NUMBER_CHOICES)
    prop_uuid_PropertyUUIDFilter = PropertyUUIDFilter(field_name='prop_uuid', lookup_expr='exact')
    prop_number_PropertyLookupChoiceFilter = PropertyLookupChoiceFilter(field_name='prop_number')

    class Meta:
        model = BenchmarkModel
        exclude = ['number', 'text', 'is_true', 'date', 'date_time', 'duration']

ALL_VALUE_FILTER_LOOKUP_LIST = [
    ('number_AllValuesFilter', 'prop_number_AllValuesFilter', NUMBER_RANGE[0]),
    ('number_AllValuesMultipleFilter', 'prop_number_PropertyAllValuesMultipleFilter', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[1])]),
    ('number_BaseCSVFilterNumber', 'prop_number_PropertyBaseCSVFilterNumber', str(NUMBER_RANGE[0])),
    ('number_BaseInFilterNumber', 'prop_number_PropertyBaseInFilterNumber', str(NUMBER_RANGE[0])),
    ('number_BaseRangeFilterNumber', 'prop_number_PropertyBaseRangeFilterNumber', F'{NUMBER_RANGE[0]},{NUMBER_RANGE[1]}'),
    ('is_true_BooleanFilter', 'prop_is_true_PropertyBooleanFilter', IS_TRUE_RANGE[0]),
    ('text_CharFilter_CharFilter', 'prop_text_PropertyCharFilter', TEXT_RANGE[0]),
    ('number_ChoiceFilter', 'prop_number_PropertyChoiceFilter', str(NUMBER_RANGE[0])),
    ('date_DateFilter', 'prop_date_PropertyDateFilter', str(DATE_RANGE[0])),
    ('date_DateRangeFilter', 'prop_date_PropertyDateRangeFilter', 'year'),
    ('date_time_DateTimeFilter', 'prop_date_time_PropertyDateTimeFilter', str(DATE_TIME_RANGE[0])),
    ('duration_DurationFilter', 'prop_duration_PropertyDurationFilter', '15 00:00:00'),
    ('date_time_IsoDateTimeFilter', 'prop_date_time_PropertyIsoDateTimeFilter',
        DATE_TIME_RANGE[0] + datetime.timedelta(days=2)),
    #('date_time_IsoDateTimeFromToRangeFilter', 'prop_date_time_PropertyIsoDateTimeFromToRangeFilter',
    #    (DATE_TIME_RANGE[0] - datetime.timedelta(days=2), DATE_TIME_RANGE[0] + datetime.timedelta(days=2))),
    ('number_MultipleChoiceFilter', 'prop_number_PropertyMultipleChoiceFilter', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[1])]),
    ('number_NumberFilter', 'prop_number_PropertyNumberFilter', NUMBER_RANGE[0]),
    ('number_OrderingFilter', 'prop_number_PropertyOrderingFilter', 'number'),
    #('date_time_TimeFilter', 'prop_date_time_PropertyTimeFilter', str(DATE_TIME_RANGE[0].time())),
    #('date_time_TimeRangeFilter', 'prop_date_time_PropertyTimeRangeFilter',
    #    (str(DATE_TIME_RANGE[0].time()), str(DATE_TIME_RANGE[1].time()))),
    ('number_TypedChoiceFilter', 'prop_number_PropertyTypedChoiceFilter', NUMBER_RANGE[0]),
    ('text_TypedMultipleChoiceFilter', 'prop_number_PropertyTypedMultipleChoiceFilter', [NUMBER_RANGE[0], NUMBER_RANGE[1]]),
    ('uuid_UUIDFilter', 'prop_uuid_PropertyUUIDFilter', UUID_RANGE[0]),

]

# Special case
LOOKUP_CHOICE_FILTER_LOOKUP_LIST = [
    ('number_LookupChoiceFilter', 'prop_number_PropertyLookupChoiceFilter', NUMBER_RANGE[0], 'exact'),
]

FROM_TO_RANGE_FILTER_LOOKUP_LIST = [
    ('date_DateFromToRangeFilter', 'prop_date_PropertyDateFromToRangeFilter',
        'after', str(DATE_RANGE[0]), 'before', str(DATE_RANGE[1])),
    ('date_time_DateTimeFromToRangeFilter', 'prop_date_time_PropertyDateTimeFromToRangeFilter',
        'after', str(DATE_TIME_RANGE[0]), 'before', str(DATE_TIME_RANGE[1])),
    ('number_RangeFilter', 'prop_number_PropertyRangeFilter', 'min', NUMBER_RANGE[0], 'max', NUMBER_RANGE[1]),
]
