
import sqlite3

from unittest.mock import patch, PropertyMock

import pytest

from django.db import connection, transaction
from django.db.models.query import QuerySet
from django.db.utils import OperationalError
from django.test import TestCase

from django_property_filter.utils import (
    compare_by_lookup_expression,
    convert_int_list_to_range_lists,
    filter_qs_by_pk_list,
    get_db_vendor,
    get_db_version,
    get_max_params_for_db,
    get_value_for_db_field,
    sort_queryset,
)

from property_filter.models import (
    Delivery,
    DeliveryLine,
    Product,
    DoubleIntModel,
)

from tests.common import db_is_sqlite, db_is_postgresql


class GetAttributeTests(TestCase):

    def setUp(self):
        self.delivery1 = Delivery.objects.create(address='My Home')
        self.line1 = DeliveryLine.objects.create(line_no=1, delivery=self.delivery1)
        self.prod1 = Product.objects.create(name='Sun Rice', price='20.0', del_line=self.line1)

    def test_get_attribute_1_level(self):
        self.assertEqual(get_value_for_db_field(self.prod1, 'name'), 'Sun Rice')
        self.assertEqual(get_value_for_db_field(self.prod1, 'prop_name'), 'Sun Rice')

    def test_get_attribute_2_level(self):
        self.assertEqual(get_value_for_db_field(self.prod1, 'del_line__line_no'), 1)
        self.assertEqual(get_value_for_db_field(self.prod1, 'del_line__prop_line_no'), 1)

    def test_get_attribute_3_level(self):
        self.assertEqual(get_value_for_db_field(self.prod1, 'del_line__delivery__address'), 'My Home')
        self.assertEqual(get_value_for_db_field(self.prod1, 'del_line__delivery__prop_address'), 'My Home')

    def test_get_attribute_invalid_object(self):
        self.assertRaises(AttributeError, get_value_for_db_field, 'None', 'id')

    def test_get_attribute_invalid_field(self):
        self.assertRaises(AttributeError, get_value_for_db_field, self.prod1, 'invalid_field')

    def test_get_attribute_invalid_related_field(self):
        self.assertRaises(AttributeError, get_value_for_db_field, self.prod1, 'del_line__delivery__invalid_field')


