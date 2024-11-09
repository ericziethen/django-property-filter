#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

#########################################
##### START OF FUNCTION DEFINITIONS #####
#########################################
run_ruff () {
    local lint_path=$1

    echo "### RUFF START - '$lint_path' ###"
    ruff check "$lint_path"
    local return_code=$?

    if [[ $return_code -eq  0 ]];
    then
        echo "   No Issues"
    else
        echo "   Issues Found"
        ERROR_FOUND="true"
        ERROR_LIST+=" $lint_path"
    fi
    echo "### RUFF END - '$lint_path' ###"
}
#######################################
##### END OF FUNCTION DEFINITIONS #####
#######################################

MODULE_NAME=django_property_filter
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_MAIN_DIR=$SCRIPT_PATH/../..
MODULE_PATH=$PROJ_MAIN_DIR/$MODULE_NAME

echo SCRIPT_PATH: $SCRIPT_PATH
echo PROJ_MAIN_DIR: $PROJ_MAIN_DIR
echo MODULE_PATH: $MODULE_PATH

ERROR_FOUND="false"
ERROR_LIST=''

export PYTHONPATH=$PYTHONPATH:$MODULE_PATH

run_ruff "$MODULE_PATH"

echo "ERROR_FOUND: '$ERROR_FOUND'"
if [ $ERROR_FOUND == "false" ];
then
    echo "exit 0"
    exit 0
else
    for value in $ERROR_LIST
    do
        echo "  - $value"
    done
    echo "exit 1"
    exit 1
fi
