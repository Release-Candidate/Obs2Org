#!/bin/sh
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  PYTHON_TEMPLATE
# File:     run_local_linters.sh
#
################################################################################

# Runs the local linters
isort PYTHON_TEMPLATE tests
black PYTHON_TEMPLATE tests
pyflakes PYTHON_TEMPLATE tests
pycodestyle PYTHON_TEMPLATE tests
pydocstyle PYTHON_TEMPLATE tests
flake8 PYTHON_TEMPLATE tests
bandit -r PYTHON_TEMPLATE tests
