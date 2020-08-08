#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

MODULE_NAME=django_property_filter
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_MAIN_DIR=$SCRIPT_PATH/..
MODULE_PATH=$PROJ_MAIN_DIR/$MODULE_NAME
DJANGO_DIR=$PROJ_MAIN_DIR/tests/django_test_proj

echo SCRIPT_PATH: $SCRIPT_PATH
echo PROJ_MAIN_DIR: $PROJ_MAIN_DIR
echo MODULE_PATH: $MODULE_PATH
echo DJANGO_DIR: $DJANGO_DIR

export PYTHONPATH=$PYTHONPATH:$MODULE_PATH

python "$DJANGO_DIR/manage.py" migrate --fake
return_code=$?

if [[ $return_code -eq  0 ]];
then
    echo "*** No Django Issues Found"
else
    echo "*** Some Django Issues Found"
fi

exit $return_code
