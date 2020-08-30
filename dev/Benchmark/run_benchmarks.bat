
@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set SCRIPT_DIR=%~dp0
set PROJ_MAIN_DIR=%SCRIPT_DIR%..\..
set MODULE_PATH=%PROJ_MAIN_DIR%\django_property_filter
set DJANGO_DIR=%PROJ_MAIN_DIR%\tests\django_test_proj
set CSV_FILE_PATH=%PROJ_MAIN_DIR%\benchmarks.csv

pushd "%DJANGO_DIR%"

rem call:run_benchmarks "10"
rem call:run_benchmarks "100"
call:run_benchmarks "1000"
rem call:run_benchmarks "10000"
rem call:run_benchmarks "50000"
rem call:run_benchmarks "100000"
goto end

:run_benchmarks
set DB_ENTRIES=%~1
call:run_benchmark_sqlite "%DB_ENTRIES%"
call:run_benchmark_postgres "%DB_ENTRIES%"
goto:eof

:run_benchmark_sqlite
set DB_ENTRIES=%~1
set DJANGO_SETTINGS_MODULE=django_test_proj.settings
call:run_benchmark "%DB_ENTRIES%"
goto:eof

:run_benchmark_postgres
set DB_ENTRIES=%~1
set DJANGO_SETTINGS_MODULE=django_test_proj.settings_postgres_local
call:run_benchmark "%DB_ENTRIES%"
goto:eof

:run_benchmark
set DB_ENTRIES=%~1
echo %date%-%time% ### RUN BENCHMARK - %DB_ENTRIES% entries - Settings: "%DJANGO_SETTINGS_MODULE%" ###
python manage.py run_benchmarks %DB_ENTRIES% "%CSV_FILE_PATH%"
echo %date%-%time% ### BENCHMARK END ###
echo[
goto:eof


:end
popd
endlocal
