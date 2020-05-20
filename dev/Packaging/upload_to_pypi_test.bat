@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0..\..

set PKG_NAME=django-filter-property

pushd "%PROJ_MAIN_DIR%"

echo CurrentDIr: %CD%

twine upload --repository testpypi dist/*

echo ProjectUrl: https://test.pypi.org/project/%PKG_NAME%

echo Install with: 'pip install --extra-index-url https://test.pypi.org/simple/ %PKG_NAME%'

popd

endlocal
