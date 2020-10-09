
import pytest
from django_filters import FilterSet, NumericRangeFilter

try:
    from psycopg2.extras import NumericRange
except ImportError:
    pass

from django_property_filter import PropertyFilterSet, PropertyNumericRangeFilter

from property_filter.models import NumericRangeFilterModel

from tests.common import db_is_postgresql, db_is_sqlite




'''
# To keep Coverage at 100% we fake the Postgress Specific function under sqlite only
# The alternative would be to exclude, but I can't get it to exclude for sqlite only
# Therefore faking it is better to catch it when we run under postgres
@pytest.mark.skipif(not db_is_sqlite(), reason='Fake Coverage for Sqlite only')
def test_fake_postgres_coverage_for_sqlite():
    my_filter = PropertyNumericRangeFilter(field_name='fake_field', lookup_expr='exact')
    lookup_values = [slice(1, None), slice(None, 10), slice(1, 5)]

    for lookup_val in lookup_values:
        for lookup_expr in PropertyNumericRangeFilter.supported_lookups:
            my_filter._lookup_convertion(lookup_expr, lookup_val, )
'''

# Run the Convertion Test even under sqlite for code coverage
class FakePostgreasRange():
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
TEST_LOOKUP_CONVERTIONS = [
    ('exact', slice(1, 1), FakePostgreasRange(1, 1), 'postgres_range_exact', slice(1, 1), slice(1, 1)),
    ('contains', slice(1, 1), FakePostgreasRange(1, 1), 'postgres_range_contains', slice(1, 1), slice(1, 1)),
    ('contained_by', slice(1, 1), FakePostgreasRange(1, 1), 'postgres_range_contained_by', slice(1, 1), slice(1, 1)),
    ('overlap', slice(1, 1), FakePostgreasRange(1, 1), 'postgres_range_overlap', slice(1, 1), slice(1, 1)),
    ('exact', slice(5, None), FakePostgreasRange(1, 1), 'postgres_range_startwith', 5, slice(1, 1)),
    ('exact', slice(None, 34), FakePostgreasRange(1, 1), 'postgres_range_endwith', 34, slice(1, 1)),
]
@pytest.mark.parametrize(
    'in_lookup_xpr, in_lookup_val, in_prop_value, out_lookup_xpr, out_lookup_val, out_prop_value',
    TEST_LOOKUP_CONVERTIONS)
def test_lookup_convertion(
        in_lookup_xpr, in_lookup_val, in_prop_value,
        out_lookup_xpr, out_lookup_val, out_prop_value):
    my_filter = PropertyNumericRangeFilter(field_name='fake_field', lookup_expr=in_lookup_xpr)

    result_lookup_xpr, result_lookup_val, result_prop_value =\
        my_filter._lookup_convertion(in_lookup_xpr, in_lookup_val, in_prop_value)

    assert result_lookup_xpr == out_lookup_xpr
    assert result_lookup_val == out_lookup_val
    assert result_prop_value == out_prop_value



