
import datetime

import pytest

from django.utils import timezone

from django_filters import FilterSet, DateRangeFilter

from django_property_filter import PropertyFilterSet, PropertyDateRangeFilter

from property_filter.models import DateRangeFilterModel


@pytest.mark.parametrize('lookup', PropertyDateRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyDateRangeFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyDateRangeFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


SAME_MONTH_VALUES_DATE = []
SAME_YEAR_VALUES_DATE = []
SAME_MONTH_VALUES_DATETIME = []
SAME_YEAR_VALUES_DATETIME = []

@pytest.fixture
def fixture_property_filter():
    tz = timezone.get_default_timezone()

    global SAME_MONTH_VALUES_DATE
    global SAME_YEAR_VALUES_DATE
    global SAME_MONTH_VALUES_DATETIME
    global SAME_YEAR_VALUES_DATETIME
    SAME_MONTH_VALUES_DATE = []
    SAME_YEAR_VALUES_DATE = []
    SAME_MONTH_VALUES_DATETIME = []
    SAME_YEAR_VALUES_DATETIME = []

    DateRangeFilterModel.objects.create(
        id=-1,
        date=datetime.date.today(),
        date_time=datetime.datetime.now(tz=tz))
    DateRangeFilterModel.objects.create(
        id=0,
        date=datetime.date.today() - datetime.timedelta(days=1),
        date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=1))
    DateRangeFilterModel.objects.create(
        id=1,
        date=datetime.date.today() - datetime.timedelta(days=6),
        date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=6))
    DateRangeFilterModel.objects.create(
        id=2,
        date=datetime.date.today() - datetime.timedelta(days=7),
        date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=7))
    DateRangeFilterModel.objects.create(
        id=3,
        date=datetime.date.today() - datetime.timedelta(days=15),
        date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=15))
    DateRangeFilterModel.objects.create(
        id=4,
        date=datetime.date.today() + datetime.timedelta(days=15),
        date_time=datetime.datetime.now(tz=tz) + datetime.timedelta(days=15))
    DateRangeFilterModel.objects.create(
        id=5,
        date=datetime.date.today() + datetime.timedelta(days=400),
        date_time=datetime.datetime.now(tz=tz) + datetime.timedelta(days=400))
    DateRangeFilterModel.objects.create(
        id=6,
        date=datetime.date.today() - datetime.timedelta(days=800),
        date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=800))

    today = datetime.date.today()
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
    #('exact', 'month', [SAME_MONTH_VALUES_DATE]),
    #('exact', 'year', [SAME_YEAR_VALUES_DATE]),
    #('gt', 'today', []),
    #('gt', 'yesterday', []),
    #('gt', 'week', []),
    #('gt', 'month', [SAME_MONTH_VALUES_DATE]),
    #('gt', 'year', [SAME_YEAR_VALUES_DATE]),
    #('gte', 'today', []),
    #('gte', 'yesterday', []),
    #('gte', 'week', []),
    #('gte', 'month', [SAME_MONTH_VALUES_DATE]),
    #('gte', 'year', [SAME_YEAR_VALUES_DATE]),
    #('lt', 'today', []),
    #('lt', 'yesterday', []),
    #('lt', 'week', []),
    #('lt', 'month', [SAME_MONTH_VALUES_DATE]),
    #('lt', 'year', [SAME_YEAR_VALUES_DATE]),
    #('lte', 'today', []),
    #('lte', 'yesterday', []),
    #('lte', 'week', []),
    #('lte', 'month', [SAME_MONTH_VALUES_DATE]),
    #('lte', 'year', [SAME_YEAR_VALUES_DATE]),




    #('range', ('2018-01-01', '2021-01-01'), [-1, 0, 1, 2, 3, 4]),
    #('range', ('2019-03-02', '2019-03-02'), [0, 1]),
    #('range', ('2019-03-03', '2019-03-02'), []),
    #('range', ('2020-02-06', '2100-01-01'), [4]),
    #('range', ('2023-01-01', '2024-01-01'), []),
    #('range', ('2019-03-02', None), [0, 1, 2, 3, 4]),
    #('range', (None, '2019-03-02'), [-1, 0, 1]),
    #('range', (None, None), [-1, 0, 1, 2, 3, 4]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS_DATE)
