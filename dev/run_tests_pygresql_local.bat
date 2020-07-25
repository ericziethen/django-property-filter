
@echo off

setlocal

set SCRIPT_DIR=%~dp0

"%SCRIPT_DIR%run_tests.bat" postgres-local

endlocal
