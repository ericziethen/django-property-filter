
import datetime

import pytest
from django_filters import FilterSet, DateFilter

from django_property_filter import PropertyFilterSet, PropertyDateFilter

from property_filter.models import DateClass


@pytest.mark.parametrize('lookup', PropertyDateFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyDateFilter(property_fld_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyDateFilter(property_fld_name='fake_field', lookup_expr='fake-lookup')


@pytest.fixture
def fixture_property_date_filter():
    DateClass.objects.update_or_create(id=-1, date=datetime.date(2018, 2, 1))
    DateClass.objects.update_or_create(id=0, date=datetime.date(2018, 3, 2))
    DateClass.objects.update_or_create(id=1, date=datetime.date(2019, 3, 2))
    DateClass.objects.update_or_create(id=2, date=datetime.date(2019, 3, 2))
    DateClass.objects.update_or_create(id=3, date=datetime.date(2019, 3, 4))
    DateClass.objects.update_or_create(id=4, date=datetime.date(2020, 2, 5))


TEST_LOOKUPS = [
    ('exact', '2019-03-02', [1, 2]),
    ('iexact', '2019-03-02', [1, 2]),
    ('gt', '2018-03-02', [1, 2, 3, 4]),
    ('gte', '2018-03-02', [0, 1, 2, 3, 4]),
    ('lt', '2019-03-02', [-1, 0]),
    ('lte', '2019-03-02', [-1, 0, 1, 2]),
]


@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_date_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class DateFilterSet(FilterSet):
        date = DateFilter(field_name='date', lookup_expr=lookup_xpr)

        class Meta:
            model = DateClass
            fields = ['date']

    filter_fs = DateFilterSet({'date': lookup_val}, queryset=DateClass.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal Filterset
    class PropertyDateFilterSet(FilterSet):
        prop_date = PropertyDateFilter(property_fld_name='prop_date', lookup_expr=lookup_xpr)

        class Meta:
            model = DateClass
            fields = ['prop_date']

    prop_filter_fs = PropertyDateFilterSet({'prop_date': lookup_val}, queryset=DateClass.objects.all())
    assert set(prop_filter_fs.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = DateClass
            exclude = ['date']
            property_fields = [('prop_date', PropertyDateFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_date__{lookup_xpr}': lookup_val}, queryset=DateClass.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)

def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyDateFilter.supported_lookups)
