
import logging
import os
import random
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
    sort_range_list,
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
    ('slice_exact', slice(6, 13), slice(6, 13)),
    ('slice_contains', slice(6, 13), slice(6, 13)),
    ('slice_contains', slice(6, 13), slice(5, 13)),
    ('slice_contains', slice(6, 13), slice(6, 14)),
    ('slice_contains', slice(6, None), slice(6, 13)),
    ('slice_contains', slice(None, 13), slice(6, 13)),
    ('slice_contains', slice(6, 13), slice(6, None)),
    ('slice_contains', slice(6, 13), slice(None, 13)),
    ('slice_contained_by', slice(6, 13), slice(6, 13)),
    ('slice_contained_by', slice(5, 13), slice(6, 13)),
    ('slice_contained_by', slice(6, 14), slice(6, 13)),
    ('slice_contained_by', slice(6, None), slice(6, None)),
    ('slice_contained_by', slice(None, 13), slice(None, 13)),
    ('slice_contained_by', slice(6, None), slice(6, 13)),
    ('slice_contained_by', slice(None, 13), slice(6, 13)),
    ('slice_overlap', slice(5, 10), slice(5, 10)),
    ('slice_overlap', slice(5, 10), slice(7, 9)),
    ('slice_overlap', slice(7, 9), slice(5, 10)),
    ('slice_overlap', slice(5, 10), slice(2, 6)),
    ('slice_overlap', slice(2, 6), slice(5, 10)),
    ('slice_overlap', slice(5, 10), slice(8, 12)),
    ('slice_overlap', slice(8, 12), slice(5, 10)),
    ('slice_overlap', slice(5, 10), slice(None, 7)),
    ('slice_overlap', slice(None, 7), slice(5, 10)),
    ('slice_overlap', slice(5, 10), slice(7, None)),
    ('slice_overlap', slice(7, None), slice(5, 10)),
    ('slice_overlap', slice(7, None), slice(5, None)),
    ('slice_overlap', slice(None, 7), slice(None, 10)),
    ('slice_overlap', slice(None, 7), slice(6, None)),
    ('slice_overlap', slice(6, None), slice(None, 7)),





    
]
@pytest.mark.debug
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
    ('slice_exact', slice(6, 13), slice(1, 13)),
    ('slice_exact', slice(6, 13), slice(6, 55)),
    ('slice_exact', slice(6, 13), slice(4, 25)),
    ('slice_contains', slice(6, 13), slice(7, 13)),
    ('slice_contains', slice(6, 13), slice(6, 12)),
    ('slice_contains', slice(6, 13), slice(5, 12)),
    ('slice_contains', slice(6, 13), slice(7, None)),
    ('slice_contains', slice(6, 13), slice(None, 12)),
    ('slice_contains', slice(None, 13), slice(6, 14)),
    ('slice_contains', slice(6, None), slice(5, 13)),
    ('slice_contained_by', slice(7, 13), slice(6, 13)),
    ('slice_contained_by', slice(6, 12), slice(6, 13)),
    ('slice_contained_by', slice(5, 12), slice(6, 13)),
    ('slice_contained_by', slice(7, None), slice(6, 13)),
    ('slice_contained_by', slice(None, 12), slice(6, 13)),
    ('slice_contained_by', slice(6, 13), slice(None, 13)),
    ('slice_contained_by', slice(6, 13), slice(6, None)),
    ('slice_overlap', slice(5, 10), slice(4, 5)),
    ('slice_overlap', slice(4, 5), slice(5, 10)),
    ('slice_overlap', slice(5, 10), slice(5, 5)),
    ('slice_overlap', slice(5, 5), slice(5, 10)),
    ('slice_overlap', slice(5, 10), slice(10, 10)),
    ('slice_overlap', slice(10, 10), slice(5, 10)),
    ('slice_overlap', slice(5, 10), slice(10, 11)),
    ('slice_overlap', slice(10, 11), slice(5, 10)),
    ('slice_overlap', slice(2, 4), slice(15, 25)),
    ('slice_overlap', slice(5, 10), slice(11, None)),
    ('slice_overlap', slice(11, None), slice(5, 10)),
    ('slice_overlap', slice(5, 10), slice(None, 4)),
    ('slice_overlap', slice(5, 10), slice(None, 5)),
    ('slice_overlap', slice(None, 4), slice(5, 10)),
    ('slice_overlap', slice(None, 5), slice(5, 10)),
    ('slice_overlap', slice(None, 7), slice(7, None)),
    ('slice_overlap', slice(None, 7), slice(8, None)),
    ('slice_overlap', slice(8, None), slice(None, 7)),
]
@pytest.mark.debug
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
def test_get_max_db_param_values(db_name, db_version, max_params):
    with patch.object(connection, 'vendor', db_name), patch.object(sqlite3, 'sqlite_version', db_version):
        assert get_max_params_for_db() == max_params


