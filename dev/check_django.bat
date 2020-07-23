@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0..
set MODULE_PATH=%PROJ_MAIN_DIR%\django_property_filter
set DJANGO_DIR=%PROJ_MAIN_DIR%\tests\django_test_proj

set PYTHONPATH=%PYTHONPATH%;%MODULE_PATH%

python "%DJANGO_DIR%\manage.py" migrate --fake
set return_code=%errorlevel%
if %return_code% equ 0 (
    echo *** No Django Issues Found
    goto exit_ok
) else (
    echo *** Some Django Issues Found
    goto exit_error
)

:exit_error
endlocal
echo exit /B 1
exit /B 1

:exit_ok
endlocal
echo exit /B 0
exit /B 0
