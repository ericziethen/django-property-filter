#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

MODULE_NAME=django_property_filter
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_MAIN_DIR=$SCRIPT_PATH/../..
MODULE_PATH=$MODULE_NAME

pushd "$PROJ_MAIN_DIR"
echo SCRIPT_PATH: $SCRIPT_PATH
echo PROJ_MAIN_DIR: $PROJ_MAIN_DIR
echo MODULE_PATH: $MODULE_PATH

bandit -r "$MODULE_PATH"
return_code=$?

if [[ $return_code -eq  0 ]];
then
    echo "*** No Issues Found"
else
    echo "*** Some Issues Found"
fi

popd
exit $return_code
