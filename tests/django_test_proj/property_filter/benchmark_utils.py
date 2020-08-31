
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

from property_filter.models import MultiFilterTestModel as BenchmarkModel


NUMBER_RANGE = [1, 2, 3]
TEXT_RANGE = ['One', 'Two', 'Three']
IS_TRUE_RANGE = [True, False]
DATE_RANGE = [
    datetime.date(2018, 2, 1),
    datetime.date(2018, 3, 1),
    datetime.date(2018, 4, 1),
    timezone.now().date()
]
DATE_TIME_RANGE = [
    datetime.datetime(2066, 3, 2, 12, tzinfo=timezone.get_default_timezone()),
    datetime.datetime(2066, 3, 3, 12, tzinfo=timezone.get_default_timezone()),
    datetime.datetime(2066, 3, 4, 12, tzinfo=timezone.get_default_timezone())
]
NUMBER_CHOICES = [(c, F'Number: {c}') for c in NUMBER_RANGE]


class BaseCSVFilterNumber(BaseCSVFilter, CharFilter):
    pass
class PropertyBaseCSVFilterNumber(PropertyBaseCSVFilter, PropertyCharFilter):
    pass
class BaseInFilterNumber(BaseInFilter, CharFilter):
    pass
class PropertyBaseInFilterNumber(PropertyBaseInFilter, PropertyCharFilter):
    pass
class BaseRangeFilterNumber(BaseRangeFilter, DateFilter):
    pass
class PropertyBaseRangeFilterNumber(PropertyBaseRangeFilter, PropertyDateFilter):
    pass


class MultiFilterFilterSet(FilterSet):
    number = MultipleChoiceFilter(
        field_name='number', lookup_expr='exact', conjoined=False,  # OR
        choices=NUMBER_CHOICES)
    class Meta:
        model = BenchmarkModel
        fields = ['text', 'is_true', 'date', 'date_time']


class PropertyMultiFilterFilterSet(PropertyFilterSet):
    prop_number = PropertyMultipleChoiceFilter(
        field_name='prop_number', lookup_expr='exact', conjoined=False,  # OR
        choices=NUMBER_CHOICES)

    class Meta:
        model = BenchmarkModel
        fields = ['prop_number']
        exclude = ['number', 'text', 'is_true', 'date', 'date_time']
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



    class Meta:
        model = BenchmarkModel
        exclude = ['number', 'text', 'is_true', 'date', 'date_time']


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




    class Meta:
        model = BenchmarkModel
        exclude = ['number', 'text', 'is_true', 'date', 'date_time']

ALL_VALUE_FILTER_LOOKUP_LIST = [
    ('number_AllValuesFilter', 'prop_number_AllValuesFilter', NUMBER_RANGE[0]),
    ('number_AllValuesMultipleFilter', 'prop_number_PropertyAllValuesMultipleFilter', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[1])]),
    ('number_BaseCSVFilterNumber', 'prop_number_PropertyBaseCSVFilterNumber', str(NUMBER_RANGE[0])),
    ('number_BaseInFilterNumber', 'prop_number_PropertyBaseInFilterNumber', str(NUMBER_RANGE[0])),
    #('number_BaseRangeFilterNumber', 'prop_number_PropertyBaseRangeFilterNumber', F'{NUMBER_RANGE[0]},{NUMBER_RANGE[1]}'),
    ('is_true_BooleanFilter', 'prop_is_true_PropertyBooleanFilter', IS_TRUE_RANGE[0]),
    ('text_CharFilter_CharFilter', 'prop_text_PropertyCharFilter', TEXT_RANGE[0]),
    ('number_ChoiceFilter', 'prop_number_PropertyChoiceFilter', str(NUMBER_RANGE[0])),
    ('date_DateFilter', 'prop_date_PropertyDateFilter', str(DATE_RANGE[0])),
    #('date_DateFromToRangeFilter', 'prop_date_PropertyDateFromToRangeFilter', (str(DATE_RANGE[0]), str(DATE_RANGE[1]))),
    ('date_DateRangeFilter', 'prop_date_PropertyDateRangeFilter', 'year'),
    #('', '', ),
    #('', '', ),
    #('', '', ),
    #('', '', ),
    #('', '', ),
    #('', '', ),
    #('', '', ),



    #('', '', ),
]


'''
from django_filters import (
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

    BaseRangeFilterNumber
)

from django_property_filter import (
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

    PropertyBaseRangeFilterNumber
)
'''
