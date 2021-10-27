#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Obs2Org
# File:     run_local_linters.sh
#
################################################################################

# Runs the local linters
isort obs2org tests
black obs2org tests
pyflakes obs2org tests
pycodestyle obs2org tests
pydocstyle obs2org tests
flake8 obs2org tests
bandit -r obs2org tests


pre-commit run --all-files