DB_PARAM_LIMIT_USER_SET = [
    ('sqlite', '3.31.1', 1000),
    ('sqlite', '3.32.0', 5000),
    ('postgresql', '1.0.0', 1000),
    ('postgresql', '9.9.9', 5000),
]
@pytest.mark.parametrize('db_name, db_version, user_limit', DB_PARAM_LIMIT_USER_SET)
def test_get_max_db_param_values_user_values(db_name, db_version, user_limit):
    os.environ['USER_DB_MAX_PARAMS'] = str(user_limit)

    with patch.object(connection, 'vendor', db_name), patch.object(sqlite3, 'sqlite_version', db_version):
        assert get_max_params_for_db() == user_limit


def test_get_max_db_param_values_user_values_invalid(caplog):
    os.environ['USER_DB_MAX_PARAMS'] = 'not int invalid'

    with patch.object(connection, 'vendor', 'sqlite'),\
         patch.object(sqlite3, 'sqlite_version', '3.32.0'),\
         caplog.at_level(logging.ERROR):

        assert get_max_params_for_db() == 32766
        assert F'Invalid Environment Variable "USER_DB_MAX_PARAMS", int expected but got "not int invalid".' in caplog.text


RANGE_TEST_DATA = [
    ([], []),
    ([1], [(1, 1)]),
    ([1, 2], [(1, 2)]),
    ([2, 1], [(1, 2)]),
    ([1, 3], [(1, 1), (3, 3)]),
    ([3, 1], [(1, 1), (3, 3)]),
    ([1, 2, 4], [(1, 2), (4, 4)]),
    ([1, 2, 3], [(1, 3)]),
    ([-1, 0, 1, 4, 6, 7, 8, 9], [(-1, 1), (4, 4), (6, 9)]),
    ([1, 2, 3, 10, 21, 22, 24], [(1, 3), (10, 10), (21, 22), (24, 24)]),
]
@pytest.mark.parametrize('input_list, expected_result_list', RANGE_TEST_DATA)
def test_range_data_convertion(input_list, expected_result_list):
    result_list = convert_int_list_to_range_lists(input_list)

    assert result_list == expected_result_list

RANGE_TEST_DATA_UNSORTED = [
    ([1, 4, 2], [(1, 1), (4, 4), (2, 2)]),
    ([1, 4, 5, 6, 2], [(1, 1), (4, 6), (2, 2)]),
]
@pytest.mark.parametrize('input_list, expected_result_list', RANGE_TEST_DATA_UNSORTED)
def test_range_data_convertion_unsorted(input_list, expected_result_list):
    result_list = convert_int_list_to_range_lists(input_list, sort_list=False)

    assert result_list == expected_result_list




def test_large_number_range_convertion():

    rand_list = [random.randint(0, 1000000) for x in range(10000)]
    print('len(rand_list)', len(rand_list))

    result_list = convert_int_list_to_range_lists(rand_list)
    print('len(result_list)', len(result_list))

    num_covers = 0
    for entry in result_list:
        num_covers += entry[1] - entry[0] + 1

    assert num_covers == len(rand_list)


RANGE_SORT_TEST_DATA = [
    ([], [], True),
    ([(1, 2)], [(1, 2)], True),
    ([(1, 2)], [(1, 2)], False),
    ([(1, 2), (4, 8)], [(4, 8), (1, 2)], True),
    ([(1, 2), (4, 8)], [(1, 2), (4, 8)], False),
    ([(4, 8), (1, 2)], [(4, 8), (1, 2)], True),
    ([(4, 8), (1, 2)], [(1, 2), (4, 8)], False),
    ([(2, 1), (8, 4)], [(8, 4), (2, 1)], True),
    ([(1, 3), (5, 5), (7, 8)], [(1, 3), (7, 8), (5, 5)], True),
]
@pytest.mark.parametrize('unsorted_range_list, sorted_range_list, descending', RANGE_SORT_TEST_DATA)
def test_sort_range_list(unsorted_range_list, sorted_range_list, descending):
    result_list = sort_range_list(unsorted_range_list, descending=descending)

    assert result_list == sorted_range_list


def test_large_number_range_sorting():
    test_list = [(1, random.randint(1, 100000)) for x in range(100000)]
    print('len(TEST_LIST)', len(test_list))
    result_list = sort_range_list(test_list, descending=False)
    print('len(result_list)', len(result_list))
    print('len(result_list)', result_list[0:3], '...', result_list[-3:])


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
            mock_method.side_effect = (OperationalError(), None)
            qs = filter_qs_by_pk_list(Delivery.objects.all(), test_list)
            self.assertEqual(len(qs), 1)

