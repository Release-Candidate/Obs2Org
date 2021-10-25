:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  PYTHON_TEMPLATE
:: File:     run_tests.bat
::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: slow version
:: pytest --hypothesis-show-statistics --no-cov

:: Running the tests using 12 processes.
pytest --hypothesis-show-statistics --no-cov -n 12
