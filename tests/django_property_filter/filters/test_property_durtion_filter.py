
import datetime

import pytest
from django_filters import FilterSet, DurationFilter

from django_property_filter import PropertyFilterSet, PropertyDurationFilter

from property_filter.models import DurationFilterModel


@pytest.mark.parametrize('lookup', PropertyDurationFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyDurationFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyDurationFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_duration_filter():
    DurationFilterModel.objects.create(id=-1, duration=datetime.timedelta(hours=5))
    DurationFilterModel.objects.create(id=0, duration=datetime.timedelta(hours=5))
    DurationFilterModel.objects.create(id=1, duration=datetime.timedelta(days=1, hours=10))
    DurationFilterModel.objects.create(id=2, duration=datetime.timedelta(days=2, hours=10))
    DurationFilterModel.objects.create(id=3, duration=datetime.timedelta(days=2, hours=10))
    DurationFilterModel.objects.create(id=4, duration=datetime.timedelta(days=15))
    DurationFilterModel.objects.create(id=5, duration=datetime.timedelta(days=15))
    DurationFilterModel.objects.create(id=6, duration=datetime.timedelta(days=30))
    DurationFilterModel.objects.create(id=7, duration=datetime.timedelta(days=200))


TEST_LOOKUPS = [
    ('exact', '15 00:00:00', [4, 5]),
    #('iexact', '1 10:00:00', [1]),  Base Filter doesn't support iexact, so leaving out
    ('gt', '2 10:00:00', [4, 5, 6, 7]),
    ('gt', '2 09:59:59', [2, 3, 4, 5, 6, 7]),
    ('gte', '2 10:00:00', [2, 3, 4, 5, 6, 7]),
    ('lt', '15 00:00:00', [-1, 0, 1, 2, 3]),
    ('lte', '15 00:00:00', [-1, 0, 1, 2, 3, 4, 5]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_duration_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class DurationFilterSet(FilterSet):
        duration = DurationFilter(field_name='duration', lookup_expr=lookup_xpr)

        class Meta:
            model = DurationFilterModel
            fields = ['duration']

    filter_fs = DurationFilterSet({'duration': lookup_val}, queryset=DurationFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyDurationFilterSet(FilterSet):
        prop_duration = PropertyDurationFilter(property_fld_name='prop_duration', lookup_expr=lookup_xpr)

        class Meta:
            model = DurationFilterModel
            fields = ['prop_duration']

    prop_filter_fs = PropertyDurationFilterSet({'prop_duration': lookup_val}, queryset=DurationFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = DurationFilterModel
            exclude = ['duration']
            property_fields = [('prop_duration', PropertyDurationFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_duration__{lookup_xpr}': lookup_val}, queryset=DurationFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDurationFilter.supported_lookups)
