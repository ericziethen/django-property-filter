
import datetime
import sys

from copy import deepcopy

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
ISO_DATE_TIME_RANGE = [
    '2020-01-03T12:00:00+12:00',
    '2020-01-03T12:00:00+11:00',
    '2021-12-03T12:00:00+10:00'
]
TIME_RANGE = [
    datetime.time(8, 0, 0),
    datetime.time(15, 15, 15),
    datetime.time(18, 30)
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


class AllFiltersFilterSet(FilterSet):
    number_AllValuesFilter = AllValuesFilter(field_name='number', lookup_expr='exact')
    number_AllValuesMultipleFilter_OR = AllValuesMultipleFilter(field_name='number', lookup_expr='exact', conjoined=False)  # OR
    number_AllValuesMultipleFilter_AND = AllValuesMultipleFilter(field_name='number', lookup_expr='exact', conjoined=True)  # AND
    number_BaseCSVFilterNumber = BaseCSVFilterNumber(field_name='number', lookup_expr='in')
    number_BaseInFilterNumber = BaseInFilterNumber(field_name='number', lookup_expr='in')
    number_BaseRangeFilterNumber = BaseRangeFilterNumber(field_name='number', lookup_expr='range')
    is_true_BooleanFilter = BooleanFilter(field_name='is_true', lookup_expr='exact')
    text_CharFilter = CharFilter(field_name='text', lookup_expr='exact')
    number_ChoiceFilter = ChoiceFilter(field_name='number', lookup_expr='exact', choices=NUMBER_CHOICES)
    date_DateFilter = DateFilter(field_name='date', lookup_expr='exact')
    date_DateFromToRangeFilter = DateFromToRangeFilter(field_name='date', lookup_expr='range')
    date_DateRangeFilter = DateRangeFilter(field_name='date', lookup_expr='exact')
    date_time_DateTimeFilter = DateTimeFilter(field_name='date_time', lookup_expr='exact')
    date_time_DateTimeFromToRangeFilter = DateTimeFromToRangeFilter(field_name='date_time', lookup_expr='range')
    duration_DurationFilter = DurationFilter(field_name='duration', lookup_expr='exact')
    iso_date_time_IsoDateTimeFilter = IsoDateTimeFilter(field_name='iso_date_time', lookup_expr='lt')
    iso_date_time_IsoDateTimeFromToRangeFilter = IsoDateTimeFromToRangeFilter(field_name='iso_date_time', lookup_expr='range')
    number_MultipleChoiceFilter_OR = MultipleChoiceFilter(field_name='number', lookup_expr='exact', conjoined=False, choices=NUMBER_CHOICES)
    number_MultipleChoiceFilter_AND = MultipleChoiceFilter(field_name='number', lookup_expr='exact', conjoined=True, choices=NUMBER_CHOICES)
    number_NumberFilter = NumberFilter(field_name='number', lookup_expr='exact')
    number_OrderingFilter = OrderingFilter(fields=('number', 'number'))
    number_RangeFilter = RangeFilter(field_name='number', lookup_expr='range')
    time_TimeFilter = TimeFilter(field_name='time', lookup_expr='exact')
    time_TimeRangeFilter = TimeRangeFilter(field_name='time', lookup_expr='range')
    number_TypedChoiceFilter = TypedChoiceFilter(field_name='number', lookup_expr='exact', choices=NUMBER_CHOICES)
    text_TypedMultipleChoiceFilter_OR = TypedMultipleChoiceFilter(field_name='number', lookup_expr='exact', conjoined=False, choices=NUMBER_CHOICES)
    text_TypedMultipleChoiceFilter_AND = TypedMultipleChoiceFilter(field_name='number', lookup_expr='exact', conjoined=True, choices=NUMBER_CHOICES)
    uuid_UUIDFilter = UUIDFilter(field_name='uuid', lookup_expr='exact')
    number_LookupChoiceFilter = LookupChoiceFilter(field_name='number')

    class Meta:
        model = BenchmarkModel
        exclude = ['number', 'text', 'is_true', 'date', 'date_time', 'duration']


class AllFiltersPropertyFilterSet(PropertyFilterSet):
    prop_number_AllValuesFilter = PropertyAllValuesFilter(field_name='prop_number', lookup_expr='exact')
    prop_number_PropertyAllValuesMultipleFilter_OR = PropertyAllValuesMultipleFilter(field_name='prop_number', lookup_expr='exact', conjoined=False)  # OR
    prop_number_PropertyAllValuesMultipleFilter_AND = PropertyAllValuesMultipleFilter(field_name='prop_number', lookup_expr='exact', conjoined=True)  # OR
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
    prop_iso_date_time_PropertyIsoDateTimeFilter = PropertyIsoDateTimeFilter(field_name='prop_iso_date_time', lookup_expr='lt')
    prop_iso_date_time_PropertyIsoDateTimeFromToRangeFilter = PropertyIsoDateTimeFromToRangeFilter(field_name='prop_iso_date_time', lookup_expr='range')
    prop_number_PropertyMultipleChoiceFilter_OR = PropertyMultipleChoiceFilter(field_name='prop_number', lookup_expr='exact', conjoined=False, choices=NUMBER_CHOICES)
    prop_number_PropertyMultipleChoiceFilter_AND = PropertyMultipleChoiceFilter(field_name='prop_number', lookup_expr='exact', conjoined=True, choices=NUMBER_CHOICES)
    prop_number_PropertyNumberFilter = PropertyNumberFilter(field_name='prop_number', lookup_expr='exact')
    prop_number_PropertyOrderingFilter = PropertyOrderingFilter(fields=('prop_number', 'prop_number'))
    prop_number_PropertyRangeFilter = PropertyRangeFilter(field_name='prop_number', lookup_expr='range')
    prop_time_PropertyTimeFilter = PropertyTimeFilter(field_name='prop_time', lookup_expr='exact')
    prop_time_PropertyTimeRangeFilter = PropertyTimeRangeFilter(field_name='prop_time', lookup_expr='range')
    prop_number_PropertyTypedChoiceFilter = PropertyTypedChoiceFilter(field_name='prop_number', lookup_expr='exact', choices=NUMBER_CHOICES)
    prop_number_PropertyTypedMultipleChoiceFilter_OR = PropertyTypedMultipleChoiceFilter(field_name='prop_number', lookup_expr='exact', conjoined=False, choices=NUMBER_CHOICES)
    prop_number_PropertyTypedMultipleChoiceFilter_AND = PropertyTypedMultipleChoiceFilter(field_name='prop_number', lookup_expr='exact', conjoined=True, choices=NUMBER_CHOICES)
    prop_uuid_PropertyUUIDFilter = PropertyUUIDFilter(field_name='prop_uuid', lookup_expr='exact')
    prop_number_PropertyLookupChoiceFilter = PropertyLookupChoiceFilter(field_name='prop_number')

    class Meta:
        model = BenchmarkModel
        exclude = ['number', 'text', 'is_true', 'date', 'date_time', 'duration']


SINGLE_FILTER_LOOKUP_LIST = [
    ('number_AllValuesFilter', 'prop_number_AllValuesFilter', NUMBER_RANGE[0]),
    ('number_AllValuesMultipleFilter_OR', 'prop_number_PropertyAllValuesMultipleFilter_OR', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[1])]),
    ('number_AllValuesMultipleFilter_AND', 'prop_number_PropertyAllValuesMultipleFilter_AND', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[0])]),
    ('number_BaseCSVFilterNumber', 'prop_number_PropertyBaseCSVFilterNumber', str(NUMBER_RANGE[0])),
    ('number_BaseInFilterNumber', 'prop_number_PropertyBaseInFilterNumber', str(NUMBER_RANGE[0])),
    ('number_BaseRangeFilterNumber', 'prop_number_PropertyBaseRangeFilterNumber', F'{NUMBER_RANGE[0]},{NUMBER_RANGE[1]}'),
    ('is_true_BooleanFilter', 'prop_is_true_PropertyBooleanFilter', IS_TRUE_RANGE[0]),
    ('text_CharFilter', 'prop_text_PropertyCharFilter', TEXT_RANGE[0]),
    ('number_ChoiceFilter', 'prop_number_PropertyChoiceFilter', str(NUMBER_RANGE[0])),
    ('date_DateFilter', 'prop_date_PropertyDateFilter', str(DATE_RANGE[0])),
    ('date_DateRangeFilter', 'prop_date_PropertyDateRangeFilter', 'year'),
    ('date_time_DateTimeFilter', 'prop_date_time_PropertyDateTimeFilter', str(DATE_TIME_RANGE[0])),
    ('duration_DurationFilter', 'prop_duration_PropertyDurationFilter', '15 00:00:00'),
    ('iso_date_time_IsoDateTimeFilter', 'prop_iso_date_time_PropertyIsoDateTimeFilter',
        ISO_DATE_TIME_RANGE[1]),
    ('number_MultipleChoiceFilter_OR', 'prop_number_PropertyMultipleChoiceFilter_OR', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[1])]),
    ('number_MultipleChoiceFilter_AND', 'prop_number_PropertyMultipleChoiceFilter_AND', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[0])]),
    ('number_NumberFilter', 'prop_number_PropertyNumberFilter', NUMBER_RANGE[0]),
    ('number_OrderingFilter', 'prop_number_PropertyOrderingFilter', ('number', 'prop_number')),
    ('time_TimeFilter', 'prop_time_PropertyTimeFilter', str(TIME_RANGE[0])),
    ('number_TypedChoiceFilter', 'prop_number_PropertyTypedChoiceFilter', NUMBER_RANGE[0]),
    ('text_TypedMultipleChoiceFilter_AND', 'prop_number_PropertyTypedMultipleChoiceFilter_AND', [NUMBER_RANGE[0], NUMBER_RANGE[0]]),
    ('uuid_UUIDFilter', 'prop_uuid_PropertyUUIDFilter', UUID_RANGE[0]),

    # Range Filters
    ('date_DateFromToRangeFilter', 'prop_date_PropertyDateFromToRangeFilter', (str(DATE_RANGE[0]), str(DATE_RANGE[1]))),
    ('date_time_DateTimeFromToRangeFilter', 'prop_date_time_PropertyDateTimeFromToRangeFilter',
        (str(DATE_TIME_RANGE[0]), str(DATE_TIME_RANGE[1]))),
    ('number_RangeFilter', 'prop_number_PropertyRangeFilter', (NUMBER_RANGE[0], NUMBER_RANGE[1])),
    ('time_TimeRangeFilter', 'prop_time_PropertyTimeRangeFilter',
        (str(TIME_RANGE[0]), str(TIME_RANGE[1]))),
    ('iso_date_time_IsoDateTimeFromToRangeFilter', 'prop_iso_date_time_PropertyIsoDateTimeFromToRangeFilter',
        (ISO_DATE_TIME_RANGE[0], ISO_DATE_TIME_RANGE[1])),

    # Lookup Filters
    ('number_LookupChoiceFilter', 'prop_number_PropertyLookupChoiceFilter', (NUMBER_RANGE[0], 'exact')),
]


