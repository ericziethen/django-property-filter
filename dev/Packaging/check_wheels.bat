@echo off

echo ##### Calling: "%~nx0" (%0)

set PROJ_MAIN_DIR=%~dp0../..

pushd "%PROJ_MAIN_DIR%""

echo DIR: %CD%

twine check dist/*

popd
