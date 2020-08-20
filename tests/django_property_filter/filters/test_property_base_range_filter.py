
import datetime

import pytest

from django_filters import FilterSet, BaseRangeFilter, DateFilter

from django_property_filter import PropertyFilterSet, PropertyBaseRangeFilter, PropertyDateFilter

from property_filter.models import BaseRangeFilterModel


@pytest.mark.parametrize('lookup', PropertyBaseRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyBaseRangeFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyBaseRangeFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyBaseRangeFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'range'

@pytest.fixture
def fixture_property_base_csv_filter():
    BaseRangeFilterModel.objects.create(id=-1, date=datetime.date(2018, 2, 1))
    BaseRangeFilterModel.objects.create(id=0, date=datetime.date(2019, 3, 2))
    BaseRangeFilterModel.objects.create(id=1, date=datetime.date(2019, 3, 2))
    BaseRangeFilterModel.objects.create(id=2, date=datetime.date(2019, 3, 4))
    BaseRangeFilterModel.objects.create(id=3, date=datetime.date(2020, 2, 5))
    BaseRangeFilterModel.objects.create(id=4, date=datetime.date(2020, 2, 6))
    BaseRangeFilterModel.objects.create(id=5, date=datetime.date(2020, 2, 6))
    BaseRangeFilterModel.objects.create(id=6, date=datetime.date(2020, 2, 6))
    BaseRangeFilterModel.objects.create(id=7, date=datetime.date(2020, 2, 9))

TEST_LOOKUPS = [
    ('range', '', [-1, 0, 1, 2, 3, 4, 5, 6, 7]),
    ('range', '2017-01-01, 2017-12-31', []),
    ('range', '2019-03-02, 2020-02-06', [0, 1, 2, 3, 4, 5, 6]),
    ('range', '2020-02-06,2019-03-02', []),
    ('range', '2020-02-08,2020-02-10', [7]),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_base_csv_filter, lookup_xpr, lookup_val, result_list):

    class BaseRangeFilterNumer(BaseRangeFilter, DateFilter):
        pass
    class PropertyBaseRangeFilterNumer(PropertyBaseRangeFilter, PropertyDateFilter):
        pass

    # Test using Normal Django Filter
    class BaseRangeFilterSet(FilterSet):
        date = BaseRangeFilterNumer(field_name='date', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseRangeFilterModel
            fields = ['date']

    filter_fs = BaseRangeFilterSet({'date': lookup_val}, queryset=BaseRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyBaseRangeFilterSet(PropertyFilterSet):
        prop_date = PropertyBaseRangeFilterNumer(field_name='prop_date', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseRangeFilterModel
            fields = ['prop_date']

    prop_filter_fs = PropertyBaseRangeFilterSet({'prop_date': lookup_val}, queryset=BaseRangeFilterModel.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = BaseRangeFilterModel
            exclude = ['date']
            property_fields = [('prop_date', PropertyBaseRangeFilterNumer, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_date__{lookup_xpr}': lookup_val}, queryset=BaseRangeFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)



INVALID_VALUES = [
    ('range', '2017-01-01,', ),
    ('range', ',', ),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val', INVALID_VALUES)
@pytest.mark.django_db
def test_invalid_range(fixture_property_base_csv_filter, lookup_xpr, lookup_val):
    class PropertyBaseRangeFilterNumer(PropertyBaseRangeFilter, PropertyDateFilter):
        pass

    class PropertyBaseRangeFilterSet(PropertyFilterSet):
        prop_date = PropertyBaseRangeFilterNumer(field_name='prop_date', lookup_expr=lookup_xpr)

        class Meta:
            model = BaseRangeFilterModel
            fields = ['prop_date']

    property_filter = PropertyBaseRangeFilterSet({'prop_date': lookup_val}, queryset=BaseRangeFilterModel.objects.all())
    with pytest.raises(ValueError):
        property_filter.qs


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyBaseRangeFilter.supported_lookups)
