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
def convert_single_file(path: Path, out_path: Path, pandoc: str) -> None:
    """Convert a markdown file to an Org-Mode formatted file.

    Convert the markdown file with the given path `path` to an Org-Mode file
    with the given path `out_path`.

    Parameters
    ----------
    path : Path
        The path to the markdown file to convert.
    out_path : Path
        The path to the Org-Mode file to generate.
    pandoc : str
        The path to the pandoc executable to convert the file.
    """
    print(
        "Converting file '{in_path}' to '{out_path}' using '{pandoc}'\n".format(
            in_path=path, out_path=out_path, pandoc=pandoc
        ),
        flush=True,
    )
    try:
        run_pandoc(in_file=path, out_path=out_path, pandoc=pandoc)
    except subprocess.SubprocessError as excp:
        print(
            "{err} converting file '{in_path}' to '{out_path}'\n".format(
                err=excp, in_path=path, out_path=out_path
            ),
            flush=True,
        )
    else:
        print("File converted to '{path}'.\n".format(path=out_path), flush=True)


###############################################################################
def run_pandoc(in_file: Path, out_path: Path, pandoc: str) -> None:
    """Run the pandoc executable to convert the given markdown file.

    Execute `pandoc` to convert the given markdown file `in_file` to
    an Org-Mode file with path `out_path`.

    Parameters
    ----------
    in_file : Path
        Path to the markdown file to convert.
    out_path : Path
        Path to the Org-Mode file to generate.
    pandoc : str
        Path to the pandoc executable or the name of the executable if it is
        in the PATH.
    """
    args: list[str] = [
        pandoc,
        str(in_file),
        "-f",
        "markdown",
        "-t",
        "org",
        "-s",
        "--eol=lf",
        "--toc",
        "--wrap=none",
        "-o",
        str(out_path),
    ]
    pandoc_out = subprocess.run(
        args=args,
        check=False,
        shell=False,  # nosec
        text=True,
        capture_output=True,
    )

    if pandoc_out.returncode != 0 and pandoc_out.stderr is not None:
        raise subprocess.SubprocessError(
            "Pandoc error: '{err}'".format(err=pandoc_out.stderr.strip())
        )


###############################################################################
def correct_org_mode(file_path: Path) -> None:
    """Correct internal links, tags and dates in the generated Org-Mode file.

    Parse the generated Org-Mode file with path `out_path` and correct
    internal links, tags and dates in this file.

    Parameters
    ----------
    file_path : str
        The path to the generated Org-Mode file to correct.

    """
    print("Correcting links, tags, ... in file '{in_path}'".format(in_path=file_path))
    tmp_file = file_path.with_suffix(".org~")
    try:
        with file_path.open(mode="r", encoding="utf-8") as f_d:
            file_text = f_d.read()
            new_text = correct_org_mode_file(file_text, file_path.parent)
        with tmp_file.open(mode="w", encoding="utf-8") as tmp:
            tmp.write(new_text)

        tmp_file.replace(file_path)

    except FileNotFoundError as excp:
        print("Error, a file has not been found. '{err}'".format(err=excp))
    except OSError as excp:
        print("Error opening file '{file}': {err}".format(file=tmp_file, err=excp))
    except Exception as excp:
        print("Error: opening file '{}': {err}".format(file=tmp_file, err=excp))

    else:
        print("OK\n")