LOOKUP_SUCCEED = [
    ('exact', 5, 5),
    ('exact', 'a', 'a'),
    ('iexact', 'a', 'A'),
    ('contains', 12, 1234),
    ('contains', 'ell', 'Hello'),
    ('icontains', 'Ell', 'Hello'),
    ('gt', 5, 5.000001),
    ('gte', 5, 5.00000),
    ('lt', 5, 4.9),
    ('lte', 5.0, 5),
    ('startswith', 'H', 'Hello'),
    ('startswith', 'Hel', 'Hello'),
    ('istartswith', 'hel', 'Hello'),
    ('endswith', 'ello', 'Hello'),
    ('endswith', 'Hello', 'Hello'),
    ('iendswith', 'hello', 'Hello'),
    ('isnull', True, None),
    ('isnull', False, 1),
    ('range', slice(3, 7), 3),
    ('range', slice(3, 7), 5),
    ('range', slice(3, 7), 7),
    ('in', [1, 3, 5], 1),
    ('in', [1, 3, 5], 3),
    ('in', [1, 3, 5], 5),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val, property_value', LOOKUP_SUCCEED)
def test_compare_by_lookup_expression_succeed(lookup_xpr, lookup_val, property_value):
    assert compare_by_lookup_expression(lookup_xpr, lookup_val, property_value)


LOOKUP_FAILED = [
    ('exact', 5, 6),
    ('exact', 'a', 'A'),
    ('iexact', 'a', 'A '),
    ('contains', 1234, 12),
    ('contains', 'Hello', 'ell'),
    ('contains', 'Ell', 'Hello'),
    ('icontains', 'Elo', 'Hello'),
    ('gt', 5, 5.00000),
    ('gt', 5, None),
    ('gt', None, 5),
    ('gte', 5, 4.999999),
    ('gte', None, 4.999999),
    ('gte', 5, None),
    ('lt', 5, 6),
    ('lt', 5.0, 5),
    ('lt', None, 5),
    ('lt', 5.0, None),
    ('lte', 5.000000, 5.000001),
    ('lte', None, 5.000001),
    ('lte', 5.000000, None),
    ('startswith', ' Hel', 'Hello'),
    ('startswith', 'ello', 'Hello'),
    ('startswith', 'hello', 'Hello'),
    ('istartswith', ' hello', 'Hello'),
    ('endswith', 'Hell', 'Hello'),
    ('endswith', 'hello', 'Hello'),
    ('iendswith', 'hell', 'Hello'),
    ('isnull', True, 1),
    ('isnull', False, None),
    ('range', slice(3, 7), 2.9),
    ('range', slice(3, 7), 7.1),
    ('range', slice(3, None), 2.9),
    ('in', [1, 3, 5], 4),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val, property_value', LOOKUP_FAILED)
def test_compare_by_lookup_expression_fail(lookup_xpr, lookup_val, property_value):
    assert not compare_by_lookup_expression(lookup_xpr, lookup_val, property_value)


class TestGetDbVendorVersion(TestCase):
    def test_get_db_vendor(self):
        with patch.object(connection, 'vendor', 'DATABASE_NAME'):
            assert get_db_vendor() == 'DATABASE_NAME'

    def test_get_db_version_sqlite(self):
        with patch.object(connection, 'vendor', 'sqlite'), patch.object(sqlite3, 'sqlite_version', '2.5.4'):
            assert get_db_version() == '2.5.4'

    def test_get_db_version_postgresql(self):
        with patch.object(connection, 'vendor', 'postgresql'):
            assert get_db_version() == 'Unknown'


DB_PARAM_LIMITS = [
    ('sqlite', '3.31.1', 999),
    ('sqlite', '3.32.0', 32766),
    ('postgresql', '1.0.0', None),
    ('postgresql', '9.9.9', None),
]
@pytest.mark.parametrize('db_name, db_version, max_params', DB_PARAM_LIMITS)
@pytest.mark.django_db
def test_get_max_db_param_values(db_name, db_version, max_params):
    with patch.object(connection, 'vendor', db_name), patch.object(sqlite3, 'sqlite_version', db_version):
        assert get_max_params_for_db() == max_params


class SortQuerysetTests(TestCase):

    def setUp(self):
        DoubleIntModel.objects.create(id=1, number=2, age=10)
        DoubleIntModel.objects.create(id=2, number=2, age=12)
        DoubleIntModel.objects.create(id=3, number=1, age=5)
        DoubleIntModel.objects.create(id=4, number=4, age=9)
        DoubleIntModel.objects.create(id=5, number=2, age=11)

    def test_sort_single_value_ascending(self):
        qs = DoubleIntModel.objects.all()
        assert list(qs)[0].id == 1

        sorted_qs = sort_queryset('prop_age', qs)

        assert list(sorted_qs.values_list('id', flat=True)) == [3, 4, 1, 5, 2]

    def test_sort_single_value_descending(self):
        qs = DoubleIntModel.objects.all()
        assert list(qs)[0].id == 1

        sorted_qs = sort_queryset('-prop_age', qs)

        assert list(sorted_qs.values_list('id', flat=True)) == [2, 5, 1, 4, 3]


class TestMaxParamLimits(TestCase):
    '''
    SQLite has a limit which effects bulk actions e.g. filter(pk__in=large_list)
    https://www.sqlite.org/limits.html
        - Maximum Number Of Host Parameters In A Single SQL Statement
        "the maximum value of a host parameter number is SQLITE_MAX_VARIABLE_NUMBER,
        which defaults to 999 for SQLite versions prior to 3.32.0 (2020-05-22) or
        32766 for SQLite versions after 3.32.0"

    Once Python Ships with a new Sqlite Version we will need to update our tests to cope with that

    '''

    def setUp(self):
        self.entry_count = 1000
        bulk_list = []

        with transaction.atomic():
            for _ in range(1, self.entry_count + 1):
                bulk_list.append(Delivery(address='My Home'))
            Delivery.objects.bulk_create(bulk_list)

        self.pk_list = list(Delivery.objects.all().values_list('pk', flat=True))

    def test_below_limit_ok(self):
        test_list = self.pk_list[:999]
        qs = Delivery.objects.all().filter(pk__in=test_list)
        qs.count()

        qs = filter_qs_by_pk_list(Delivery.objects.all(), test_list)
        qs.count()

    @patch('django_property_filter.utils.get_max_params_for_db')
    def test_limit_reached_mocked(self, mock_max_params):
        mock_max_params.return_value = 1

        test_list = self.pk_list[:2]

        with patch.object(QuerySet, 'count') as mock_method:
            mock_method.side_effect = OperationalError()
            qs = filter_qs_by_pk_list(Delivery.objects.all(), test_list)
            self.assertEqual(len(qs), 1)

    # Tests for sqlite (checking as not for postgresql in case adding more databases so not to skip)
    @pytest.mark.skiptravis
    @pytest.mark.skipif(db_is_postgresql(), reason='Sqlite has a limit of maximum params in can handle')
    def test_reached_sqlite_limit_sqlite_fail(self):
        test_list = self.pk_list[:1000]
        qs = Delivery.objects.all().filter(pk__in=test_list)
        with self.assertRaises(OperationalError, msg='expect "To many Sqlite Operations"'):
            qs.count()

        qs = filter_qs_by_pk_list(Delivery.objects.all(), test_list)
        self.assertEqual(qs.count(), get_max_params_for_db())

    # Tests for postgresql (checking as not for sqlite in case adding more databases so not to skip)
    @pytest.mark.skipif(db_is_sqlite(), reason='Postgres doesnt have the same limit as Sqlite')
    def test_reached_sqlite_limit_non_sqlite_ok(self):
        test_list = self.pk_list[:1000]
        qs = Delivery.objects.all().filter(pk__in=test_list)
        qs.count()

        qs = filter_qs_by_pk_list(Delivery.objects.all(), test_list)
        qs.count()


VOLUME_TEST_MAX = 100000
class VolumeTestQsFilteringByPkList(TestCase):

    def setUp(self):
        bulk_list = []

        with transaction.atomic():
            for _ in range(1, VOLUME_TEST_MAX + 1):
                bulk_list.append(Delivery(address='My Home'))
            Delivery.objects.bulk_create(bulk_list)

        self.pk_list = list(Delivery.objects.all().values_list('pk', flat=True))

    # Tests for sqlite (checking as not for postgresql in case adding more databases so not to skip)
    @pytest.mark.skipif(db_is_postgresql(), reason='Sqlite has a limit of maximum params in can handle')
    @pytest.mark.skiptravis
    def test_volume_filtering_sqlite(self):
        result_qs = filter_qs_by_pk_list(Delivery.objects.all(), self.pk_list)
        self.assertEqual(result_qs.count(), 999)

        self.assertEqual(
            set(result_qs.values_list('pk', flat=True)),
            set(self.pk_list[:999]),
        )

    # Tests for postgresql (checking as not for sqlite in case adding more databases so not to skip)
    @pytest.mark.skipif(db_is_sqlite(), reason='Postgres doesnt have the same limit as Sqlite')
    def test_volume_filtering_non_sqlite(self):
        result_qs = filter_qs_by_pk_list(Delivery.objects.all(), self.pk_list)
        self.assertEqual(result_qs.count(), VOLUME_TEST_MAX)

        self.assertEqual(
            set(result_qs.values_list('pk', flat=True)),
            set(Delivery.objects.all().values_list('pk', flat=True)),
        )


RANGE_TEST_DATA = [
    ([], [], []),
    ([1], [1], []),
    ([1, 2], [], [(1, 2)]),
    ([2, 1], [], [(1, 2)]),
    ([1, 3], [1, 3], []),
    ([3, 1], [1, 3], []),
    ([1, 2, 4], [4], [(1, 2)]),
    ([1, 2, 3], [], [(1, 3)]),
    ([-1, 0, 1, 4, 6, 7, 8, 9], [4], [(-1, 1), (6, 9)]),
    ([1, 2, 3, 10, 21, 22, 24], [10, 24], [(1, 3), (21, 22)]),
]
@pytest.mark.debug
@pytest.mark.parametrize('input_list, expected_single_list, expected_range_list', RANGE_TEST_DATA)
def test_range_data_convertion(input_list, expected_single_list, expected_range_list):
    single_list, range_list = convert_int_list_to_range_lists(input_list)

    assert single_list == expected_single_list
    assert range_list == expected_range_list


#@pytest.mark.debug
def test_large_number_range_convertion():
    assert False


#@pytest.mark.debug
def test_filtering_with_range_convertion():
    # TODO - Mock the max number
    assert False

