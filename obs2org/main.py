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
from os import path, walk
from pathlib import Path, PurePath
from typing import NamedTuple

from obs2org import VERSION
from obs2org.convert import convert_single_file, correct_org_mode


class FilePaths(NamedTuple):
    """Class holding the path to the Markdown file to convert and the path to the
    Org-Mode file to generate.
    """

    in_file: Path
    """Path to the Markdown file to convert."""
    out_file: Path
    """Path to the generated Org-Mode file."""


__descriptionText: str = (
    """Converts markdown formatted files to Org-Mode formatted files using Pandoc."""
)
__epilogText: str = """Examples:

python -m obs2org (which is the same as 'python -m obs2org ./')

Converts all markdown files with a suffix of '.md' in the current working
directory and all its subdirectories to files in Org-Mode format with the
same base filename but a '.org' suffix.

python -m obs2org hugo.md -o sepp.org

Converts the markdown document 'hugo.md' to an Org-Mode document named
'sepp.org'.

python -m obs2org *.md

Converts all markdown files with a suffix of '.md' in the current working
directory to files in Org-Mode format with the same base filename but a
'.org' suffix.

python -m obs2org *.md ../Org

Converts all markdown files with a suffix of '.md' in the current working
directory to files in Org-Mode format with the same base filename but a
'.org' suffix in the directory '../Org'.

python -m obs2org ./Markdown ../Org

Converts all markdown files with a suffix of '.md' in the directory
'./Markdown' and its subdirectories to files in Org-Mode format with
the same base filename but a '.org' suffix in the directory '../Org'.

See website https://github.com/Release-Candidate/Obs2Org for details."""


################################################################################
def main() -> None:
    """The program's main entry point."""
    cmd_line_args, cmd_line_parser = parse_command_line()

    _convert_files(cmd_line_args=cmd_line_args, cmd_line_parser=cmd_line_parser)


###############################################################################
def parse_command_line() -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    """Parses the command line arguments of the program.

    Returns a tuple containing a `Namespace` object holding all
    parsed command line arguments and the command line parser object, an
    `argparse.ArgumentParser`.

    Returns
    -------
    tuple[argparse.Namespace, argparse.ArgumentParser]
         The parsed command line arguments in a `argparse.Namespace` object,
         the `argparse.ArgumentParser` object as the second element.
    """
    cmd_line_parser = argparse.ArgumentParser(
        prog="python -m obs2org",
        description=__descriptionText,
        epilog=__epilogText,
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    cmd_line_parser.add_argument(
        "files",
        metavar="MARKDOWN_FILES",
        nargs="*",
        help="""The path to the markdown files or directory to convert to
Org-Mode format. If this is a file or a list of markdown
files, these files are converted. If this is a directory,
all markdown files - files with a suffix of '.md' - in
this directory will be converted recursively descending
into subdirectories. If no markdown files or directory
are given, the current working directory is used.""",
        default="./",
    )

    cmd_line_parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="obs2org {version}".format(version=VERSION),
    )

    cmd_line_parser.add_argument(
        "-p",
        "--pandoc",
        metavar="PANDOC",
        type=str,
        dest="pandoc_exe",
        default="pandoc",
        help="""PANDOC is the path to the pandoc executable, if the
Pandoc executable isn't in the PATH.""",
    )

    cmd_line_parser.add_argument(
        "-o",
        "--out",
        metavar="OUT_PATH",
        type=str,
        dest="out_path",
        default="./",
        help="""OUT_PATH is the path to the file or directory to save the
converted Org-Mode file to.
If MARKDOWN_FILES is a single file this is used as the
filename of the converted file.
If MARKDOWN_FILES are more than one file or a directory,
this is used as the pathname of the directory to save the
converted files to.""",
    )

    return cmd_line_parser.parse_args(), cmd_line_parser


