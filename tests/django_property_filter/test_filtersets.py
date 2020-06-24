
import pytest

from django_property_filter import PropertyFilterSet, PropertyNumberFilter

from property_filter.models import (
    Product,
    NumberClass
)


def test_declare_implicit_filter():
    class Fs(PropertyFilterSet):

        class Meta:
            model = NumberClass
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, ['gte', 'exact'])]

    fs = Fs({'prop_number': 5}, queryset=NumberClass.objects.all())

    assert len(fs.filters) == 2
    assert 'prop_number__gte' in fs.filters
    assert fs.filters['prop_number__gte'].lookup_expr == 'gte'

    assert 'prop_number__exact' in fs.filters
    assert fs.filters['prop_number__exact'].lookup_expr == 'exact'


def test_declare_implicit_filter_multiple_properties():
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

    assert 'prop_line_no__exact' in fs.filters
    assert fs.filters['prop_line_no__exact'].lookup_expr == 'exact'

def test_invalid_implicit_class():
    class Fs(PropertyFilterSet):

        class Meta:
            model = NumberClass
            exclude = ['number']
            property_fields = [('prop_number', NumberClass, ['gte'])]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=NumberClass.objects.all())

def test_invalid_implicit_field_name():
    class Fs(PropertyFilterSet):

        class Meta:
            model = NumberClass
            exclude = ['number']
            property_fields = [(None, PropertyNumberFilter, ['gte'])]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=NumberClass.objects.all())

def test_invalid_implicit_lookup_empty_list():
    class Fs(PropertyFilterSet):

        class Meta:
            model = NumberClass
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, [])]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=NumberClass.objects.all())

def test_invalid_implicit_lookup_invalid_list():
    class Fs(PropertyFilterSet):

        class Meta:
            model = NumberClass
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, None)]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=NumberClass.objects.all())
