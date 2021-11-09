Contributing
============

Python, version > 3.9
~~~~~~~~~~~~~~~~~~~~~

You need Python 3.9 or newer.

Setup
~~~~~

1. Run ``pipenv install --dev`` to install the Python environment in the
   project directory

2. Run ``pipenv run pre-commit install`` to install the pre commit hooks
   to git. Now every time you commit a change, the linters are run.

   -  To run the pre commit checks manually:
      ``pipenv run pre-commit run --all-files``

Scripts
~~~~~~~

-  ` <./make_package.sh>`__ - Linux, OS X: build the Obs2Org PyPI
   package
-  `./make_package.bat <./make_package.bat>`__ - Windows: build the
   Obs2Org PyPI package. This is disabled on Windows, because the
   scripts would not be executable because of the Windows filesystem.
-  `./run_local_linters.sh <./run_local_linters.sh>`__ - Linux, OS X:
   run all configured linters on the Source code and tests.
-  `./run_local_linters.bat <./run_local_linters.bat>`__ - Windows: run
   all configured linters on the Source code and tests.
-  `./run_tests.sh <./run_tests.sh>`__ - Linux, OS X: run all tests.
-  `./run_tests.bat <./run_tests.bat>`__ - Windows: run all tests.

Documentation
~~~~~~~~~~~~~

Ths source files for the `Read the
Docs <https://obs2org.readthedocs.io/en/latest>`__ site are located in
the directory `./obs2org/doc/source <./obs2org/doc/source>`__

Sources
~~~~~~~

The sources of the program are in the directory
`./obs2org/ <./obs2org/>`__, the test sources and fixtures in
`./tests/ <./tests/>`__
