#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Obs2Org
# File:     make_package.sh
#
################################################################################

# generates a Python PIP package in the current working directory and uploads
# it to Pypi.
# Uses pipenv, you can install that by `python -m pip install pipenv` and
# installing the needed packages from the Obs2Org root dir `Obs2Org` - where
# the `Pipfile` is located.
# `pipenv install --dev` installs all needed dependencies to develop.


rm -rf -- ./build
rm -rf -- ./dist
rm -rf -- ./obs2org.egg-info

pipenv run python -m build

# pipenv run twine upload --repository testpypi dist/* --config-file ~/.pypirc

pipenv run twine upload --repository pypi dist/* --config-file ~/.pypirc
