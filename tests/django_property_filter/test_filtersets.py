
import pytest

from django.test import TestCase

from django_property_filter import (
    PropertyFilterSet,
    PropertyChoiceFilter,
    PropertyNumberFilter,
)

from django_filters import FilterSet

from property_filter.models import (
    DoubleIntModel,
    Product,
    RangeFilterModel
)


def test_declare_implicit_filter_normal_fs_no_filters():
    class Fs(FilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, ['gte', 'exact'])]

    fs = Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

    assert len(fs.filters) == 0


def test_declare_explicit_filter_normal_fs():
    class Fs(FilterSet):

        prop_number = PropertyNumberFilter(field_name='prop_number', lookup_expr='exact')

        class Meta:
            model = RangeFilterModel
            exclude = ['number']

    fs = Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

    assert len(fs.filters) == 1
    assert fs.filters['prop_number'].model == RangeFilterModel
    assert fs.filters['prop_number'].parent == fs


def test_declare_implicit_filter_property_fs():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, ['gte', 'exact'])]

    fs = Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

    assert len(fs.filters) == 2
    assert 'prop_number__gte' in fs.filters
    assert fs.filters['prop_number__gte'].lookup_expr == 'gte'
    assert fs.filters['prop_number__gte'].model == RangeFilterModel
    assert fs.filters['prop_number__gte'].parent == fs

    assert 'prop_number__exact' in fs.filters
    assert fs.filters['prop_number__exact'].lookup_expr == 'exact'
    assert fs.filters['prop_number__exact'].model == RangeFilterModel
    assert fs.filters['prop_number__exact'].parent == fs


def test_declare_explicit_filter_property_fs():
    class Fs(PropertyFilterSet):

        prop_number = PropertyNumberFilter(field_name='prop_number', lookup_expr='exact')

        class Meta:
            model = RangeFilterModel
            exclude = ['number']

    fs = Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

    assert len(fs.filters) == 1
    assert fs.filters['prop_number'].model == RangeFilterModel
    assert fs.filters['prop_number'].parent == fs


def test_declare_implicit_filter_multiple_properties_property_fs():
    class Fs(PropertyFilterSet):

        class Meta:
            model = Product
            exclude = ['name', 'price', 'del_line']
            property_fields = [
                ('prop_name', PropertyNumberFilter, ['gte']),
                ('prop_line_no', PropertyNumberFilter, ['exact'])
                ]

    fs = Fs({'prop_name': 5}, queryset=Product.objects.all())

    assert len(fs.filters) == 2
    assert 'prop_name__gte' in fs.filters
    assert fs.filters['prop_name__gte'].lookup_expr == 'gte'
    assert fs.filters['prop_name__gte'].model == Product
    assert fs.filters['prop_name__gte'].parent == fs

    assert 'prop_line_no__exact' in fs.filters
    assert fs.filters['prop_line_no__exact'].lookup_expr == 'exact'
    assert fs.filters['prop_line_no__exact'].model == Product
    assert fs.filters['prop_line_no__exact'].parent == fs


def test_invalid_implicit_class():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', RangeFilterModel, ['gte'])]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

def test_invalid_implicit_field_name():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [(None, PropertyNumberFilter, ['gte'])]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

def test_invalid_implicit_lookup_empty_list():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, [])]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

def test_invalid_implicit_lookup_invalid_list():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, None)]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

def test_disallowed_implicid_filter_created():

    class Fs(PropertyFilterSet):

        class Meta:
            model = Product
            exclude = ['name', 'price', 'del_line']
            property_fields = [
                ('prop_name', PropertyChoiceFilter, ['exact'])
                ]

    with pytest.raises(ValueError):
        Fs({'prop_name': '5'}, queryset=Product.objects.all())






