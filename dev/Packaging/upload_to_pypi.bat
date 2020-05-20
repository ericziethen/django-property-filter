@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0..\..

set PKG_NAME=django-filter-property

pushd "%PROJ_MAIN_DIR%"

echo CurrentDIr: %CD%

rem twine upload --repository pypi dist/*

echo !!! Pypi Upload is currently Disabled until the project is stable

echo ProjectUrl: https://pypi.org/project/%PKG_NAME%

echo Install with: 'pip install --extra-index-url https://pypi.org/simple/ %PKG_NAME%'

popd

endlocal