@pytest.mark.django_db





@pytest.mark.debug
def test_lookup_xpr_date(fixture_property_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class DateRangeFilterSet(FilterSet):
        date = DateRangeFilter(field_name='date', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['date']

    filter_fs = DateRangeFilterSet({'date': lookup_val}, queryset=DateRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyDateRangeFilterSet(FilterSet):
        prop_date = PropertyDateRangeFilter(property_fld_name='prop_date', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['prop_date']

    prop_filter_fs = PropertyDateRangeFilterSet({'prop_date': lookup_val}, queryset=DateRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyDateRangeFilterSet(PropertyFilterSet):
        prop_date = PropertyDateRangeFilter(property_fld_name='prop_date', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['prop_date']

    prop_filter_fs = PropertyDateRangeFilterSet({'prop_date': lookup_val}, queryset=DateRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)


    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = DateRangeFilterModel
            exclude = ['date']
            property_fields = [('prop_date', PropertyDateRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_date__{lookup_xpr}': lookup_val}, queryset=DateRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


TEST_LOOKUPS_DATE_TIME = [
    #('range', ('2018-01-01', '2021-01-01'), [-1, 0, 1, 2, 3, 4]),
    #('range', ('2019-03-02', '2019-03-02'), [0, 1]),
    #('range', ('2019-03-02', '2019-03-02'), [0, 1]),
    #('range', ('2019-03-02 12:00:00', '2019-03-02 12:00:00'), [-1, 0, 1, 2, 3, 4]), # Any time component is ignored
    #('range', ('2019-03-03', '2019-03-02'), []),
    #('range', ('2020-02-06', '2100-01-01'), [4]),
    #('range', ('2023-01-01', '2024-01-01'), []),
    #('range', ('2019-03-02', None), [0, 1, 2, 3, 4]),
    #('range', (None, '2019-03-02'), [-1, 0, 1]),
    #('range', (None, None), [-1, 0, 1, 2, 3, 4]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS_DATE_TIME)
@pytest.mark.django_db





@pytest.mark.debug
def test_lookup_xpr_date_time(fixture_property_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class DateRangeFilterSet(FilterSet):
        date_time = DateRangeFilter(field_name='date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['date_time']

    filter_fs = DateRangeFilterSet({'date_time_after': lookup_val[0], 'date_time_before': lookup_val[1]}, queryset=DateRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyDateRangeFilterSet(FilterSet):
        prop_date_time = PropertyDateRangeFilter(property_fld_name='prop_date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['prop_date_time']

    prop_filter_fs = PropertyDateRangeFilterSet({'prop_date_time_after': lookup_val[0], 'prop_date_time_before': lookup_val[1]}, queryset=DateRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyDateRangeFilterSet(PropertyFilterSet):
        prop_date_time = PropertyDateRangeFilter(property_fld_name='prop_date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = DateRangeFilterModel
            fields = ['prop_date_time']

    prop_filter_fs = PropertyDateRangeFilterSet({'prop_date_time_after': lookup_val[0], 'prop_date_time_before': lookup_val[1]}, queryset=DateRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)


    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = DateRangeFilterModel
            exclude = ['date_time']
            property_fields = [('prop_date_time', PropertyDateRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({'prop_date_time__range_after': lookup_val[0], 'prop_date_time__range_before': lookup_val[1]}, queryset=DateRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS_DATE]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDateRangeFilter.supported_lookups)
    tested_expressions = [x[0] for x in TEST_LOOKUPS_DATE_TIME]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDateRangeFilter.supported_lookups)
