
import pytest

from django_filters.conf import DEFAULTS as django_filters_DEFAULTS

from django_filter_property.conf import SUPPORTED_LOOKUPS

@pytest.mark.parametrize('lookup', SUPPORTED_LOOKUPS)
def test_all_supported_expressions_in_django_filter(lookup):
    assert lookup in django_filters_DEFAULTS['VERBOSE_LOOKUPS']
