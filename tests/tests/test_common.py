
from django.test import TestCase

from django_filters.filters import NumberFilter

from django_property_filter.filters import PropertyNumberFilter

from tests.common import class_functions_diff_dic

from property_filter.models import (
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
