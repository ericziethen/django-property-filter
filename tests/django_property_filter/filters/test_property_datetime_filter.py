
import datetime

import pytest
from django_filters import FilterSet, DateTimeFilter
from django.utils import timezone

from django_property_filter import PropertyFilterSet, PropertyDateTimeFilter

from property_filter.models import DateTimeFilterModel


@pytest.mark.parametrize('lookup', PropertyDateTimeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyDateTimeFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyDateTimeFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_date_time_filter():
    tz = timezone.get_default_timezone()

    DateTimeFilterModel.objects.update_or_create(id=-1, date_time=datetime.datetime(2020, 1, 1, 13, 30, tzinfo=tz))
    DateTimeFilterModel.objects.update_or_create(id=0, date_time=datetime.datetime(2020, 1, 1, 13, 40, tzinfo=tz))
    DateTimeFilterModel.objects.update_or_create(id=1, date_time=datetime.datetime(2020, 2, 2, 12, tzinfo=tz))
    DateTimeFilterModel.objects.update_or_create(id=2, date_time=datetime.datetime(2020, 2, 2, 12, 0, tzinfo=tz))
    DateTimeFilterModel.objects.update_or_create(id=3, date_time=datetime.datetime(2020, 2, 2, 12, 0, 0, tzinfo=tz))
    DateTimeFilterModel.objects.update_or_create(id=4, date_time=datetime.datetime(2021, 1, 1, 13, 30, tzinfo=tz))
    DateTimeFilterModel.objects.update_or_create(id=5, date_time=datetime.datetime(2021, 1, 1, 13, 30, tzinfo=tz))
    DateTimeFilterModel.objects.update_or_create(id=6, date_time=datetime.datetime(2022, 1, 1, 13, 30, tzinfo=tz))


TEST_LOOKUPS = [
    ('exact', '2019-03-02', []),
    ('exact', '2020-02-02 12:00:00', [1, 2, 3]),
    #('iexact', '2020-02-02 12:00:00', [1, 2, 3]),  Base Filter doesn't support iexact, so leaving out
    ('gt', '2020-02-02 11:59:59', [1, 2, 3, 4, 5, 6]),
    ('gte', '2020-02-02 11:59:59', [1, 2, 3, 4, 5, 6]),
    ('lt', '2020-02-02 12:00:00', [-1, 0]),
    ('lte', '2020-02-02 12:00:00', [-1, 0, 1, 2, 3]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_date_time_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class DateTimeFilterSet(FilterSet):
        date_time = DateTimeFilter(field_name='date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = DateTimeFilterModel
            fields = ['date_time']

    filter_fs = DateTimeFilterSet({'date_time': lookup_val}, queryset=DateTimeFilterModel.objects.all())
    print(filter_fs.qs)
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyDateTimeFilterSet(FilterSet):
        prop_date_time = PropertyDateTimeFilter(property_fld_name='prop_date_time', lookup_expr=lookup_xpr)

        class Meta:
            model = DateTimeFilterModel
            fields = ['prop_date_time']

    prop_filter_fs = PropertyDateTimeFilterSet({'prop_date_time': lookup_val}, queryset=DateTimeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = DateTimeFilterModel
            exclude = ['date_time']
            property_fields = [('prop_date_time', PropertyDateTimeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_date_time__{lookup_xpr}': lookup_val}, queryset=DateTimeFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDateTimeFilter.supported_lookups)
