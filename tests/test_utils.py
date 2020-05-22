
from django.test import TestCase

from django_property_filter.utils import (
    get_attr_val_recursive
)

from tests.models import (
    DeliveryLine,
    Product
)


class GerAttributeTests(TestCase):

    def setUp(self):
        self.line1 = DeliveryLine.objects.create(line_no=1)
        self.prod1 = Product.objects.create(name='Sun Rice', price='20.0', del_line=self.line1)

    def test_get_attribute_1_level(self):
        self.assertEqual(get_attr_val_recursive(self.prod1, ['name']), 'Sun Rice')
        self.assertEqual(get_attr_val_recursive(self.prod1, ['prop_name']), 'Sun Rice')

    def test_get_attribute_2_level(self):
        self.assertEqual(get_attr_val_recursive(self.prod1, ['del_line', 'line_no']), 1)
        self.assertEqual(get_attr_val_recursive(self.prod1, ['del_line', 'prop_line_no']), 1)

    '''
    def test_get_attribute_3_level(self):
        assert False

    def test_get_attribute_invalid_object(self):
        assert False

    def test_get_attribute_invalid_field(self):
        assert False

    def test_get_attribute_invalid_related_field(self):
        assert False
    '''





# TODO - Test get_attr_val_recursive
# TODO - Test compare_by_lookup_expression (Test all Supported Ones)

# TODO - Test PropertyBaseFilterMixin


