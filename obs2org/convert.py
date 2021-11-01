# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Obs2Org
# File:     convert.py
# Date:     01.11.2021
# ===============================================================================
"""Module containing the actual conversion functions to convert markdown files
to Org-Mode files.
"""

from __future__ import annotations

import subprocess  # nosec B404


###############################################################################
def convert_single_file(path: str, out_path: str, pandoc: str) -> None:
    """Convert a markdown file to an Org-Mode formatted file.

    Convert the markdown file with the given path `path` to an Org-Mode file
    with the given path `out_path`.

    Parameters
    ----------
    path : str
        The path to the markdown file to convert.
    out_path : str
        The path to the Org-Mode file to generate.
    pandoc : str
        The path to the pandoc executable to convert the file.
    """
    print(
        "Converting file '{in_path}' to '{out_path}' using '{pandoc}'".format(
            in_path=path, out_path=out_path, pandoc=pandoc
        )
    )
    try:
        run_pandoc(in_file=path, out_path=out_path, pandoc=pandoc)

    except Exception as excp:
        print(
            "Error '{err}' converting file '{in_path}' to '{out_path}'".format(
                err=excp, in_path=path, out_path=out_path
            )
        )


###############################################################################
def run_pandoc(in_file: str, out_path: str, pandoc: str) -> None:
    """Run the pandoc executable to convert the given markdown file.

    Execute `pandoc` to convert the given markdown file `in_file` to
    an Org-Mode file with path `out_path`.

    Parameters
    ----------
    in_file : str
        Path to the markdown file to covnert.
    out_path : str
        Path to the Org-Mode file to generate.
    pandoc : str
        Path to the pandoc executable or the name of the executable if it is in the PATH.
    """
    pandoc_out = subprocess.run(
        args=[
            pandoc,
            in_file,
            "-f",
            "markdown",
            "-t",
            "org",
            "-s",
            "--eol=lf",
            "--toc",
            "--wrap=none",
            "-o",
            out_path,
        ],
        check=False,
        shell=True,
        capture_output=True,
    )

    if pandoc_out.returncode != 0:
        print("Pandoc error: '{err}'".format(err=pandoc_out.stderr.decode()))
