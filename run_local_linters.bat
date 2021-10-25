:: SPDX-License-Identifier: GPL-3.0-or-later
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Obs2Org
:: File:     run_local_linters.bat
::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Runs the local linters
isort Obs2Org tests
black Obs2Org tests
pyflakes Obs2Org tests
pycodestyle Obs2Org tests
pydocstyle Obs2Org tests
flake8 Obs2Org tests
bandit -r Obs2Org tests
