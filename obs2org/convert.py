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
from pathlib import Path

from obs2org.parse_org_mode import correct_org_mode_file


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
        correct_org_mode(out_path)
    except subprocess.SubprocessError as excp:
        print(
            "{err} converting file '{in_path}' to '{out_path}'\n".format(
                err=excp, in_path=path, out_path=out_path
            )
        )
    else:
        print("OK\n")


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
        text=True,
        capture_output=True,
    )

    if pandoc_out.returncode != 0 and pandoc_out.stderr is not None:
        raise subprocess.SubprocessError(
            "Pandoc error: '{err}'".format(err=pandoc_out.stderr.strip("\n"))
        )


###############################################################################
def correct_org_mode(out_path: str) -> None:
    """Correct internal links, tags and dates in the generated Org-Mode file.

    Parse the generated Org-Mode file with path `out_path` and correct
    internal links, tags and dates in this file.

    Parameters
    ----------
    out_path : str
        The path to the generated Org-Mode file to correct.

    """
    in_file = Path(out_path)

    tmp_file = Path(out_path + "~")
    try:
        with in_file.open(mode="r", encoding="utf-8") as fd:
            file_text = fd.read()
            new_text = correct_org_mode_file(file_text, in_file.parent)
        with tmp_file.open(mode="w", encoding="utf-8") as tmp:
            tmp.write(new_text)

        tmp_file.replace(out_path)

    except FileNotFoundError as excp:
        print("ERR {err}".format(err=excp))
