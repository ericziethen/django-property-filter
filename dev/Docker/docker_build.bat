@echo off

echo ##### Calling: "%~nx0" (%0)

docker compose -f docker-compose-postgres-local.yml build
