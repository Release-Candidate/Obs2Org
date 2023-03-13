# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  obs2org
# File:     test_main.py
# Date:     07.Nov.2021
#
# ==============================================================================
"""Test Obs2Org by executing the program's main function with various arguments."""

import filecmp
import runpy
import shutil
import sys
from typing import List
from unittest import mock

import pytest


################################################################################
def run_obs2org(cmd_line_args: List[str]) -> None:
    """Run the program with the given arguments.

    Returns the output of the command in the tuple `stdout, stderr`. The first element
    of the tuple holds the process' output on `stdout`, the second the output on
    `stderr`.

    Args:
        cmd_line_args (List[str]): The arguments to pass to the program's main.
    """
    sys_argv_list = [""]
    sys_argv_list.extend(cmd_line_args)
    sys.argv = sys_argv_list

    runpy.run_module("obs2org", run_name="__main__")


################################################################################
def test_python_version() -> None:
    """Tests the check of the Python version."""
    with mock.patch.object(sys, "version_info") as mock_vers:
        mock_vers.major = 3
        mock_vers.minor = 6
        with pytest.raises(expected_exception=SystemExit) as excp:
            runpy.run_module("obs2org", run_name="__main__")
        assert excp.value.args[0] == 1  # nosec


################################################################################
def test_version_string(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the output of a version string."""
    with pytest.raises(expected_exception=SystemExit) as excp:
        run_obs2org(["--version"])

    assert excp.value.args[0] == 0  # nosec
    captured = capsys.readouterr()
    assert captured.err == ""  # nosec
    assert captured.out.find("obs2org") == 0  # nosec


################################################################################
def test_illegal_arg() -> None:
    """Test an illegal argument."""
    with pytest.raises(expected_exception=SystemExit) as excp:
        run_obs2org(["--HASD"])
    assert excp.value.args[0] == 2  # nosec


################################################################################
def test_show_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the output of the help text."""
    with pytest.raises(expected_exception=SystemExit) as excp:
        run_obs2org(["--help"])

    assert excp.value.args[0] == 0  # nosec
    captured = capsys.readouterr()
    assert captured.err == ""  # nosec
    assert captured.out.find("usage: python -m obs2org [-h] [-V]") == 0  # nosec


################################################################################
def test_illegal_markdown() -> None:
    """Test an illegal markdown input path."""
    with pytest.raises(expected_exception=SystemExit) as excp:
        run_obs2org(["./does_not_exist/"])
    assert excp.value.args[0] == 2  # nosec


################################################################################
def test_illegal_org_mode() -> None:
    """Test an illegal Org-Mode output file."""
    with pytest.raises(expected_exception=SystemExit) as excp:
        run_obs2org(["-o ./does_not_exist.org"])
    assert excp.value.args[0] == 2  # nosec


################################################################################
def test_illegal_pandoc() -> None:
    """Test an illegal pandoc command."""
    with pytest.raises(expected_exception=SystemExit) as excp:
        run_obs2org(["-p does_not_exist"])
    assert excp.value.args[0] == 2  # nosec


################################################################################
def test_convert_test1(capsys: pytest.CaptureFixture[str]) -> None:
    """Test conversion of `fixture/dir/test1.md`."""
    run_obs2org(["./tests/fixtures/dir/test1.md", "-o", "test_out/"])

    captured = capsys.readouterr()
    assert captured.err == ""  # nosec
    assert captured.out.find("OK") > 1  # nosec
    assert (  # nosec
        filecmp.cmp(
            "./test_out/test1.org",
            "./tests/fixtures/test1_orig.org",
            shallow=False,
        )
        is True
    )


################################################################################
def test_convert_test2(capsys: pytest.CaptureFixture[str]) -> None:
    """Test conversion of `fixture/dir/test1.md` and `fixture/test2.md`."""
    run_obs2org(["./tests/fixtures/", "-o=test_out/"])

    captured = capsys.readouterr()
    assert captured.err == ""  # nosec
    assert captured.out.find("OK") > 1  # nosec
    assert (  # nosec
        filecmp.cmp(
            "./test_out/dir/test1.org",
            "./tests/fixtures/test1_orig.org",
            shallow=False,
        )
        is True
    )
    assert (  # nosec
        filecmp.cmp(
            "./test_out/test2.org",
            "./tests/fixtures/test2_orig.org",
            shallow=False,
        )
        is True
    )
    assert (  # nosec
        filecmp.cmp(
            "./test_out/dir1/Test 3.org",
            "./tests/fixtures/Test 3_orig.org",
            shallow=False,
        )
        is True
    )
