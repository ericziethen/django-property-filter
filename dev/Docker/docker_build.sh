#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

docker-compose build --no-cache
