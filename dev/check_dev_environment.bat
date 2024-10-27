@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal enabledelayedexpansion

set PROJ_MAIN_DIR=%~dp0..
set REQUIREMENTS_FILE=%PROJ_MAIN_DIR%\requirements.txt
set TEMP_FILE_PATH=%TEMP%\tem_django_property_filter_dev_check.txt
set TOX_FILE=%PROJ_MAIN_DIR%\tox.ini

set ERROR_FOUND=
call:CHECK_REQUIREMENT_IN_TOX "pytest" "%REQUIREMENTS_FILE%" "%TOX_FILE%"
call:CHECK_REQUIREMENT_IN_TOX "pytest-cov" "%REQUIREMENTS_FILE%" "%TOX_FILE%"
call:CHECK_REQUIREMENT_IN_TOX "pytest-django" "%REQUIREMENTS_FILE%" "%TOX_FILE%"

if defined ERROR_FOUND (
    goto error
) else (
    goto end
)

:error
echo[
echo --------------------------------------------------------
echo !!! CHECK OUTPUT, SOME DEV ENVIRONMENT ISSUE FOUND
endlocal
echo exit /B 1
exit /B 1

:end
echo[
echo ########################################################
echo !!! NO DEV ENVIRONMENT ISSUE FOUND
endlocal
echo exit /B 0
exit /B 0


: #########################################
: ##### START OF FUNCTION DEFINITIONS #####
: #########################################

:CHECK_REQUIREMENT_IN_TOX
set REQUIREMENT_NAME=%~1
set REQUIREMENTS_FILE=%~2
set TOX_FILE=%~3
echo[
echo ##### Checking '%REQUIREMENT_NAME%' in requirements file '%REQUIREMENTS_FILE%' and tox file '%TOX_FILE%'

set result=
for /f "tokens=*" %%i in ('FINDSTR /C:"%REQUIREMENT_NAME%==" "%REQUIREMENTS_FILE%"') do (
    echo %%i
    set result=%%i
)
if "!result!"=="" ( 
    echo 1 - DID NOT FIND "%REQUIREMENT_NAME%==" inside "%REQUIREMENTS_FILE%"
    set ERROR_FOUND=TRUE
    goto:eof
) else (
    echo 2 - Found "!result!" inside "%REQUIREMENTS_FILE%"
)

FINDSTR /C:!result! "%TOX_FILE%"
set return_code=%errorlevel%
if %return_code% equ 0 (
    echo 3 - Found "!result!" inside "%TOX_FILE%"
) else (
    echo 4 - DID NOT FIND "!result!" inside "%TOX_FILE%"
    set ERROR_FOUND=TRUE
    echo Command: 'FINDSTR /C:%REQUIREMENT_NAME%== "%TOX_FILE%"'
    FINDSTR /C:%REQUIREMENT_NAME%== "%TOX_FILE%"
)
goto:eof
