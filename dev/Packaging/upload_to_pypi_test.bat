@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set PROJ_MAIN_DIR=%~dp0..\..

set PKG_NAME=django-property-filter

pushd "%PROJ_MAIN_DIR%"

echo CurrentDIr: %CD%

twine upload --repository testpypi dist/*

echo ProjectUrl: https://test.pypi.org/project/%PKG_NAME%

echo Install with: 'pip install --extra-index-url https://test.pypi.org/simple/ %PKG_NAME%'

popd

endlocal