MULTI_FILTER_LOOKUP_LIST = [
    [
        ('number_RangeFilter', 'prop_number_PropertyRangeFilter', (NUMBER_RANGE[0], NUMBER_RANGE[1])),
        ('text_CharFilter', 'prop_text_PropertyCharFilter', TEXT_RANGE[0]),
        ('is_true_BooleanFilter', 'prop_is_true_PropertyBooleanFilter', IS_TRUE_RANGE[0]),
        ('date_DateFilter', 'prop_date_PropertyDateFilter', DATE_RANGE[0]),
        ('date_time_DateTimeFilter', 'prop_date_time_PropertyDateTimeFilter', DATE_TIME_RANGE[0]),
    ],
    [
        ('number_MultipleChoiceFilter_OR', 'prop_number_PropertyMultipleChoiceFilter_OR', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[1])]),
        ('text_CharFilter', 'prop_text_PropertyCharFilter', TEXT_RANGE[0]),
    ],
    [
        ('text_CharFilter', 'prop_text_PropertyCharFilter', TEXT_RANGE[0]),
        ('number_MultipleChoiceFilter_OR', 'prop_number_PropertyMultipleChoiceFilter_OR', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[1])]),
    ],
    [
        ('number_MultipleChoiceFilter_AND', 'prop_number_PropertyMultipleChoiceFilter_AND', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[0])]),
        ('text_CharFilter', 'prop_text_PropertyCharFilter', TEXT_RANGE[0]),
    ],
    [
        ('text_CharFilter', 'prop_text_PropertyCharFilter', TEXT_RANGE[0]),
        ('number_MultipleChoiceFilter_AND', 'prop_number_PropertyMultipleChoiceFilter_AND', [str(NUMBER_RANGE[0]), str(NUMBER_RANGE[0])]),
    ],
]


