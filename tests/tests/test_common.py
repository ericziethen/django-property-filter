
from django.test import TestCase

from tests.common import class_functions_diff_dic


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


# TODO - Implement Tests for Filterset Generators to ensure the function generator works





'''
def test_get_valid_django_filter(Class, Expression)

def test_get_valid_django_filter_propert(Class, Expression)
'''



