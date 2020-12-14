
import pytest

from tests.common import is_ci_build


def pytest_collection_modifyitems(items):
    for item in items:
        skip_ci = item.get_closest_marker('skiptravis')

        # Don't count in coverage even when running to not be surprised later
        if skip_ci:
            item.add_marker(pytest.mark.no_cover)

            # Skip if run on CI
            if is_ci_build():
                print(F'Skip {item} because is CI Build')
                item.add_marker(pytest.mark.skip)
