
import datetime

import pytest
from django_filters import FilterSet, IsoDateTimeFilter

from django_property_filter import PropertyFilterSet, PropertyIsoDateTimeFilter

from property_filter.models import IsoDateTimeFilterModel


@pytest.mark.parametrize('lookup', PropertyIsoDateTimeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyIsoDateTimeFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyIsoDateTimeFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyIsoDateTimeFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'exact'


@pytest.fixture
def fixture_property_iso_date_time_filter():
    # Avoiding Time Zone Manipulation to not having to convert iso times for comparison manually
    IsoDateTimeFilterModel.objects.create(id=-1, date_time='2020-01-03T00:00:00+00:00')
    IsoDateTimeFilterModel.objects.create(id=0, date_time='2020-01-03T01:00:00+00:00')
    IsoDateTimeFilterModel.objects.create(id=1, date_time='2020-01-03T02:00:00+00:00')
    IsoDateTimeFilterModel.objects.create(id=2, date_time='2020-12-03T02:00:00+00:00')
    IsoDateTimeFilterModel.objects.create(id=3, date_time='2020-12-03T02:00:00+00:00')
    IsoDateTimeFilterModel.objects.create(id=4, date_time='2021-12-03T02:00:00+00:00')


TEST_LOOKUPS = [
    ('exact', '2020-01-03T12:00:00+08:00', []),
    ('exact', '2020-12-03T02:00:00+00:00', [2, 3]),
    ('gt', '2020-01-03T01:00:00+00:00', [1, 2, 3, 4]),
    ('gte', '2020-01-03T01:00:00+00:00', [0, 1, 2, 3, 4]),
    ('lt', '2020-01-03T02:00:00+00:00', [-1, 0]),
    ('lte', '2020-01-03T02:00:00+00:00', [-1, 0, 1]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_iso_date_time_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class DateTimeFilterSet(FilterSet):
        date_time = IsoDateTimeFilter(field_name='date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = IsoDateTimeFilterModel
            fields = ['date_time']

    filter_fs = DateTimeFilterSet({'date_time': lookup_val}, queryset=IsoDateTimeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyIsoDateTimeFilterSet(FilterSet):
        prop_date_time = PropertyIsoDateTimeFilter(field_name='prop_date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = IsoDateTimeFilterModel
            fields = ['prop_date_time']

    prop_filter_fs = PropertyIsoDateTimeFilterSet({'prop_date_time': lookup_val}, queryset=IsoDateTimeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyIsoDateTimeFilterSet(PropertyFilterSet):
        prop_date_time = PropertyIsoDateTimeFilter(field_name='prop_date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = IsoDateTimeFilterModel
            fields = ['prop_date_time']

    prop_filter_fs = PropertyIsoDateTimeFilterSet({'prop_date_time': lookup_val}, queryset=IsoDateTimeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = IsoDateTimeFilterModel
            exclude = ['date_time']
            property_fields = [('prop_date_time', PropertyIsoDateTimeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_date_time__{lookup_xpr}': lookup_val}, queryset=IsoDateTimeFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyIsoDateTimeFilter.supported_lookups)
