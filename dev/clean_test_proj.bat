@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal EnableDelayedExpansion

echo Args: %*

set SCRIPT_DIR=%~dp0
pushd %SCRIPT_DIR%

set TEST_PROJ_DIR=..\tests\django_test_proj

del "%TEST_PROJ_DIR%\db.sqlite3" /Q
del "%TEST_PROJ_DIR%\property_filter\migrations\00*.py" /Q

goto end


:end
endlocal