@pytest.mark.skipif(not db_is_postgresql(), reason='NumericRangeFilter only supported in PostGres')
@pytest.mark.parametrize('lookup', PropertyNumericRangeFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyNumericRangeFilter(field_name='fake_field', lookup_expr=lookup)


@pytest.mark.skipif(not db_is_postgresql(), reason='NumericRangeFilter only supported in PostGres')
def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyNumericRangeFilter(field_name='fake_field', lookup_expr='fake-lookup')


@pytest.mark.skipif(not db_is_postgresql(), reason='NumericRangeFilter only supported in PostGres')
def test_default_lookup():
    my_filter = PropertyNumericRangeFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'exact'


@pytest.fixture
@pytest.mark.skipif(not db_is_postgresql(), reason='NumericRangeFilter only supported in PostGres')
def fixture_property_numeric_range_filter():
    NumericRangeFilterModel.objects.create(id=-1,
        postgres_int_range=NumericRange(5, 10), postgres_decimal_range=NumericRange(5.0, 10.0))
    NumericRangeFilterModel.objects.create(id=0,
        postgres_int_range=NumericRange(5, 10), postgres_decimal_range=NumericRange(5.0, 10.0))
    NumericRangeFilterModel.objects.create(id=1,
        postgres_int_range=NumericRange(5, None), postgres_decimal_range=NumericRange(5.0, None))
    NumericRangeFilterModel.objects.create(id=2,
        postgres_int_range=NumericRange(None, 10), postgres_decimal_range=NumericRange(None, 10.0))
    NumericRangeFilterModel.objects.create(id=3,
        postgres_int_range=NumericRange(1, 10), postgres_decimal_range=NumericRange(1.0, 10.0))
    NumericRangeFilterModel.objects.create(id=4,
        postgres_int_range=NumericRange(5, 20), postgres_decimal_range=NumericRange(5.0, 20.0))
    NumericRangeFilterModel.objects.create(id=5,
        postgres_int_range=NumericRange(1, 20), postgres_decimal_range=NumericRange(1.0, 20.0))
    NumericRangeFilterModel.objects.create(id=6,
        postgres_int_range=None, postgres_decimal_range=None)


TEST_LOOKUPS = [
    ('exact', (5, 10), [-1, 0]),
    ('contains', (5, 10), [-1, 0, 1, 2, 3, 4, 5]),
    ('contains', (4, 10), [2, 3, 5]),
    ('contains', (5, 11), [1, 4, 5]),
    ('contains', (0, 100), []),
    ('contains', (5, None), [-1, 0, 1, 4]),
    ('contains', (None, 10), [-1, 0, 2, 3]),
    ('contained_by', (5, 10), [-1, 0]),
    ('contained_by', (4, 10), [-1, 0]),
    ('contained_by', (6, 10), []),
    ('contained_by', (5, 9), []),
    ('contained_by', (5, 11), [-1, 0]),
    ('contained_by', (1, 15), [-1, 0, 3]),
    ('contained_by', (5, None), [-1, 0, 1, 4]),
    ('contained_by', (None, 10), [-1, 0, 2, 3]),
    # For Overlap, start is included, end is excluded
    ('overlap', (4, 10), [-1, 0, 1, 2, 3, 4, 5]),
    ('overlap', (5, 10), [-1, 0, 1, 2, 3, 4, 5]),
    ('overlap', (5, None), [-1, 0, 1, 4]),  # Django-Filter only Matches the start
    ('overlap', (None, 10), [-1, 0, 2, 3]),  # Django-Filter only Matches the end
    ('overlap', (9, 22), [-1, 0, 1, 2, 3, 4, 5]),
    ('overlap', (10, 22), [1, 4, 5]),
    ('overlap', (22, 23), [1]),
]
@pytest.mark.skipif(not db_is_postgresql(), reason='NumericRangeFilter only supported in PostGres')
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr_int_range(fixture_property_numeric_range_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class NumericRangeFilterSet(FilterSet):
        postgres_int_range = NumericRangeFilter(field_name='postgres_int_range', lookup_expr=lookup_xpr)

        class Meta:
            model = NumericRangeFilterModel
            fields = ['postgres_int_range']

    filter_fs = NumericRangeFilterSet({'postgres_int_range_min': lookup_val[0], 'postgres_int_range_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyNumericRangeFilterSet(PropertyFilterSet):
        postgres_int_range = NumericRangeFilter(field_name='postgres_int_range', lookup_expr=lookup_xpr)
        prop_postgres_int_range = PropertyNumericRangeFilter(field_name='prop_postgres_int_range', lookup_expr=lookup_xpr)

        class Meta:
            model = NumericRangeFilterModel
            fields = ['prop_postgres_int_range']

    filter_fs_mixed = NumericRangeFilterSet({'postgres_int_range_min': lookup_val[0], 'postgres_int_range_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())
    prop_filter_fs_mixed = PropertyNumericRangeFilterSet({'prop_postgres_int_range_min': lookup_val[0], 'prop_postgres_int_range_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())

    assert set(filter_fs_mixed.qs) == set(filter_fs.qs)
    assert set(prop_filter_fs_mixed.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = NumericRangeFilterModel
            exclude = ['postgres_int_range', 'postgres_decimal_range']
            property_fields = [('prop_postgres_int_range', PropertyNumericRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_postgres_int_range__{lookup_xpr}_min': lookup_val[0], F'prop_postgres_int_range__{lookup_xpr}_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


# Django specifies that some fileds exclude the upper range (numeric). FOr some it is not specified
# https://docs.djangoproject.com/en/3.1/ref/contrib/postgres/fields/#querying-range-fields
# e.g. Decimal, so test to verify
TEST_LOOKUPS_DECIMAL_RANGE = [
    ('exact', (5.0, 10.0), [-1, 0]),
    ('contains', (5.0, 10.0), [-1, 0, 1, 2, 3, 4, 5]),
    ('contains', (4.0, 10.0), [2, 3, 5]),
    ('contains', (5.0, 11.0), [1, 4, 5]),
    ('contains', (0.0, 100.0), []),
    ('contains', (5.0, None), [-1, 0, 1, 4]),
    ('contains', (None, 10.0), [-1, 0, 2, 3]),
    ('contained_by', (5.0, 10.0), [-1, 0]),
    ('contained_by', (4.0, 10.0), [-1, 0]),
    ('contained_by', (6.0, 10.0), []),
    ('contained_by', (5.0, 9.0), []),
    ('contained_by', (5.0, 11.0), [-1, 0]),
    ('contained_by', (1.0, 15.0), [-1, 0, 3]),
    ('contained_by', (5.0, None), [-1, 0, 1, 4]),
    ('contained_by', (None, 10.0), [-1, 0, 2, 3]),
    ('overlap', (4.0, 10.0), [-1, 0, 1, 2, 3, 4, 5]),
    ('overlap', (5.0, 10.0), [-1, 0, 1, 2, 3, 4, 5]),
    ('overlap', (5.0, None), [-1, 0, 1, 4]),
    ('overlap', (None, 10.0), [-1, 0, 2, 3]),
    ('overlap', (9.0, 22.0), [-1, 0, 1, 2, 3, 4, 5]),
    ('overlap', (10.0, 22.0), [1, 4, 5]),
    ('overlap', (22.0, 23.0), [1]),
]
@pytest.mark.skipif(not db_is_postgresql(), reason='NumericRangeFilter only supported in PostGres')
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS_DECIMAL_RANGE)
@pytest.mark.django_db
def test_lookup_xpr_decimal_range(fixture_property_numeric_range_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class NumericRangeFilterSet(FilterSet):
        postgres_decimal_range = NumericRangeFilter(field_name='postgres_decimal_range', lookup_expr=lookup_xpr)

        class Meta:
            model = NumericRangeFilterModel
            fields = ['postgres_decimal_range']

    filter_fs = NumericRangeFilterSet({'postgres_decimal_range_min': lookup_val[0], 'postgres_decimal_range_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a normal PropertyFilterSet
    class PropertyNumericRangeFilterSet(PropertyFilterSet):
        postgres_decimal_range = NumericRangeFilter(field_name='postgres_decimal_range', lookup_expr=lookup_xpr)
        prop_postgres_decimal_range = PropertyNumericRangeFilter(field_name='prop_postgres_decimal_range', lookup_expr=lookup_xpr)

        class Meta:
            model = NumericRangeFilterModel
            fields = ['prop_postgres_decimal_range']

    filter_fs_mixed = NumericRangeFilterSet({'postgres_decimal_range_min': lookup_val[0], 'postgres_decimal_range_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())
    prop_filter_fs_mixed = PropertyNumericRangeFilterSet({'prop_postgres_decimal_range_min': lookup_val[0], 'prop_postgres_decimal_range_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())

    assert set(filter_fs_mixed.qs) == set(filter_fs.qs)
    assert set(prop_filter_fs_mixed.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = NumericRangeFilterModel
            exclude = ['postgres_int_range', 'postgres_decimal_range']
            property_fields = [('prop_postgres_decimal_range', PropertyNumericRangeFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_postgres_decimal_range__{lookup_xpr}_min': lookup_val[0], F'prop_postgres_decimal_range__{lookup_xpr}_max': lookup_val[1]}, queryset=NumericRangeFilterModel.objects.all())

    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


@pytest.mark.skipif(not db_is_postgresql(), reason='NumericRangeFilter only supported in PostGres')
def test_all_expressions_tested():

    # Integer Range Testing
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyNumericRangeFilter.supported_lookups)

    # Decimal Range Testing
    tested_expressions = [x[0] for x in TEST_LOOKUPS_DECIMAL_RANGE]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyNumericRangeFilter.supported_lookups)


