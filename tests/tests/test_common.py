
from django.test import TestCase

from django_filters.filters import NumberFilter

from django_property_filter.filters import PropertyNumberFilter

from tests.common import (
    class_functions_diff_dic,
    get_django_filter_test_filterset,
    get_django_property_filter_test_filterset
)

from tests.models import (
    Product
)


class ClassComparisonTests(TestCase):

    def test_same_class_matching(self):
        class Test():
            def name(self):
                return 'Test'

        self.assertEqual(class_functions_diff_dic(Test, Test), {})

    def test_sub_class_matching(self):
        class Test():
            def name(self):
                return 'Test'

        class SubTest(Test):
            var = 'Me'

        self.assertEqual(class_functions_diff_dic(Test, SubTest), {})

    def test_different_class_not_matching(self):
        class Test():
            def name(self):
                return 'Test'

        class Test2():
            def name(self):
                return 'Test'

        self.assertNotEqual(class_functions_diff_dic(Test, Test2), {})

    def test_sub_class_not_matching(self):
        class Test():
            def name(self):
                return 'Test'

        class SubTest(Test):
            def name(self):
                return 'Test'

        self.assertNotEqual(class_functions_diff_dic(Test, SubTest), {})

    def test_sub_class_different_but_allow_ignore(self):
        class Test():
            def name(self):
                return 'Test'

        class SubTest(Test):
            def name(self):
                return 'Test'

        self.assertEqual(class_functions_diff_dic(Test, SubTest, ignore=['name']), {})


class FiltersetGeneratorTests(TestCase):

    def test_get_valid_django_filterset(self):
        filterset = get_django_filter_test_filterset(
            filter_class=NumberFilter, filter_model=Product, field_name='name', lookup_expr='gte')

        my_filter = list(filterset.base_filters.values())[0]
        self.assertEqual(len(filterset.base_filters), 1)
        self.assertEqual(type(my_filter), NumberFilter)
        self.assertEqual(my_filter.field_name, 'name')
        self.assertEqual(my_filter.lookup_expr, 'gte')

        f1 = filterset({'name': 'Tom'}, queryset=Product.objects.all())
        fs_options = f1._meta
        self.assertEqual(fs_options.model, Product)


class PropertyFiltersetGeneratorTests(TestCase):

    def test_get_valid_django_property_filterset(self):
        filterset = get_django_property_filter_test_filterset(
            filter_class=PropertyNumberFilter, filter_model=Product, property_field='name.field', lookup_expr='lte')

        my_filter = list(filterset.base_filters.values())[0]
        self.assertEqual(len(filterset.base_filters), 1)
        self.assertEqual(type(my_filter), PropertyNumberFilter)
        self.assertEqual(my_filter.property_fld_name, 'name.field')
        self.assertEqual(my_filter.lookup_expr, 'lte')

        f1 = filterset({'name': 'Tom'}, queryset=Product.objects.all())
        fs_options = f1._meta
        self.assertEqual(fs_options.model, Product)