class TestFilteringWithRangeConvertion(TestCase):
    def setUp(self):
        Delivery.objects.create(pk=0, address='')
        Delivery.objects.create(pk=3, address='')
        Delivery.objects.create(pk=5, address='')
        Delivery.objects.create(pk=6, address='')
        Delivery.objects.create(pk=7, address='')
        Delivery.objects.create(pk=9, address='')
        Delivery.objects.create(pk=10, address='')
        Delivery.objects.create(pk=20, address='')
        Delivery.objects.create(pk=30, address='')

        self.pk_list = [deliv.pk for deliv in Delivery.objects.all()]

    @patch('django_property_filter.utils.get_max_params_for_db')
    def test_filtering_with_range_convertion_single_item(self, mock_max_params):
        mock_max_params.return_value = 1

        with patch.object(QuerySet, 'count') as mock_method:
            mock_method.side_effect = (OperationalError(), None)
            result_qs = filter_qs_by_pk_list(Delivery.objects.all(), self.pk_list)
            assert list(result_qs.values_list('pk', flat=True)) == [5]  # First item of longest range

    @patch('django_property_filter.utils.get_max_params_for_db')
    def test_filtering_with_range_convertion_single_range(self, mock_max_params):
        mock_max_params.return_value = 2

        with patch.object(QuerySet, 'count') as mock_method:
            mock_method.side_effect = (OperationalError(), None)
            result_qs = filter_qs_by_pk_list(Delivery.objects.all(), self.pk_list)
            assert set(result_qs.values_list('pk', flat=True)) == set([5, 6, 7])  # Longest Range

    @patch('django_property_filter.utils.get_max_params_for_db')
    def test_filtering_with_range_convertion_split_range(self, mock_max_params):
        mock_max_params.return_value = 4

        with patch.object(QuerySet, 'count') as mock_method:
            mock_method.side_effect = (OperationalError(), None)
            result_qs = filter_qs_by_pk_list(Delivery.objects.all(), self.pk_list)
            assert set(result_qs.values_list('pk', flat=True)) == set([5, 6, 7, 9, 10])

    @patch('django_property_filter.utils.get_max_params_for_db')
    def test_filtering_with_range_convertion_inside_range(self, mock_max_params):
        mock_max_params.return_value = 5

        with patch.object(QuerySet, 'count') as mock_method:
            mock_method.side_effect = (OperationalError(), None)
            result_qs = filter_qs_by_pk_list(Delivery.objects.all(), self.pk_list)

            assert len(result_qs) == 6  # 2 Ranges (4 params, 5 values) + 1 single values
            assert set([5, 6, 7, 9, 10]).issubset(set(result_qs.values_list('pk', flat=True)))  # First 5 items from 2 ranges


class TestFilteringAndOrdering(TestCase):
    def setUp(self):
        Delivery.objects.create(pk=1, address='A')
        Delivery.objects.create(pk=2, address='B')
        Delivery.objects.create(pk=3, address='C')
        Delivery.objects.create(pk=4, address='D')

    def test_keep_order_full_qs_no_filtering(self):
        result_qs = filter_qs_by_pk_list(Delivery.objects.all(), [1, 2, 3, 4], preserve_order=[3, 1, 4, 2])
        assert list(result_qs.values_list('pk', flat=True)) == [3, 1, 4, 2]

    def test_keep_order_with_filtering(self):
        result_qs = filter_qs_by_pk_list(Delivery.objects.all(), [3, 2, 4], preserve_order=[3, 1, 4, 2])
        assert list(result_qs.values_list('pk', flat=True)) == [3, 4, 2]


VOLUME_TEST_MAX = 10000
class VolumeTestQsFilteringByPkList(TestCase):

    def setUp(self):
        bulk_list = []

        with transaction.atomic():
            for _ in range(1, VOLUME_TEST_MAX + 1):
                bulk_list.append(Delivery(address='My Home'))
            Delivery.objects.bulk_create(bulk_list)

        self.pk_list = list(Delivery.objects.all().values_list('pk', flat=True))

    def test_volume_filtering_non_sqlite(self):
        result_qs = filter_qs_by_pk_list(Delivery.objects.all(), self.pk_list)
        self.assertEqual(result_qs.count(), VOLUME_TEST_MAX)

        self.assertEqual(
            set(result_qs.values_list('pk', flat=True)),
            set(Delivery.objects.all().values_list('pk', flat=True)),
        )
