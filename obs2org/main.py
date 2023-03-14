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
import asyncio
import subprocess  # nosec
from os import path, walk
from pathlib import Path, PurePath
from typing import Coroutine, NamedTuple

from obs2org import VERSION
from obs2org.convert import convert_single_file, correct_org_mode


################################################################################
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

python -m obs2org *.md -o ../Org/

Converts all markdown files with a suffix of '.md' in the current working
directory to files in Org-Mode format with the same base filename but a
'.org' suffix in the directory '../Org'.

python -m obs2org ./Markdown -o ../Org/

Converts all markdown files with a suffix of '.md' in the directory
'./Markdown' and its subdirectories to files in Org-Mode format with
the same base filename but a '.org' suffix in the directory '../Org'.

See website https://github.com/Release-Candidate/Obs2Org for details."""


################################################################################
async def main() -> None:
    """The program's main entry point."""
    cmd_line_args, cmd_line_parser = _parse_command_line()

    await _convert_files(cmd_line_args=cmd_line_args, cmd_line_parser=cmd_line_parser)


###############################################################################
def _parse_command_line() -> tuple[argparse.Namespace, argparse.ArgumentParser]:
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
        version=f"obs2org {VERSION}",
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
        "-n",
        "--no-cite",
        action="store_true",
        dest="remove_citations",
        default=False,
        help="""If this flag is set, links like '[[@Name]]' are threaded
like normal links instead of Pandoc citations.
If this is not set, '[[@Name]]' is converted to '[[cite:@Name]]'""",
    )

    cmd_line_parser.add_argument(
        "-u",
        "--uuid",
        action="store_true",
        dest="generate_uuid",
        default=False,
        help="""If this flag is set, every file gets a header of the form
:PROPERTIES:
:ID: UUID
:END:
where UUID is a UUID like '16fd2706-8baf-433b-82eb-8c7fada847da'.""",
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
async def _convert_files(
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
    pandoc_path: str = _check_pandoc(
        cmd_line_args=cmd_line_args, cmd_line_parser=cmd_line_parser
    )

    if isinstance(cmd_line_args.files, list):
        path_list: list[str] = cmd_line_args.files
    else:
        path_list = [cmd_line_args.files]

    out_path = _check_out_path(
        cmd_line_args=cmd_line_args,
        cmd_line_parser=cmd_line_parser,
        path_list=path_list,
    )

    list_of_files: list[FilePaths] = []

    for arg_path in path_list:
        paths = _check_in_path(
            cmd_line_parser=cmd_line_parser,
            out_path=out_path,
            arg_path=arg_path,
        )
        list_of_files.extend(paths)

    await _do_convert_files(
        pandoc_path=pandoc_path,
        list_of_files=list_of_files,
        add_uuid=cmd_line_args.generate_uuid,
        remove_citations=cmd_line_args.remove_citations,
    )


################################################################################
def _check_pandoc(
    cmd_line_args: argparse.Namespace,
    cmd_line_parser: argparse.ArgumentParser,
) -> str:
    """Check if the given command to call Pandoc works.

    If the command does not work, the program is exited with an error message.

    Parameters
    ----------
    cmd_line_args : argparse.Namespace
        The object holding all command line arguments, the pandoc command too.
    cmd_line_parser : argparse.ArgumentParser
        The command line parser object to use.

    Returns
    -------
    str
        The command to call the Pandoc executable on success.
    """
    pandoc = cmd_line_args.pandoc_exe

    pandoc_version_arg = "--version"

    pandoc_out = subprocess.run(
        args=" ".join([pandoc, pandoc_version_arg]),
        check=False,
        shell=True,
        text=True,
        capture_output=True,
    )

    if pandoc_out.returncode != 0 and pandoc_out.stderr != "":
        cmd_line_parser.error(
            f"Pandoc executable '{pandoc}' not found or does not work!\n"
            f"Error message: '{pandoc_out.stderr.strip()}'\n"
            f"Look at https://pandoc.org/installing.html for information on how to install\n"
            f"pandoc"
        )

    return pandoc


################################################################################
def _check_in_path(
    cmd_line_parser: argparse.ArgumentParser,
    out_path: str,
    arg_path: str,
) -> list[FilePaths]:
    """Check, if the given path contains Markdown files and return the path to
    them and the Org-Mode file to generate.
    Return the empty list else.

    Parameters
    ----------
    cmd_line_parser : argparse.ArgumentParser
        The command line parser object to use.
    out_path : str
        The path to write the generated Org-Mode files to.
    arg_path : str
        The path to check for Markdown files.

    Returns
    -------
    list[FilePaths]
        The `FilePaths` of the Markdown file to convert and the Org-Mode file
        to generate.
    """
    ret_list: list[FilePaths] = []

    if path.isdir(arg_path):
        dir_path_list = _walk_directory(out_path=out_path, arg_path=arg_path)
        ret_list.extend(dir_path_list)

    elif path.isfile(arg_path):
        file_obj = Path(arg_path)
        out_file = path.join(out_path, file_obj.with_suffix(".org").name)
        ret_list.append(FilePaths(in_file=file_obj, out_file=Path(out_file)))

    else:
        cmd_line_parser.error(f"no markdown file(s) found at path '{arg_path}'.")

    return ret_list


################################################################################
def _walk_directory(out_path: str, arg_path: str) -> list[FilePaths]:
    """Walk through the directory `arg_path` and add all Markdown files to the
    list of files to convert.

    Parameters
    ----------
    out_path : str
        The path to write the generated Org-Mode files to.
    arg_path : str
        The directory to search for Markdown files.

    Returns
    -------
    list[FilePaths]
        A list of found Markdown files and the paths to the Org-Mode file to
        generate.
    """
    ret_list: list[FilePaths] = []
    for dirpath, _, filenames in walk(top=arg_path, topdown=True, followlinks=True):
        rel_dirpath = path.relpath(dirpath, arg_path)
        out_dir = path.join(out_path, rel_dirpath)
        Path(out_dir).mkdir(exist_ok=True, parents=True)
        for file in filenames:
            file_object = PurePath(file)
            if file_object.suffix == ".md":
                in_file = path.join(dirpath, file)
                out_file = path.join(out_dir, file_object.with_suffix(".org"))
                ret_list.append(
                    FilePaths(in_file=Path(in_file), out_file=Path(out_file))
                )

    return ret_list


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
        print(f"Output to directory {out_path}")
        Path(out_path).mkdir(exist_ok=True, parents=True)
    else:
        print(f"Output to file {out_path} {len(path_list)}")
        if len(path_list) >= 1:
            cmd_line_parser.error(
                f"more than one markdown file to convert given,"
                f" but just one output file '{out_path}'!"
            )

    return out_path


################################################################################
async def _do_convert_files(
    pandoc_path: str,
    list_of_files: list[FilePaths],
    remove_citations: bool,
    add_uuid: bool,
) -> None:
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
    remove_citations : bool
        Whether to remove Pandoc-style citations to treat them as normal links,
        or not.
    add_uuid : bool
        Whether to add an UUID-header to each file.
    """
    convert_tasks: list[Coroutine[object, object, object]] = []
    for convert_file in list_of_files:
        convert_tasks.append(
            asyncio.to_thread(
                convert_single_file,
                convert_file.in_file,
                convert_file.out_file,
                pandoc_path,
            )
        )

    await asyncio.gather(*convert_tasks)

    # Can't run this asynchronously, as
    # we need to look up headings in converted files.
    for correct_file in list_of_files:
        correct_org_mode(
            correct_file.out_file, remove_citations=remove_citations, add_uuid=add_uuid
        )
