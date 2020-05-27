

import pytest
from django.test import TestCase

from django_filters.filters import NumberFilter

from django_property_filter.filters import PropertyNumberFilter

from tests.common import (
    get_django_filter_test_filterset,
    get_django_property_filter_test_filterset
)
from tests.models import NumberClass, Delivery

counter = 0

def db_setup():
    Delivery.objects.create(address='Hi')

@pytest.mark.django_db
def test_create_deliv1():
    db_setup()
    assert Delivery.objects.all().count() == 1

    global counter
    counter += 1
    assert counter == 1


@pytest.mark.django_db
def test_create_deliv2():
    db_setup()
    assert Delivery.objects.all().count() == 1

    global counter
    counter += 1
    assert counter == 2


@pytest.fixture
def fixture_eric():
    Delivery.objects.create(address='Hi')
    Delivery.objects.create(address='You')

@pytest.mark.django_db
def test_eric(fixture_eric):
    assert Delivery.objects.all().count() == 2

@pytest.mark.django_db
def test_eric2(fixture_eric):
    assert Delivery.objects.all().count() == 2

'''
@pytest.fixture
def fixture_eric111():
    Delivery.objects.create(address='Hi')
    Delivery.objects.create(address='You')

ERIC2 = [1, 2]
@pytest.mark.parametrize('number', ERIC2)
@pytest.mark.django_db
def test_test_this(fixture_eric111, number):
    assert Delivery.objects.all().count() == 2
    assert number == 3
'''
'''
class EricTest(PropertyTestMixin, TestCase):
    def setUp(self):
        Delivery.objects.create(address='Hi')

    def test_1(self):
        assert Delivery.objects.all().count() == 1
        self.lookups_tested.append('exact')
        assert len(self.lookups_tested) == 1

    def test_2(self):
        assert Delivery.objects.all().count() == 1
        self.lookups_tested.append('iexact')
        assert len(self.lookups_tested) == 2
'''





'''
ERIC = [
    (1,2,5),
    (1,2,3),
    (1,2,4),
]
@pytest.mark.parametrize('num1, num2, result', ERIC)
def test_eric_sum(num1, num2, result):
    assert num1 + num2 == result
'''



MY_LOOKUPS = [
    'exact',
    'iexact',
    'contains',
    'icontains',
    'in',
    'gt',
    'gte',
    'lt',
    'lte',
    'startswith',
    'istartswith',
    'endswith',
    'iendswith',
    'range',
    #'isnull',
]
'''
class NANTestLookupExpressions(PropertyTestMixin):
#class TestLookupExpressions():
    lookups_tested = []
    @pytest.mark.parametrize('xpr', MY_LOOKUPS)
    def test_lookup(self, xpr):
        self.lookups_tested.append(xpr)
        print(self.lookups_tested)
        assert True
'''


class LookupExpressionTests(TestCase):

    def setUp(self):
        NumberClass.objects.create(number=1)
        NumberClass.objects.create(number=2)
        NumberClass.objects.create(number=3)
        NumberClass.objects.create(number=4)
        NumberClass.objects.create(number=5)
    '''
    def test_exact(self):
        filter_fs = get_django_filter_test_filterset(
            filter_class=NumberFilter, filter_model=Product, field_name='name', lookup_expr='exact')
    '''

        # TODO - CONTINUE TEST









@pytest.fixture
def fixture_property_number_filter():
    NumberClass.objects.create(id=1, number=1)
    NumberClass.objects.create(id=2, number=2)
    NumberClass.objects.create(id=3, number=2)
    NumberClass.objects.create(id=4, number=2)
    NumberClass.objects.create(id=5, number=3)
    NumberClass.objects.create(id=6, number=4)
    NumberClass.objects.create(id=7, number=4)
    NumberClass.objects.create(id=8, number=5)
    NumberClass.objects.create(id=9, number=5)
    NumberClass.objects.create(id=10, number=5)
    NumberClass.objects.create(id=11, number=5)
    NumberClass.objects.create(id=12, number=10)
    NumberClass.objects.create(id=13, number=20)

TEST_LOOKUPS = [
    ('exact', 5, [8, 9, 10, 11]),
    #('iexact', , []),
    #('contains', , []),
    #('icontains', , []),
    #('in', , []),
    #('gt', , []),
    #('gte', , []),
    #('lt', , []),
    #'lte', , []),
    #'startswith', , []),
    #('istartswith', , []),
    #('endswith', , []),
    #('iendswith', , []),
    #('range', , []),
    #('isnull', , []),
]


from django_filters import FilterSet
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_number_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    fs_class = get_django_filter_test_filterset(
        filter_class=NumberFilter, filter_model=NumberClass, field_name='number', lookup_expr=lookup_xpr)
    filter_fs = fs_class({'number': lookup_val}, queryset=NumberClass.objects.all())

    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Property Filter
    prop_fs_class = get_django_property_filter_test_filterset(
        filter_class=PropertyNumberFilter, filter_model=NumberClass, property_field='prop_number', lookup_expr=lookup_xpr)
    prop_filter_fs = prop_fs_class({'number': lookup_val}, queryset=NumberClass.objects.all())

    assert set(prop_filter_fs.qs) == set(filter_fs.qs)





def test_all_expressions_tested():
    assert True




### TODO TODO - CAN WE PARAMETRIZE ALL LOOKUPS WITH PYTEST AND A LARGE SET OF NUMBERS ?



# TODO - TEST Number Filter

# TODO - Automate to test all supported filter methods (from conf.py)

# TODO - Ensure all Expressions are Tested e.g. multiple lists, parametrize