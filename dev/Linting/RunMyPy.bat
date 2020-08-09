@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set BATCH_DIR=%~dp0
set PROJ_MAIN_DIR=%BATCH_DIR%..\..
set MODULE_PATH=%PROJ_MAIN_DIR%\django_property_filter

set MYPYPATH=%MYPYPATH%;%MODULE_PATH%

mypy "%MODULE_PATH%"
set return_code=%errorlevel%
if %return_code% equ 0 (
    echo *** No Issues Found
    goto exit_ok
) else (
    echo *** Some Issues Found
    goto exit_error
)

:exit_error
endlocal
exit /B 1

:exit_ok
endlocal
exit /B 0
