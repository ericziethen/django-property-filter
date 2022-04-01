#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

PACKAGE_ROOT=django_property_filter
DJANGO_TEST_PROJ_ROOT=tests/django_test_proj
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_MAIN_DIR=$SCRIPT_PATH/../..
pushd "$PROJ_MAIN_DIR"

echo SCRIPT_PATH: $SCRIPT_PATH
echo PROJ_MAIN_DIR: $PROJ_MAIN_DIR
echo PACKAGE_ROOT: $PACKAGE_ROOT
echo DJANGO_TEST_PROJ_ROOT: $DJANGO_TEST_PROJ_ROOT

export PYTHONPATH=$PYTHONPATH:$PACKAGE_ROOT:$DJANGO_TEST_PROJ_ROOT

# Can use to overwrite pytest.ini
# set PYTEST_ADDOPTS=""

echo PYTHONPATH: "$PYTHONPATH"

# Test directories are specified in Pytest.ini
pytest --cov="$PACKAGE_ROOT" $ENV_PYTEST_EXTRA_ARGS
return_code=$?

if [[ $return_code -eq  0 ]];
then
    echo "*** No Issues Found"
else
    echo "*** Some Issues Found"
fi

popd
echo "exit $return_code"
exit $return_code
