@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0..
set DJANGO_DIR=%PROJ_MAIN_DIR%\tests\django_test_proj

echo CD: %CD%
echo: pushd "%DJANGO_DIR%"
pushd %DJANGO_DIR%
echo CD: %CD%

python manage.py migrate --fake
set return_code=%errorlevel%
if %return_code% equ 0 (
    echo *** No Django Issues Found
    goto exit_ok
) else (
    echo *** Some Django Issues Found
    goto exit_error
)

:exit_error
popd
endlocal
echo exit /B 1
exit /B 1

:exit_ok
popd
endlocal
echo exit /B 0
exit /B 0
