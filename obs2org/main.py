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
from pathlib import PurePath

from obs2org import VERSION
from obs2org.convert import convert_single_file

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

    convert_files(cmd_line_args=cmd_line_args, cmd_line_parser=cmd_line_parser)


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
def convert_files(
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
        convert_single_file(
            path=cmd_line_args.files,
            out_path=cmd_line_args.out_path,
            pandoc=pandoc_path,
        )

    out_path = cmd_line_args.out_path

    if path.basename(out_path) == "" or path.isdir(out_path):
        print("Output to directory {dir}".format(dir=out_path))
    else:
        print("Output to file {file}".format(file=out_path))

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
                        convert_single_file(
                            path=in_file,
                            out_path=out_file,
                            pandoc=pandoc_path,
                        )

        elif path.isfile(arg_path):
            convert_single_file(path=arg_path, out_path=out_path, pandoc=pandoc_path)
        else:
            cmd_line_parser.print_help()
            cmd_line_parser.error(
                "no markdown files found in path '{path}'".format(path=arg_path)
            )