LOOKUP_FILTER_TYPES = [
    LookupChoiceFilter, PropertyLookupChoiceFilter
]


RANGE_FILTER_SUFFIXES = {
    DateFromToRangeFilter: ('after', 'before'),
    PropertyDateFromToRangeFilter: ('after', 'before'),
    DateTimeFromToRangeFilter: ('after', 'before'),
    PropertyDateTimeFromToRangeFilter: ('after', 'before'),
    IsoDateTimeFromToRangeFilter: ('after', 'before'),
    PropertyIsoDateTimeFromToRangeFilter: ('after', 'before'),
    TimeRangeFilter: ('after', 'before'),
    PropertyTimeRangeFilter: ('after', 'before'),
    RangeFilter: ('min', 'max'),
    PropertyRangeFilter: ('min', 'max'),
}
def get_range_suffixes_for_filter_type(filter_type):
    from_suffix = None
    to_suffix = None

    if filter_type in RANGE_FILTER_SUFFIXES:
        from_suffix, to_suffix = RANGE_FILTER_SUFFIXES[filter_type]

    return (from_suffix, to_suffix)


def get_filtertype_from_filter_name(filterset, filter_name):
    if filter_name in filterset.filters:
        return filterset.filters[filter_name].__class__

    return None

def get_filter_types_from_filter_names(filterset, filter_name_list):
    type_list = []
    unknown_list = []

    for name in filter_name_list:
        filter_type = get_filtertype_from_filter_name(filterset, name)

        # Check name as is
        if filter_type:
            type_list.append(filter_type.__name__)
        else:
            #unknown_list.append(F'Unknown Type for "{name}"')
            raise ValueError(F'Unknown Filter Type for Filter "{name}"')

    # In some cases  has multiple entries, not all are the filternames but could be expressions
    if not type_list:
        type_list = unknown_list

    return list(set(type_list))

