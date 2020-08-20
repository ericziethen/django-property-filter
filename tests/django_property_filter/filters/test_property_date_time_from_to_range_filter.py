
import datetime

import pytest

from django.utils import timezone

from django_filters import FilterSet, DateTimeFromToRangeFilter

from django_property_filter import PropertyFilterSet, PropertyDateTimeFromToRangeFilter

from property_filter.models import DateTimeFromToRangeFilterModel


@pytest.mark.parametrize('lookup', PropertyDateTimeFromToRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyDateTimeFromToRangeFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyDateTimeFromToRangeFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyDateTimeFromToRangeFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'range'


@pytest.fixture
def fixture_property_time_range_filter():
    tz = timezone.get_default_timezone()

    DateTimeFromToRangeFilterModel.objects.create(id=-1, date_time=datetime.datetime(2020, 1, 1, 13, 30, tzinfo=tz))
    DateTimeFromToRangeFilterModel.objects.create(id=0, date_time=datetime.datetime(2020, 1, 1, 13, 40, tzinfo=tz))
    DateTimeFromToRangeFilterModel.objects.create(id=1, date_time=datetime.datetime(2020, 2, 2, 12, tzinfo=tz))
    DateTimeFromToRangeFilterModel.objects.create(id=2, date_time=datetime.datetime(2020, 2, 2, 12, 0, tzinfo=tz))
    DateTimeFromToRangeFilterModel.objects.create(id=3, date_time=datetime.datetime(2020, 2, 2, 12, 0, 0, tzinfo=tz))
    DateTimeFromToRangeFilterModel.objects.create(id=4, date_time=datetime.datetime(2021, 1, 1, 13, 30, tzinfo=tz))
    DateTimeFromToRangeFilterModel.objects.create(id=5, date_time=datetime.datetime(2021, 1, 1, 13, 30, tzinfo=tz))
    DateTimeFromToRangeFilterModel.objects.create(id=6, date_time=datetime.datetime(2022, 1, 1, 13, 30, tzinfo=tz))


TEST_LOOKUPS = [
    ('range', ('2018-02-02 12:00:00', '2030-02-02 12:00:00'), [-1, 0, 1, 2, 3, 4, 5, 6]),
    ('range', ('2020-02-02 12:00:00', '2020-02-02 12:00:00'), [1, 2, 3]),
    ('range', ('2020-02-02', '2020-02-03'), [1, 2, 3]),
    ('range', ('2020-02-03 12:00:00', '2020-02-02 12:00:00'), []),
    ('range', ('2021-02-03 12:00:00', '2024-02-03 12:00:00'), [6]),
    ('range', ('2020-12-03 12:00:00', '2022-01-01 13:30:00'), [4, 5, 6]),
    ('range', ('2020-02-02 12:00:00', None), [1, 2, 3, 4, 5, 6]),
    ('range', (None, '2020-02-02 12:00:00'), [-1, 0, 1, 2, 3]),
    ('range', (None, None), [-1, 0, 1, 2, 3, 4, 5, 6]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_time_range_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class DateTimeFromToRangeFilterSet(FilterSet):
        date_time = DateTimeFromToRangeFilter(field_name='date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = DateTimeFromToRangeFilterModel
            fields = ['date_time']

    filter_fs = DateTimeFromToRangeFilterSet({'date_time_after': lookup_val[0], 'date_time_before': lookup_val[1]}, queryset=DateTimeFromToRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyDateTimeFromToRangeFilterSet(PropertyFilterSet):
        prop_date_time = PropertyDateTimeFromToRangeFilter(field_name='prop_date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = DateTimeFromToRangeFilterModel
            fields = ['prop_date_time']

    prop_filter_fs = PropertyDateTimeFromToRangeFilterSet({'prop_date_time_after': lookup_val[0], 'prop_date_time_before': lookup_val[1]}, queryset=DateTimeFromToRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = DateTimeFromToRangeFilterModel
            exclude = ['date_time']
            property_fields = [('prop_date_time', PropertyDateTimeFromToRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({'prop_date_time__range_after': lookup_val[0], 'prop_date_time__range_before': lookup_val[1]}, queryset=DateTimeFromToRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDateTimeFromToRangeFilter.supported_lookups)
