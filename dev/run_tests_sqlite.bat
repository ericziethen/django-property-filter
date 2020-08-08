
@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set SCRIPT_DIR=%~dp0

"%SCRIPT_DIR%run_tests.bat" sqlite

endlocal
