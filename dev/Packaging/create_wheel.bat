@echo off

echo ##### Calling: "%~nx0" (%0)

python setup.py sdist bdist_wheel
