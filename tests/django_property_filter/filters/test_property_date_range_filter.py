
import datetime

import pytest

from django.utils import timezone

from django_filters import FilterSet, DateRangeFilter

from django_property_filter import PropertyFilterSet, PropertyDateRangeFilter

from property_filter.models import DateRangeFilterModel


@pytest.mark.parametrize('lookup', PropertyDateRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyDateRangeFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyDateRangeFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyDateRangeFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'exact'


# This is a bit abstract but since we need to know the same week/year whenever
# the tests are running we need to calculate them dynamically
SAME_MONTH_VALUES_DATE = []
SAME_YEAR_VALUES_DATE = []
SAME_MONTH_VALUES_DATETIME = []
SAME_YEAR_VALUES_DATETIME = []

@pytest.fixture
def fixture_property_filter():
    global SAME_MONTH_VALUES_DATE
    global SAME_YEAR_VALUES_DATE
    global SAME_MONTH_VALUES_DATETIME
    global SAME_YEAR_VALUES_DATETIME
    SAME_MONTH_VALUES_DATE = []
    SAME_YEAR_VALUES_DATE = []
    SAME_MONTH_VALUES_DATETIME = []
    SAME_YEAR_VALUES_DATETIME = []

    today_datetime = timezone.now()

    DateRangeFilterModel.objects.create(
        id=-1,
        date=today_datetime.date(),
        date_time=today_datetime)
    DateRangeFilterModel.objects.create(
        id=0,
        date=today_datetime.date() - datetime.timedelta(days=1),
        date_time=today_datetime - datetime.timedelta(days=1))
    DateRangeFilterModel.objects.create(
        id=1,
        date=today_datetime.date() - datetime.timedelta(days=6),
        date_time=today_datetime - datetime.timedelta(days=6))
    DateRangeFilterModel.objects.create(
        id=2,
        date=today_datetime.date() - datetime.timedelta(days=7),
        date_time=today_datetime - datetime.timedelta(days=7))
    DateRangeFilterModel.objects.create(
        id=3,
        date=today_datetime.date() - datetime.timedelta(days=15),
        date_time=today_datetime - datetime.timedelta(days=15))
    DateRangeFilterModel.objects.create(
        id=4,
        date=today_datetime.date() + datetime.timedelta(days=15),
        date_time=today_datetime + datetime.timedelta(days=15))
    DateRangeFilterModel.objects.create(
        id=5,
        date=today_datetime.date() + datetime.timedelta(days=400),
        date_time=today_datetime + datetime.timedelta(days=400))
    DateRangeFilterModel.objects.create(
        id=6,
        date=today_datetime.date() - datetime.timedelta(days=800),
        date_time=today_datetime - datetime.timedelta(days=800))

    today = timezone.now().date()
    for obj in DateRangeFilterModel.objects.all():
        if obj.date.month == today.month:
            SAME_MONTH_VALUES_DATE.append(obj.id)
        if obj.date.year == today.year:
            SAME_YEAR_VALUES_DATE.append(obj.id)
        if obj.date_time.month == today.month:
            SAME_MONTH_VALUES_DATETIME.append(obj.id)
        if obj.date_time.year == today.year:
            SAME_YEAR_VALUES_DATETIME.append(obj.id)


TEST_LOOKUPS_DATE = [
    ('exact', 'today', [-1]),
    ('exact', 'yesterday', [0]),
    ('exact', 'week', [-1, 0, 1, 2]),
    ('exact', 'month', 'SAME_MONTH_VALUES_DATE'),
    ('exact', 'year', 'SAME_YEAR_VALUES_DATE'),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS_DATE)
@pytest.mark.django_db
def test_lookup_xpr_date(fixture_property_filter, lookup_xpr, lookup_val, result_list):

    global SAME_MONTH_VALUES_DATE
    global SAME_YEAR_VALUES_DATE
    
    if result_list == 'SAME_MONTH_VALUES_DATE':
        result_list = SAME_MONTH_VALUES_DATE
    elif result_list == 'SAME_YEAR_VALUES_DATE':
        result_list = SAME_YEAR_VALUES_DATE

    # Test using Normal Django Filter
    class DateRangeFilterSet(FilterSet):
        date = DateRangeFilter(field_name='date', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['date']

    filter_fs = DateRangeFilterSet({'date': lookup_val}, queryset=DateRangeFilterModel.objects.all())

    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyDateRangeFilterSet(PropertyFilterSet):
        date = DateRangeFilter(field_name='date', lookup_expr=lookup_xpr)
        prop_date = PropertyDateRangeFilter(field_name='prop_date', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['prop_date']

    filter_fs_mixed = DateRangeFilterSet({'date': lookup_val}, queryset=DateRangeFilterModel.objects.all())
    prop_filter_fs_mixed = PropertyDateRangeFilterSet({'prop_date': lookup_val}, queryset=DateRangeFilterModel.objects.all())
    assert set(filter_fs_mixed.qs) == set(filter_fs.qs)
    assert set(prop_filter_fs_mixed.qs) == set(filter_fs.qs)


    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = DateRangeFilterModel
            exclude = ['date']
            property_fields = [('prop_date', PropertyDateRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_date__{lookup_xpr}': lookup_val}, queryset=DateRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


TEST_LOOKUPS_DATE_TIME = [
    ('exact', 'today', [-1]),
    ('exact', 'yesterday', [0]),
    ('exact', 'week', [-1, 0, 1, 2]),
    ('exact', 'month', 'SAME_MONTH_VALUES_DATETIME'),
    ('exact', 'year', 'SAME_YEAR_VALUES_DATETIME'),
]


@pytest.mark.filterwarnings('ignore::RuntimeWarning')  # 'week' on DayTime shows a Runtime Warning, ignore
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS_DATE_TIME)
@pytest.mark.django_db
def test_lookup_xpr_date_time(fixture_property_filter, lookup_xpr, lookup_val, result_list):

    global SAME_MONTH_VALUES_DATETIME
    global SAME_YEAR_VALUES_DATETIME
    
    if result_list == 'SAME_MONTH_VALUES_DATETIME':
        result_list = SAME_MONTH_VALUES_DATETIME
    elif result_list == 'SAME_YEAR_VALUES_DATETIME':
        result_list = SAME_YEAR_VALUES_DATETIME

    # Test using Normal Django Filter
    class DateRangeFilterSet(FilterSet):
        date_time = DateRangeFilter(field_name='date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['date_time']

    filter_fs = DateRangeFilterSet({'date_time': lookup_val}, queryset=DateRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyDateRangeFilterSet(PropertyFilterSet):
        prop_date_time = PropertyDateRangeFilter(field_name='prop_date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['prop_date_time']

    prop_filter_fs = PropertyDateRangeFilterSet({'prop_date_time': lookup_val}, queryset=DateRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)


    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = DateRangeFilterModel
            exclude = ['date_time']
            property_fields = [('prop_date_time', PropertyDateRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_date_time__{lookup_xpr}': lookup_val}, queryset=DateRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS_DATE]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDateRangeFilter.supported_lookups)
    tested_expressions = [x[0] for x in TEST_LOOKUPS_DATE_TIME]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDateRangeFilter.supported_lookups)
