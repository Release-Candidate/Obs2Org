:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  PYTHON_TEMPLATE
:: File:     make_package.bat
::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: generates a Python PIP package in the current working directory and uploads
:: it to Pypi.
:: Uses pipenv, you can install that by `python -m pip install pipenv` and
:: installing the needed packages from the PYTHON_TEMPLATE root dir `PYTHON_TEMPLATE` - where
:: the `Pipfile` is located.
:: `pipenv install --dev` installs all needed dependencies to develop.

@echo off

rmdir /S /Q build
rmdir /S /Q dist
rmdir /S /Q PYTHON_TEMPLATE.egg-info

::pipenv run python -m build
echo Do not build the package under Windows, the file permissions are lost, shell
echo scripts are no longer executable!


:: pipenv run twine upload --repository testpypi dist/* --config-file %APPDATA%\pip\pip.ini

:: pipenv run twine upload --repository pypi dist/* --config-file %APPDATA%\pip\pip.ini
