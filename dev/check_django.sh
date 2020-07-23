#!/bin/bash

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DJANGO_DIR=$SCRIPT_PATH/../tests/django_test_proj

pushd "$DJANGO_DIR"

python manage.py migrate --fake
return_code=$?

if [[ $return_code -eq  0 ]];
then
    echo "*** No Django Issues Found"
else
    echo "*** Some Django Issues Found"
fi

popd
exit $return_code
