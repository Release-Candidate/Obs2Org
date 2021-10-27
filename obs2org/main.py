# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Obs2Org
# File:     main.py
# Date:     26.10.2021
# ===============================================================================
"""Contains the program's real main entry point, `main`."""

from __future__ import annotations

import argparse

from obs2org import VERSION

__descriptionText: str = "DESC"
__epilogText: str = (
    "See website https://github.com/Release-Candidate/Obs2Org for details"
)


################################################################################
def main() -> None:
    """The program's main entry point."""
    cmd_line_parser = argparse.ArgumentParser(
        prog="python -m obs2org",
        description=__descriptionText,
        epilog=__epilogText,
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    cmd_line_parser.add_argument(
        "--version",
        action="version",
        version="obs2org {version}".format(version=VERSION),
    )

    # cmd_line_args = cmd_line_parser.parse_args()
