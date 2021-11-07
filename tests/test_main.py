# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  obs2org
# File:     test_main.py
# Date:     07.Nov.2021
#
# ==============================================================================
"""Test Obs2Org by executing the program's main function with various arguments."""

import runpy
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
