
@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set SCRIPT_DIR=%~dp0
set PROJ_MAIN_DIR=%SCRIPT_DIR%..\..
set MODULE_PATH=%PROJ_MAIN_DIR%\django_property_filter
set DJANGO_DIR=%PROJ_MAIN_DIR%\tests\django_test_proj

for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set DateTime=%%a

set Yr=%DateTime:~0,4%
set Mon=%DateTime:~4,2%
set Day=%DateTime:~6,2%
set Hr=%DateTime:~8,2%
set Min=%DateTime:~10,2%
set Sec=%DateTime:~12,2%

set datetimef=%Yr%.%Mon%.%Day%_%Hr%-%Min%-%Sec%

pushd "%DJANGO_DIR%"

call:run_benchmark_sqlite

goto end

:run_benchmarks
call:run_benchmark_sqlite
call:run_benchmark_postgres
goto:eof

:run_benchmark_sqlite
set DJANGO_SETTINGS_MODULE=django_test_proj.settings
call:run_benchmark
goto:eof

:run_benchmark_postgres
set DJANGO_SETTINGS_MODULE=django_test_proj.settings_postgres_local
call:run_benchmark
goto:eof

:run_benchmark
echo %date%-%time% ### RUN PROFILER - Settings: "%DJANGO_SETTINGS_MODULE%" ###

rem Run Benchmark
set PROFILE_DIR=%SCRIPT_DIR%Profiling
if not exist "%PROFILE_DIR%" md "%PROFILE_DIR%"
set PROFILE_LOG_BASE_NAME=%PROFILE_DIR%\profile_%datetimef%
echo Command: 'python manage.py profile_filter "%PROFILE_LOG_BASE_NAME%"'
python manage.py profile_filter "%PROFILE_LOG_BASE_NAME%"

echo %date%-%time% ### PROFILER END ###
echo[
goto:eof

:end
popd
endlocal
