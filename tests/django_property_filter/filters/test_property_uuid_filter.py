
import pytest

from django_filters import FilterSet, UUIDFilter

from django_property_filter import PropertyFilterSet, PropertyUUIDFilter

from property_filter.models import UUIDFilterModel


@pytest.mark.parametrize('lookup', PropertyUUIDFilter.supported_lookups)
def test_supported_lookups(lookup):
    # Test expression not raises exception
    PropertyUUIDFilter(field_name='fake_field', lookup_expr=lookup)


def test_unsupported_lookup():
    with pytest.raises(ValueError):
        PropertyUUIDFilter(field_name='fake_field', lookup_expr='fake-lookup')


def test_default_lookup():
    my_filter = PropertyUUIDFilter(field_name='fake_field')
    assert my_filter.lookup_expr == 'exact'


@pytest.fixture
def fixture_property_uuid_filter():
    UUIDFilterModel.objects.create(id=-1, uuid='40828e84-66c7-46ee-a94a-1f2087970a68')
    UUIDFilterModel.objects.create(id=0, uuid='40828e84-66c7-46ee-a94a-1f2087970a68')
    UUIDFilterModel.objects.create(id=1, uuid='df4078eb-67ca-49fe-b86d-742e0feaf3ad')


TEST_LOOKUPS = [
    ('exact', '40828e84-66c7-46ee-a94a-1f2087970a68', [-1, 0]),
    ('exact', 'df4078eb-67ca-49fe-b86d-742e0feaf3ad', [1]),
    ('exact', 'aaaa78eb-67ca-49fe-b86d-742e0feaf3ad', []),
]
@pytest.mark.parametrize('lookup_xpr, lookup_val, result_list', TEST_LOOKUPS)
@pytest.mark.django_db
def test_lookup_xpr(fixture_property_uuid_filter, lookup_xpr, lookup_val, result_list):

    # Test using Normal Django Filter
    class UUIDFilterSet(FilterSet):
        uuid = UUIDFilter(field_name='uuid', lookup_expr=lookup_xpr)

        class Meta:
            model = UUIDFilterModel
            fields = ['uuid']

    filter_fs = UUIDFilterSet({'uuid': lookup_val}, queryset=UUIDFilterModel.objects.all())
    assert set(filter_fs.qs.values_list('id', flat=True)) == set(result_list)

    # Compare with Explicit Filter using a PropertyFilterSet
    class PropertyUUIDFilterSet(PropertyFilterSet):
        uuid = UUIDFilter(field_name='uuid', lookup_expr=lookup_xpr)
        prop_uuid = PropertyUUIDFilter(field_name='prop_uuid', lookup_expr=lookup_xpr)

        class Meta:
            model = UUIDFilterModel
            fields = ['prop_uuid']

    filter_fs_mixed = UUIDFilterSet({'uuid': lookup_val}, queryset=UUIDFilterModel.objects.all())
    prop_filter_fs_mixed = PropertyUUIDFilterSet({'prop_uuid': lookup_val}, queryset=UUIDFilterModel.objects.all())
    assert set(filter_fs_mixed.qs) == set(filter_fs.qs)
    assert set(prop_filter_fs_mixed.qs) == set(filter_fs.qs)

    # Compare with Implicit Filter using PropertyFilterSet
    class ImplicitFilterSet(PropertyFilterSet):

        class Meta:
            model = UUIDFilterModel
            exclude = ['uuid']
            property_fields = [('prop_uuid', PropertyUUIDFilter, [lookup_xpr])]

    implicit_filter_fs = ImplicitFilterSet({F'prop_uuid__{lookup_xpr}': lookup_val}, queryset=UUIDFilterModel.objects.all())
    assert set(implicit_filter_fs.qs) == set(filter_fs.qs)


def test_all_expressions_tested():
    tested_expressions = [x[0] for x in TEST_LOOKUPS]
    assert sorted(list(set(tested_expressions))) == sorted(PropertyUUIDFilter.supported_lookups)
