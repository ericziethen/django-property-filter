#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

pip-audit --desc --strict
