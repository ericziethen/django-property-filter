#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

docker compose -f docker-compose-postgres-local.yml build
