
@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set SCRIPT_DIR=%~dp0
set TEST_DIR=%SCRIPT_DIR%Testing
set ERROR_FOUND=
set ERROR_LIST=

if /I "%1"=="sqlite" (
    echo Argument "%1" passed, use sqlite as db
    set DJANGO_SETTINGS_MODULE=django_test_proj.settings
    goto run_tests
)
if /I "%1"=="postgres-travis" (
    echo Argument "%1" passed, use postgresql for travis as db
    set DJANGO_SETTINGS_MODULE=django_test_proj.settings_postgres_travis
    goto run_tests
)
if /I "%1"=="postgres-local" (
    echo Argument "%1" passed, use postgresql for local dev as db
    set DJANGO_SETTINGS_MODULE=django_test_proj.settings_postgres_local
    goto run_tests
)

echo No or unexpected Argument "%1" Passed
goto goto error

:run_tests
echo DJANGO_SETTINGS_MODULE: '%DJANGO_SETTINGS_MODULE%'
echo ### Start Testing ###
call:run_tester "Pytest"        "%TEST_DIR%\RunPytest.bat"
rem call:run_tester "DjangoTests"   "%TEST_DIR%\RunDjangoTests.bat"
echo ### Testing finished ###

if defined ERROR_FOUND (
    goto error
) else (
    goto end
)

: #########################################
: ##### START OF FUNCTION DEFINITIONS #####
: #########################################
:run_tester
set TESTER_NAME=%~1
set TESTER_SCRIPT=%~2

echo ### TESTS START - '%TESTER_SCRIPT%' ###
call "%TESTER_SCRIPT%"

set return_code=%errorlevel%
echo return_code: %return_code%
if %return_code% gtr 0 (
    set ERROR_FOUND=TRUE
    set ERROR_LIST=%ERROR_LIST% %TESTER_NAME%
    echo   Issues Found
) else (
    echo   No Issues
)
echo ### TESTS END - '%TESTER_SCRIPT%' ###
echo[
goto:eof
: #######################################
: ##### END OF FUNCTION DEFINITIONS #####
: #######################################

:error
echo !!! CHECK OUTPUT, SOME TESTING ISSUE FOUND WITH
for %%a in (%ERROR_LIST%) do (
   echo   - %%a
)

endlocal
echo exit /B 1
exit /B 1

:end
echo !!! NO TESTING ISSUE FOUND
endlocal
echo exit /B 0
exit /B 0
