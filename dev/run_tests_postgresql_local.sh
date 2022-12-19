#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo SCRIPT_PATH: $SCRIPT_PATH

. "$SCRIPT_PATH/run_tests.sh" postgres-local
