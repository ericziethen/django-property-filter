@echo off

echo ##### Calling: "%~nx0" (%0)

pip-audit --desc --strict