def create_filter_dics(filter_info_list):
    filter_dic = {}
    prop_filter_dic = {}
    filter_names = []
    prop_filter_names = []

    for filter_name, prop_filter_name, lookup_value in filter_info_list:
        filter_names.append(filter_name)
        prop_filter_names.append(prop_filter_name)

        filter_type = get_filtertype_from_filter_name(AllFiltersFilterSet(), filter_name)
        prop_filter_type = get_filtertype_from_filter_name(AllFiltersPropertyFilterSet(), prop_filter_name)

        from_suffix, to_suffix = get_range_suffixes_for_filter_type(filter_type)
        prop_from_suffix, prop_to_suffix = get_range_suffixes_for_filter_type(prop_filter_type)

        # Create the Filter dic
        if from_suffix or to_suffix:
            filter_dic = {F'{filter_name}_{from_suffix}': lookup_value[0], F'{filter_name}_{to_suffix}': lookup_value[1]}
        elif filter_type in LOOKUP_FILTER_TYPES:
            filter_dic = {filter_name: lookup_value[0], F'{filter_name}_lookup': lookup_value[1]}
        elif isinstance(lookup_value, tuple):
            filter_dic = {filter_name: lookup_value[0]}
        else:
            filter_dic = {filter_name: lookup_value}

        # Create the Property Filter dic
        if prop_from_suffix or prop_to_suffix:
            prop_filter_dic = {F'{prop_filter_name}_{prop_from_suffix}': lookup_value[0], F'{prop_filter_name}_{prop_to_suffix}': lookup_value[1]}
        elif prop_filter_type in LOOKUP_FILTER_TYPES:
            prop_filter_dic = {prop_filter_name: lookup_value[0], F'{prop_filter_name}_lookup': lookup_value[1]}
        elif isinstance(lookup_value, tuple):
            prop_filter_dic = {prop_filter_name: lookup_value[1]}
        else:
            prop_filter_dic = {prop_filter_name: lookup_value}

    return (filter_dic, filter_names, prop_filter_dic, prop_filter_names)


def create_test_filtersets(filter_info_list):
    filter_dic, filter_names, prop_filter_dic, prop_filter_names = create_filter_dics(filter_info_list)

    # Create the Filtersets
    filter_fs = AllFiltersFilterSet(filter_dic, queryset=BenchmarkModel.objects.all())
    property_filter_fs = AllFiltersPropertyFilterSet(prop_filter_dic, queryset=BenchmarkModel.objects.all())

    return (filter_fs, filter_names, property_filter_fs, prop_filter_names)

def remove_unneeded_filters_from_fs(filter_set, filter_names):
    new_fs = deepcopy(filter_set)
    for name in list(new_fs.filters.keys()):
        if name not in filter_names:
            del new_fs.filters[name]

            if hasattr(new_fs, '_form'):
                del new_fs.form.cleaned_data[name]

    return new_fs
