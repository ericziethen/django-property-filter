#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

docker-compose down --volumes
docker-compose up --remove-orphans --renew-anon-volumes
