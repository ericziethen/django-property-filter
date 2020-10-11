#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

safety check --full-report
