
import pytest

from django.test import TestCase

from django_property_filter.utils import (
    get_value_for_db_field,
    compare_by_lookup_expression
)

from tests.django_test_proj.property_filter.models import (
    Delivery,
    DeliveryLine,
    Product
)


class GetAttributeTests(TestCase):

    def setUp(self):
        self.delivery1 = Delivery.objects.create(address='My Home')
        self.line1 = DeliveryLine.objects.create(line_no=1, delivery=self.delivery1)
        self.prod1 = Product.objects.create(name='Sun Rice', price='20.0', del_line=self.line1)

    def test_get_attribute_1_level(self):
        self.assertEqual(get_value_for_db_field(self.prod1, 'name'), 'Sun Rice')
        self.assertEqual(get_value_for_db_field(self.prod1, 'prop_name'), 'Sun Rice')

    def test_get_attribute_2_level(self):
        self.assertEqual(get_value_for_db_field(self.prod1, 'del_line.line_no'), 1)
        self.assertEqual(get_value_for_db_field(self.prod1, 'del_line.prop_line_no'), 1)

    def test_get_attribute_3_level(self):
        self.assertEqual(get_value_for_db_field(self.prod1, 'del_line.delivery.address'), 'My Home')
        self.assertEqual(get_value_for_db_field(self.prod1, 'del_line.delivery.prop_address'), 'My Home')

    def test_get_attribute_invalid_object(self):
        self.assertRaises(AttributeError, get_value_for_db_field, 'None', 'id')

    def test_get_attribute_invalid_field(self):
        self.assertRaises(AttributeError, get_value_for_db_field, self.prod1, 'invalid_field')

    def test_get_attribute_invalid_related_field(self):
        self.assertRaises(AttributeError, get_value_for_db_field, self.prod1, 'del_line.delivery.invalid_field')


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
    ('isnull', None, None),
    ('range', (3, 7), 3),
    ('range', (3, 7), 5),
    ('range', (3, 7), 7),
    ('range', (3, None), 3),
    ('range', (2.9, None), 3),
    ('range', (None, 7), 7),
    ('range', (None, 7.1), 7),
    ('in', [1, 3, 5], 1),
    ('in', [1, 3, 5], 3),
    ('in', [1, 3, 5], 5),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val, compare_val', LOOKUP_SUCCEED)
def test_compare_by_lookup_expression_succeed(lookup_xpr, lookup_val, compare_val):
    assert compare_by_lookup_expression(lookup_xpr, lookup_val, compare_val)


LOOKUP_FAILED = [
    ('exact', 5, 6),
    ('exact', 'a', 'A'),
    ('iexact', 'a', 'A '),
    ('contains', 1234, 12),
    ('contains', 'Hello', 'ell'),
    ('contains', 'Ell', 'Hello'),
    ('icontains', 'Elo', 'Hello'),
    ('gt', 5, 5.00000),
    ('gte', 5, 4.999999),
    ('lt', 5, 6),
    ('lt', 5.0, 5),
    ('lte', 5.000000, 5.000001),
    ('startswith', ' Hel', 'Hello'),
    ('startswith', 'ello', 'Hello'),
    ('startswith', 'hello', 'Hello'),
    ('istartswith', ' hello', 'Hello'),
    ('endswith', 'Hell', 'Hello'),
    ('endswith', 'hello', 'Hello'),
    ('iendswith', 'hell', 'Hello'),
    ('isnull', 'a', None),
    ('isnull', ' ', None),
    ('isnull', [''], None),
    ('isnull', 0, None),
    ('range', (3, 7), 2.9),
    ('range', (3, 7), 7.1),
    ('range', (3, None), 2.9),
    ('range', (None, 7), 7.1),
    ('in', [1, 3, 5], 4),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val, compare_val', LOOKUP_FAILED)
def test_compare_by_lookup_expression_fail(lookup_xpr, lookup_val, compare_val):
    assert not compare_by_lookup_expression(lookup_xpr, lookup_val, compare_val)
