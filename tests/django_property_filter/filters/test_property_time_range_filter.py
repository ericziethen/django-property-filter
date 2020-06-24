
import datetime

import pytest
from django_filters import FilterSet, TimeRangeFilter

from django_property_filter import PropertyFilterSet, PropertyTimeRangeFilter

from property_filter.models import TimeRangeModel


@pytest.mark.parametrize('lookup', PropertyTimeRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyTimeRangeFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyTimeRangeFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_time_range_filter():
    TimeRangeModel.objects.update_or_create(id=-1, time=datetime.time(7, 30, 15))
    TimeRangeModel.objects.update_or_create(id=0, time=datetime.time(7, 30, 15))
    TimeRangeModel.objects.update_or_create(id=1, time=datetime.time(8, 0, 0))
    TimeRangeModel.objects.update_or_create(id=2, time=datetime.time(8, 0, 0))
    TimeRangeModel.objects.update_or_create(id=3, time=datetime.time(8, 0, 0))
    TimeRangeModel.objects.update_or_create(id=4, time=datetime.time(15, 15, 15))
    TimeRangeModel.objects.update_or_create(id=5, time=datetime.time(18, 30))


TEST_LOOKUPS = [
    ('range', ('07:30:15', '18:30:00'), [-1, 0, 1, 2, 3, 4, 5]),
    ('range', ('08:00:00', '08:00:00'), [1, 2, 3]),
    ('range', ('08:00:01', '08:00:00'), []),
    ('range', ('15:15:30', '20:30:00'), [5]),
    ('range', ('20:30:00', '21:30:00'), []),
    ('range', ('08:00:00', None), [1, 2, 3, 4, 5]),
    ('range', (None, '08:00:00'), [-1, 0, 1, 2, 3]),
    ('range', (None, None), [-1, 0, 1, 2, 3, 4, 5]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_time_range_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class TimeRangeFilterSet(FilterSet):
        time = TimeRangeFilter(field_name='time', lookup_expr=lookup_xpr)

        class Meta:
            model = TimeRangeModel
            fields = ['time']

    filter_fs = TimeRangeFilterSet({'time_after': lookup_val[0], 'time_before': lookup_val[1]}, queryset=TimeRangeModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyTimeRangeFilterSet(FilterSet):
        prop_time = PropertyTimeRangeFilter(property_fld_name='prop_time', lookup_expr=lookup_xpr)

        class Meta:
            model = TimeRangeModel
            fields = ['prop_time']

    prop_filter_fs = PropertyTimeRangeFilterSet({'prop_time_after': lookup_val[0], 'prop_time_before': lookup_val[1]}, queryset=TimeRangeModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = TimeRangeModel
            exclude = ['time']
            property_fields = [('prop_time', PropertyTimeRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({'prop_time__range_after': lookup_val[0], 'prop_time__range_before': lookup_val[1]}, queryset=TimeRangeModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyTimeRangeFilter.supported_lookups)
