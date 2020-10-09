
@echo off

echo ##### Calling: "%~nx0" (%0)

echo Before: DJANGO_SETTINGS_MODULE = '%DJANGO_SETTINGS_MODULE%'
set DJANGO_SETTINGS_MODULE=django_test_proj.settings_postgres_local
echo After: DJANGO_SETTINGS_MODULE = '%DJANGO_SETTINGS_MODULE%'
