#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

python setup.py sdist bdist_wheel
