@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0..

pushd %PROJ_MAIN_DIR%

for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set DateTime=%%a

set Yr=%DateTime:~0,4%
set Mon=%DateTime:~4,2%
set Day=%DateTime:~6,2%
set Hr=%DateTime:~8,2%
set Min=%DateTime:~10,2%
set Sec=%DateTime:~12,2%

set datetimef=%Yr%.%Mon%.%Day%_%Hr%-%Min%-%Sec%

!!! CONFIGURE SOURCE ROOT HERE !!!
set SOURCE_ROOT=django_filter_property
set PYTHON_PROG=#PYTHON_PROG_NAME#
set ARGS=
set PROFILE_DIR=%PROJ_MAIN_DIR%\profiling
if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"
set PROFILE_LOG=%PROFILE_DIR%\profile_%datetimef%.txt

echo Command: "python -m pyinstrument "%PYTHON_PROG%" > "%PROFILE_LOG%""
python -m pyinstrument "%PYTHON_PROG%" %ARGS% > "%PROFILE_LOG%""

:end

popd

endlocal
