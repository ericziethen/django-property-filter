
import pytest

from django_filters.conf import DEFAULTS as django_filters_DEFAULTS

from django_property_filter.conf import SUPPORTED_LOOKUPS

pytest.global_variable_1 = 100

@pytest.mark.parametrize('lookup', SUPPORTED_LOOKUPS)
def test_all_supported_expressions_in_django_filter(lookup):
    pytest.global_variable_1 += 1
    assert lookup in django_filters_DEFAULTS['VERBOSE_LOOKUPS']
