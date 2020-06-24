




# TODO MAKE SURE TO TEST 
# TODO - compare datetime with date objects
# TODO - compare datetime with datetime objects
# TODO - compare date with date objects
# TODO - compare date with datetime objects

import datetime

import pytest

from django.utils import timezone

from django_filters import FilterSet, DateFromToRangeFilter

from django_property_filter import PropertyFilterSet, PropertyDateFromToRangeFilter

from property_filter.models import DateFromToRangeFilterModel


@pytest.mark.parametrize('lookup', PropertyDateFromToRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyDateFromToRangeFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyDateFromToRangeFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_filter():
    tz = timezone.get_default_timezone()

    DateFromToRangeFilterModel.objects.update_or_create(
        id=-1,
        date=datetime.date(2018, 2, 1),
        date_time=datetime.datetime(2020, 1, 1, 13, 30, tzinfo=tz))
    DateFromToRangeFilterModel.objects.update_or_create(
        id=0,
        date=datetime.date(2019, 3, 2),
        date_time=datetime.datetime(2020, 1, 1, 13, 40, tzinfo=tz))
    DateFromToRangeFilterModel.objects.update_or_create(
        id=1,
        date=datetime.date(2019, 3, 2),
        date_time=datetime.datetime(2020, 2, 2, 12, tzinfo=tz))
    DateFromToRangeFilterModel.objects.update_or_create(
        id=2,
        date=datetime.date(2019, 3, 4),
        date_time=datetime.datetime(2020, 2, 2, 12, 0, tzinfo=tz))
    DateFromToRangeFilterModel.objects.update_or_create(
        id=3,
        date=datetime.date(2020, 2, 5),
        date_time=datetime.datetime(2020, 2, 2, 12, 0, 0, tzinfo=tz))
    DateFromToRangeFilterModel.objects.update_or_create(
        id=4,
        date=datetime.date(2020, 2, 6),
        date_time=datetime.datetime(2021, 1, 1, 13, 30, tzinfo=tz))


TEST_LOOKUPS_DATE = [
    ('range', ('2018-01-01', '2021-01-01'), [-1, 0, 1, 2, 3, 4]),
    ('range', ('2019-03-02', '2019-03-02'), [0, 1]),
    ('range', ('2019-03-03', '2019-03-02'), []),
    ('range', ('2020-02-06', '2100-01-01'), [4]),
    ('range', ('2023-01-01', '2024-01-01'), []),
    ('range', ('2019-03-02', None), [0, 1, 2, 3, 4]),
    ('range', (None, '2019-03-02'), [-1, 0, 1]),
    ('range', (None, None), [-1, 0, 1, 2, 3, 4]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS_DATE)
@pytest.mark.django_db
def test_lookup_xpr_date(fixture_property_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class DateFromToRangeFilterSet(FilterSet):
        date = DateFromToRangeFilter(field_name='date', lookup_expr=lookup_xpr)

        class Meta:
            model = DateFromToRangeFilterModel
            fields = ['date']

    filter_fs = DateFromToRangeFilterSet({'date_after': lookup_val[0], 'date_before': lookup_val[1]}, queryset=DateFromToRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyDateFromToRangeFilterSet(FilterSet):
        prop_date = PropertyDateFromToRangeFilter(property_fld_name='prop_date', lookup_expr=lookup_xpr)

        class Meta:
            model = DateFromToRangeFilterModel
            fields = ['prop_date']

    prop_filter_fs = PropertyDateFromToRangeFilterSet({'prop_date_after': lookup_val[0], 'prop_date_before': lookup_val[1]}, queryset=DateFromToRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = DateFromToRangeFilterModel
            exclude = ['date']
            property_fields = [('prop_date', PropertyDateFromToRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({'prop_date__range_after': lookup_val[0], 'prop_date__range_before': lookup_val[1]}, queryset=DateFromToRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

TEST_LOOKUPS_DATE_TIME = [

]

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDateFromToRangeFilter.supported_lookups)
    tested_expressions = [x[0] for x in TEST_LOOKUPS_DATE_TIME]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDateFromToRangeFilter.supported_lookups)
