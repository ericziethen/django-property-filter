@echo off

echo ##### Calling: "%~nx0" (%0)

doing docker-compose down --volumes
docker compose -f docker-compose-postgres-local.yml up --remove-orphans
