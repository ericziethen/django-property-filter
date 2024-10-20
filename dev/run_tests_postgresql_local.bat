
@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set SCRIPT_DIR=%~dp0

call .\dev\clean_test_proj.bat
"%SCRIPT_DIR%run_tests.bat" postgres-local

endlocal
