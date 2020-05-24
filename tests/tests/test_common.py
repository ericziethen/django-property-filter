
from django.test import TestCase

from django_filters.filters import NumberFilter

from tests.common import (
    class_functions_diff_dic,
    get_django_filter_test_filterset
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




# TODO - Implement Tests for Filterset Generators to ensure the function generator works

class FiltersetGeneratorTests(TestCase):

    def test_get_valid_django_filter(self):
        filterset = get_django_filter_test_filterset(NumberFilter, Product, 'name', 'gte')

        my_filter = list(filterset.base_filters.values())[0]
        self.assertEqual(len(filterset.base_filters), 1)
        self.assertEqual(type(my_filter), NumberFilter)
        self.assertEqual(my_filter.field_name, 'name')
        self.assertEqual(my_filter.lookup_expr, 'gte')

        f1 = filterset({'name': 'Tom'}, queryset=Product.objects.all())
        fs_options = f1._meta
        self.assertEqual(fs_options.model, Product)


class PropertyFiltersetGeneratorTests(TestCase):
    pass

'''
def test_get_valid_django_filter(Class, Expression, query_field)

def test_get_valid_django_filter_propert(Class, Expression, query_field)
'''



