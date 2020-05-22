
from django.test import TestCase

from django_property_filter.utils import (
    get_attr_val_recursive
)

from tests.models import (
    Product,
)


class GerAttributeTests(TestCase):

    def setUp(self):
        self.prod1 = Product.objects.create(name='Sun Rice', price='20.0')


    def test_get_attribute_1_level(self):
        self.assertEqual(get_attr_val_recursive(self.prod1, ['name']), 'Sun Rice')

    '''
    def test_get_attribute_2_level(self):
        assert False

    def test_get_attribute_3_level(self):
        assert False

    def test_get_attribute_field_value(self):
        assert False

    def test_get_attribute_property_value(self):
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


