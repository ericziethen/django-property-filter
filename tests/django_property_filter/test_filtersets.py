
from django_property_filter import PropertyFilterSet, PropertyNumberFilter

from tests.django_test_proj.property_filter.models import NumberClass


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

'''

def test_declare_implicit_filter_multiple_properties():
    assert False

def test_declare_implicit_filter_multiple_expressions():
    assert False

def test_implicit_and_explicit_filters_equal():
    assert False

def test_invalid_explicit_lookup():
    assert False

def test_invalid_implicit_field_name():
    not a string
    assert False

def test_invalid_implicit_lookup():
    invalid type
    empty list
    assert False

def test_invalid_implicit_class():
    not type PropertyFilter
    assert False
'''


