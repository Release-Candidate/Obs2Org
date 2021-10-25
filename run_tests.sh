#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Obs2Org
# File:     run_tests.bat
#
################################################################################

# slow version
# pytest --hypothesis-show-statistics --no-cov

# Running the tests using 12 processes.
pytest --hypothesis-show-statistics --no-cov -n 12
