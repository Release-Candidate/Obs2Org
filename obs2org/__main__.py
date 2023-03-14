# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Obs2Org
# File:     __main__.py
# Date:     26.10.2021
# ===============================================================================
"""The main entry point of the program, does nothing but call the 'real' main
function `main`.
"""

# This is just a wrapper to catch when running using python 2. The real `main`
# is in `main.py`.

from __future__ import print_function

import platform
import sys

if sys.version_info.major < 3 or sys.version_info.minor < 9:
    print(
        f"ERROR: Python version is too old, I need at least Python 3.9,"
        f" this has a version of {platform.python_version()}",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    from asyncio import run

    from obs2org import main

    run(main.main())
