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
        f"Converting file '{path}' to '{out_path}' using '{pandoc}'\n",
        flush=True,
    )
    try:
        run_pandoc(in_file=path, out_path=out_path, pandoc=pandoc)
    except subprocess.SubprocessError as excp:
        print(
            f"{excp} converting file '{path}' to '{out_path}'\n",
            flush=True,
        )
    else:
        print(f"File converted to '{out_path}'.\n", flush=True)


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

    if pandoc_out.returncode != 0 and pandoc_out.stderr != "":
        raise subprocess.SubprocessError(f"Pandoc error: '{pandoc_out.stderr.strip()}'")


###############################################################################
def correct_org_mode(
    file_path: Path,
    remove_citations: bool,
    add_uuid: bool,
) -> None:
    """Correct internal links, tags and dates in the generated Org-Mode file.

    Parse the generated Org-Mode file with path `out_path` and correct
    internal links, tags and dates in this file.

    Parameters
    ----------
    file_path : str
        The path to the generated Org-Mode file to correct.
    remove_citations : bool
        Whether to remove Pandoc-style citations to treat them as normal links,
        or not.
    add_uuid : bool
        Whether to add an UUID-header to each file.

    """
    print(f"Correcting links, tags, ... in file '{file_path}'")
    tmp_file = file_path.with_suffix(".org~")
    try:
        with file_path.open(mode="r", encoding="utf-8") as f_d:
            file_text = f_d.read()
            new_text = correct_org_mode_file(
                file_text,
                file_path.parent,
                add_uuid=add_uuid,
                remove_citations=remove_citations,
            )
        with tmp_file.open(mode="w", encoding="utf-8") as tmp:
            tmp.write(new_text)

        tmp_file.replace(file_path)

    except FileNotFoundError as excp:
        print(f"Error, a file has not been found. '{excp}'")
    except OSError as excp:
        print(f"Error opening file '{tmp_file}': {excp}")
    except Exception as excp:
        print(f"Error: opening file '{tmp_file}': {excp}")

    else:
        print("OK\n")
