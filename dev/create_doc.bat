
@echo off

setlocal

echo ##### Calling: "%~nx0" (%0)

set SCRIPT_DIR=%~dp0
set DOC_MAINDIR=%SCRIPT_DIR%..\docs

pushd "%DOC_MAINDIR%"

sphinx-build.exe -b html source build

popd
