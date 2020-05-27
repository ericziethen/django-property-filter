
from django.test import TestCase

from django_property_filter.utils import (
    get_value_for_db_field,
    compare_by_lookup_expression
)

from tests.models import (
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


def test_compare_by_lookup_expression():
    # TODO - Test All Expressions, Parametrized, compare_by_lookup_expression
    assert False


# TODO - Test PropertyBaseFilterMixin
