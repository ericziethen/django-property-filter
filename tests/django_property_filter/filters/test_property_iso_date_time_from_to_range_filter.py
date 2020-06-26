
import datetime

import pytest

from django.utils import timezone

from django_filters import FilterSet, IsoDateTimeFromToRangeFilter

from django_property_filter import PropertyFilterSet, PropertyIsoDateTimeFromToRangeFilter

from property_filter.models import IsoDateTimeFromToRangeFilterModel


@pytest.mark.parametrize('lookup', PropertyIsoDateTimeFromToRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyIsoDateTimeFromToRangeFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyIsoDateTimeFromToRangeFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_time_range_filter():
    tz = timezone.get_default_timezone()

    IsoDateTimeFromToRangeFilterModel.objects.create(id=-1, date_time=datetime.datetime(2020, 1, 1, 13, 30, tzinfo=tz))
    IsoDateTimeFromToRangeFilterModel.objects.create(id=0, date_time=datetime.datetime(2020, 1, 1, 13, 40, tzinfo=tz))
    IsoDateTimeFromToRangeFilterModel.objects.create(id=1, date_time=datetime.datetime(2020, 2, 2, 12, tzinfo=tz))
    IsoDateTimeFromToRangeFilterModel.objects.create(id=2, date_time=datetime.datetime(2020, 2, 2, 12, 0, tzinfo=tz))
    IsoDateTimeFromToRangeFilterModel.objects.create(id=3, date_time=datetime.datetime(2020, 2, 2, 12, 0, 0, tzinfo=tz))
    IsoDateTimeFromToRangeFilterModel.objects.create(id=4, date_time=datetime.datetime(2021, 1, 1, 13, 30, tzinfo=tz))
    IsoDateTimeFromToRangeFilterModel.objects.create(id=5, date_time=datetime.datetime(2021, 1, 1, 13, 30, tzinfo=tz))
    IsoDateTimeFromToRangeFilterModel.objects.create(id=6, date_time=datetime.datetime(2022, 1, 1, 13, 30, tzinfo=tz))


TEST_LOOKUPS = [
    ('range', ('2018-02-02 12:00:00', '2030-02-02 12:00:00'), [-1, 0, 1, 2, 3, 4, 5, 6]),
    #('range', ('2020-02-02 12:00:00', '2020-02-02 12:00:00'), [1, 2, 3]),
    #('range', ('2020-02-02', '2020-02-03'), [1, 2, 3]),
    #('range', ('2020-02-03 12:00:00', '2020-02-02 12:00:00'), []),
    #('range', ('2021-02-03 12:00:00', '2024-02-03 12:00:00'), [6]),
    #('range', ('2020-12-03 12:00:00', '2022-01-01 13:30:00'), [4, 5, 6]),
    #('range', ('2020-02-02 12:00:00', None), [1, 2, 3, 4, 5, 6]),
    #('range', (None, '2020-02-02 12:00:00'), [-1, 0, 1, 2, 3]),
    #('range', (None, None), [-1, 0, 1, 2, 3, 4, 5, 6]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
@pytest.mark.debug
def test_lookup_xpr(fixture_property_time_range_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class IsoDateTimeFromToRangeFilterSet(FilterSet):
        date_time = IsoDateTimeFromToRangeFilter(field_name='date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = IsoDateTimeFromToRangeFilterModel
            fields = ['date_time']

    filter_fs = IsoDateTimeFromToRangeFilterSet({'date_time_after': lookup_val[0], 'date_time_before': lookup_val[1]}, queryset=IsoDateTimeFromToRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyIsoDateTimeFromToRangeFilterSet(FilterSet):
        prop_date_time = PropertyIsoDateTimeFromToRangeFilter(property_fld_name='prop_date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = IsoDateTimeFromToRangeFilterModel
            fields = ['prop_date_time']

    prop_filter_fs = PropertyIsoDateTimeFromToRangeFilterSet({'prop_date_time_after': lookup_val[0], 'prop_date_time_before': lookup_val[1]}, queryset=IsoDateTimeFromToRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = IsoDateTimeFromToRangeFilterModel
            exclude = ['date_time']
            property_fields = [('prop_date_time', PropertyIsoDateTimeFromToRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({'prop_date_time__range_after': lookup_val[0], 'prop_date_time__range_before': lookup_val[1]}, queryset=IsoDateTimeFromToRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyIsoDateTimeFromToRangeFilter.supported_lookups)
