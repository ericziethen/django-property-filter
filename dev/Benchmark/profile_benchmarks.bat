
@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set SCRIPT_DIR=%~dp0
set PROJ_MAIN_DIR=%SCRIPT_DIR%..\..
set MODULE_PATH=%PROJ_MAIN_DIR%\django_property_filter
set DJANGO_DIR=%PROJ_MAIN_DIR%\tests\django_test_proj
set CSV_FILE_PATH=%PROJ_MAIN_DIR%\benchmarks.csv



for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set DateTime=%%a

set Yr=%DateTime:~0,4%
set Mon=%DateTime:~4,2%
set Day=%DateTime:~6,2%
set Hr=%DateTime:~8,2%
set Min=%DateTime:~10,2%
set Sec=%DateTime:~12,2%

set datetimef=%Yr%.%Mon%.%Day%_%Hr%-%Min%-%Sec%

set PROFILE_LOG=%PROJ_MAIN_DIR%\profile_%datetimef%.html

pushd "%DJANGO_DIR%"


call:run_benchmark_sqlite "10000"

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
echo %data%-%time% ### RUN BENCHMARK - %DB_ENTRIES% entries - Settings: "%DJANGO_SETTINGS_MODULE%" ###
echo Command: 'python -m pyinstrument manage.py run_benchmarks %DB_ENTRIES% "%CSV_FILE_PATH%"' > "%PROFILE_LOG%"
python -m pyinstrument -r html --show-all manage.py run_benchmarks %DB_ENTRIES% "%CSV_FILE_PATH%" > "%PROFILE_LOG%"
echo %data%-%time% ### BENCHMARK END ###
echo[
goto:eof


:end
popd
endlocal