###############################################################################
def _convert_files(
    cmd_line_args: argparse.Namespace, cmd_line_parser: argparse.ArgumentParser
) -> None:
    """Convert the markdown files to Org-Mode files.

    Convert the given markdown files or markdown files in the given
    directory to Org-Mode format.

    Parameters
    ----------
    cmd_line_args : argparse.Namespace
        The command line arguments of the program.
    cmd_line_parser : argparse.ArgumentParser
        The command line parser object to use.
    """
    pandoc_path = cmd_line_args.pandoc_exe

    if isinstance(cmd_line_args.files, list):
        path_list: list[str] = cmd_line_args.files
    else:
        path_list = [cmd_line_args.files]

    out_path = _check_out_path(cmd_line_args, cmd_line_parser, path_list)

    list_of_files: list[FilePaths] = []

    for arg_path in path_list:
        if path.isdir(arg_path):
            for dirpath, _, filenames in walk(
                top=arg_path, topdown=True, followlinks=True
            ):
                for file in filenames:
                    file_object = PurePath(file)
                    if file_object.suffix == ".md":
                        in_file = path.join(dirpath, file)
                        out_file = path.join(out_path, file_object.with_suffix(".org"))
                        list_of_files.append(
                            FilePaths(in_file=Path(in_file), out_file=Path(out_file))
                        )

        elif path.isfile(arg_path):
            file_obj = Path(arg_path)
            out_file = path.join(out_path, file_obj.with_suffix(".org"))
            list_of_files.append(FilePaths(in_file=file_obj, out_file=Path(out_file)))
        else:
            cmd_line_parser.print_help()
            cmd_line_parser.error(
                "no markdown files found at path '{path}'".format(path=arg_path)
            )

    _do_convert_files(pandoc_path=pandoc_path, list_of_files=list_of_files)


################################################################################
def _check_out_path(
    cmd_line_args: argparse.Namespace,
    cmd_line_parser: argparse.ArgumentParser,
    path_list: list[str],
) -> str:
    """Validate the path to write the Org-Mode file(s) to and return the checked
    path.
    If the path is wrong, e.g. a path to a file for more than one Markdown file
    to convert, the program exits with an error message.

    Parameters
    ----------
    cmd_line_args : argparse.Namespace
        The object holding the command line arguments.
    cmd_line_parser : argparse.ArgumentParser
        The command line parser object.
    path_list : list[str]
        The list of paths to Markdown files to convert.

    Returns
    -------
    str
        The checked path to the Org-Mode file(s) on success, exits the program
        on errors.
    """
    out_path: str = cmd_line_args.out_path

    if path.basename(out_path) == "" or path.isdir(out_path):
        print("Output to directory {dir}".format(dir=out_path))
        Path(out_path).mkdir(exist_ok=True, parents=True)
    else:
        print("Output to file {file}".format(file=out_path))
        if len(path_list) <= 1:
            cmd_line_parser.print_help()
            cmd_line_parser.error(
                "more than one markdown file to convert given, but just one output file '{path}'!".format(
                    path=out_path
                )
            )

    return out_path


################################################################################
def _do_convert_files(pandoc_path: str, list_of_files: list[FilePaths]) -> None:
    """Converts the files in the given list.

    First converts the files in `list_of_files` using pandoc and then fixes the
    links to other Org-Mode files and tags and dates.
    We have to do the conversion first, because links that need to be corrected
    can point to files not generated yet and we must search the files the link
    points to for the right section id.

    Parameters
    ----------
    pandoc_path : str
        Path to the pandoc executable.
    list_of_files : list[FilePaths]
        List of `FilePaths` containing the path to the Markdown file to convert
        and the Org-Mode file to generate.
    """
    for convert_file in list_of_files:
        convert_single_file(
            path=convert_file.in_file,
            out_path=convert_file.out_file,
            pandoc=pandoc_path,
        )
    for correct_file in list_of_files:
        correct_org_mode(correct_file.out_file)