from unittest import mock
from django_property_filter import compare_by_lookup_expression
class FilterOrderTests(TestCase):

    def setUp(self):
        DoubleIntModel.objects.create(id=0, age=30, number=1)
        DoubleIntModel.objects.create(id=1, age=30, number=1)
        DoubleIntModel.objects.create(id=2, age=20, number=1)
        DoubleIntModel.objects.create(id=3, age=20, number=1)
        DoubleIntModel.objects.create(id=4, age=20, number=1)
        DoubleIntModel.objects.create(id=5, age=20, number=1)
        DoubleIntModel.objects.create(id=6, age=20, number=1)
        DoubleIntModel.objects.create(id=7, age=20, number=1)
        DoubleIntModel.objects.create(id=8, age=20, number=2)
        DoubleIntModel.objects.create(id=9, age=20, number=2)

    def test_filter_order_explicit_declaration(self):
        class MyPropertyFilterset(PropertyFilterSet):
            prop_number = PropertyNumberFilter(field_name='prop_number', lookup_expr='exact')
            prop_age = PropertyNumberFilter(field_name='prop_age', lookup_expr='exact')

            class Meta:
                model = DoubleIntModel
                exclude = ['age', 'number']
                fields = ['prop_age', 'prop_number']  # Order of filtering

        fs = MyPropertyFilterset({'prop_age': 20, 'prop_number': 2}, queryset=DoubleIntModel.objects.all())

        with mock.patch('django_property_filter.filters.compare_by_lookup_expression', side_effect=compare_by_lookup_expression) as mock_func:
            query_set = fs.qs

            # 1.) Filter for 'prop_age:20', -> Going 10 times into compare_by_lookup_expression, 8 results
            # 2.) Filter for 'prop_number:2',    -> Going 8 times into compare_by_lookup_expression, 2 results
            #        -> 2 results and 18 x function execution

            assert query_set.count() == 2
            assert mock_func.call_count == 18

    def test_filter_order_implicit_declaration(self):
        class MyPropertyFilterset(PropertyFilterSet):

            class Meta:
                model = DoubleIntModel
                exclude = ['age', 'number']
                # fields = ['prop_age', 'prop_number']  # Order of filtering
                property_fields = [
                    ('prop_age', PropertyNumberFilter, ['exact']),
                    ('prop_number', PropertyNumberFilter, ['exact']),
                    ]


        fs = MyPropertyFilterset({'prop_age__exact': 20, 'prop_number__exact': 2}, queryset=DoubleIntModel.objects.all())

        with mock.patch('django_property_filter.filters.compare_by_lookup_expression', side_effect=compare_by_lookup_expression) as mock_func:
            query_set = fs.qs

            # 1.) Filter for 'prop_age:20', -> Going 10 times into compare_by_lookup_expression, 8 results
            # 2.) Filter for 'prop_number:2',    -> Going 8 times into compare_by_lookup_expression, 2 results
            #        -> 2 results and 18 x function execution

            assert query_set.count() == 2
            assert mock_func.call_count == 18

    def test_reverse_filter_order_explicit_declaration(self):

        class MyPropertyFilterset(PropertyFilterSet):
            prop_number = PropertyNumberFilter(field_name='prop_number', lookup_expr='exact')
            prop_age = PropertyNumberFilter(field_name='prop_age', lookup_expr='exact')

            class Meta:
                model = DoubleIntModel
                exclude = ['age', 'number']
                fields = ['prop_number', 'prop_age']  # Order of filtering

        fs = MyPropertyFilterset({'prop_age': 20, 'prop_number': 2}, queryset=DoubleIntModel.objects.all())

        with mock.patch('django_property_filter.filters.compare_by_lookup_expression', side_effect=compare_by_lookup_expression) as mock_func:
            query_set = fs.qs

            # 1.) Filter for 'prop_number:2',    -> Going 10 times into compare_by_lookup_expression, 2 results
            # 2.) Filter for 'prop_age:20', -> Going 2 times into compare_by_lookup_expression, 2 results
            #    -> 2 results and 12 x function execution

            assert query_set.count() == 2
            assert mock_func.call_count == 12

    def test_filter_reverse_order_implicit_declaration(self):
        class MyPropertyFilterset(PropertyFilterSet):

            class Meta:
                model = DoubleIntModel
                exclude = ['age', 'number']
                # fields = ['prop_age', 'prop_number']  # Order of filtering
                property_fields = [
                    ('prop_number', PropertyNumberFilter, ['exact']),
                    ('prop_age', PropertyNumberFilter, ['exact']),
                    ]


        fs = MyPropertyFilterset({'prop_age__exact': 20, 'prop_number__exact': 2}, queryset=DoubleIntModel.objects.all())

        with mock.patch('django_property_filter.filters.compare_by_lookup_expression', side_effect=compare_by_lookup_expression) as mock_func:
            query_set = fs.qs

            # 1.) Filter for 'prop_age:20', -> Going 10 times into compare_by_lookup_expression, 8 results
            # 2.) Filter for 'prop_number:2',    -> Going 8 times into compare_by_lookup_expression, 2 results
            #        -> 2 results and 18 x function execution

            assert query_set.count() == 2
            assert mock_func.call_count == 12
