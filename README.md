# Obs2Org <!-- omit in TOC -->

[![GPLv3 license badge](https://img.shields.io/github/license/Release-Candidate/Obs2Org)](https://github.com/Release-Candidate/Obs2Org/blob/main/LICENSE)
[![Python version badge](https://img.shields.io/pypi/pyversions/Obs2Org)](https://www.python.org/downloads/)
[![PIP version badge](https://img.shields.io/pypi/v/Obs2Org)](https://pypi.org/project/Obs2Org/)
[![Read The Docs badge](https://readthedocs.org/projects/obs2org/badge/?version=latest)](https://obs2org.readthedocs.io/en/latest/?badge=latest)
![OS badge](https://img.shields.io/badge/Runs%20on-Linux%7COS%20X%7CWindows-brightgreen?style=flat)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[more badges](#badges)

Obs2Org is a cross platform command (works on *BSD, Linux, OS X and Windows) line program to convert [Obsidian](https://obsidian.md/) style Markdown files to [Org-Mode](https://orgmode.org/) files for Emacs and other Editors that support Org-Mode.

It converts the Markdown files using [Pandoc](https://pandoc.org/MANUAL.html) and afterwards corrects the links to headings in other Org-Mode files, converts the hash-tag style Obsidian tags to Org-Mode style tags and puts angle brackets around dates.

## Example

Obs2Org converts a Markdown file like to following:

```md
---
title: "Programming"
author:
  -
keywords:
  - Programming
tags:
  - Programming
lang: en
---
# Programming

Keywords: #Programming

## Lisp

### Books

Keywords: #Lisp, #Book

- Lisp Cookbook, 'recipies' to solve common problems using Lisp: [[Books#Lisp Cookbook]]
- **Peter Seibel**: *Practical Common Lisp*: [[Books#Practical Common Lisp]]
- **Peter Norvig**: *Paradigms of Artificial Intelligence Programming: Case Studies in Common Lisp*: [[Books#Paradigms of Artificial Intelligence Programming]]

### State of the Common Lisp ecosystem, 2020

2021-10-08

Keywords: #Lisp, #Ecosystem, #2020

Editors, libraries, compilers, ...
[State of the Common Lisp ecosystem, 2020](https://lisp-journey.gitlab.io/blog/state-of-the-common-lisp-ecosystem-2020/#development)

```

to the following Org-Mode file:

```org
#+title: Programming

* Programming              :Programming:
  :PROPERTIES:
  :CUSTOM_ID: programming
  :END:

* Lisp
   :PROPERTIES:
   :CUSTOM_ID: lisp
   :END:
<20211008211713>
*** Books   :Lisp:Book:
    :PROPERTIES:
    :CUSTOM_ID: bücher-1
    :END:


- Lisp Cookbook, 'recipies' to solve common problems using Lisp: [[file:Books.org::#lisp-cookbook][Lisp Cookbook]]
- *Peter Seibel*: /Practical Common Lisp/: [[file:Books.org::#practical-common-lisp][Practical Common Lisp]]
- *Peter Norvig*: /Paradigms of Artificial Intelligence Programming: Case Studies in Common Lisp/: [[file:Books.org::#paradigms-of-artificial-intelligence-programming][Paradigms of Artificial Intelligence Programming]]

*** State of the Common Lisp ecosystem, 2020   :Lisp:Ecosystem:2020:
    :PROPERTIES:
    :CUSTOM_ID: state-of-the-common-lisp-ecosystem-2020
    :END:
<2021-10-08>
Editors, libraries, compilers, ... [[https://lisp-journey.gitlab.io/blog/state-of-the-common-lisp-ecosystem-2020/#development][State of the Common Lisp ecosystem, 2020]]
```

See [Installation](#installation) and [Usage](#usage) for information on how to do that.

The PyPI (pip) package can be found at [Obs2Org at PyPI](https://pypi.org/project/Obs2Org/)

Additional Documentation can be found at [Read the Docs](https://obs2org.readthedocs.io/en/latest)

## Table of Contents <!-- omit in TOC -->

- [Example](#example)
- [Installation](#installation)
  - [Pandoc](#pandoc)
  - [Obs2Org](#obs2org)
    - [Python, at Least Version 3.9](#python-at-least-version-39)
    - [The PyPI Obs2Org Package](#the-pypi-obs2org-package)
- [Usage](#usage)
  - [Examples](#examples)
- [Development](#development)
  - [Python, version > 3.9](#python-version--39)
  - [Setup](#setup)
  - [Scripts](#scripts)
  - [Documentation](#documentation)
  - [Sources](#sources)
- [License](#license)
- [Badges](#badges)
  - [External Checks](#external-checks)
  - [Static Code Checks](#static-code-checks)
  - [Tests](#tests)

## Installation

### Pandoc

[Pandoc](https://pandoc.org) is needed to do the actual conversion of Markdown files to Org-Mode files.

See [Installing pandoc](https://pandoc.org/installing.html) on how to install Pandoc for your OS.

### Obs2Org

#### Python, at Least Version 3.9

#### The PyPI Obs2Org Package

Install the PyPI (pip) package `obs2org` for all users on your computer as administrator/root:

- Linux, OS X:

    ```shell
    sudo pip install obs2org
    ```

- Windows:

   Open an administrator shell by writing `cmd` in the search field of the taskbar, ricght click on the command app and select "Run as Adminsitrator".
   in this shell execute:

   ```ps1
   pip install obs2org
   ```

## Usage

Use Obs2Org by running it as a normal user (**not** administrator or root) as Python module using

- Linux, OSX:

    ```shell
    python3 -m obs2org --version
    ```

- Windows

    ```ps1
    python -m obs2org --version
    ```

This should yield the version string like

```ps1
> python -m obs2org --version
obs2org 1.0.0
```

To get a text explaining the usage of Obs2Org, use the argument `--help` or the short form `-h`:

Windows:

```ps1
python -m obs2org --help
```

Linux, OS X:

```shell
python3 -m obs2org --help
```

Output:

```ps1
> python -m obs2org --help

usage: python -m obs2org [-h] [-V] [-p PANDOC] [-o OUT_PATH] [MARKDOWN_FILES ...]

Converts markdown formatted files to Org-Mode formatted files using Pandoc.

positional arguments:
  MARKDOWN_FILES        The path to the markdown files or directory to convert to
  ...
```

### Examples

These examples only work if Pandoc is in the PATH of your shell. If it isn't you can add the path to Pandoc by using the argument `--pandoc` or `-p`.

To set the path to Pandoc to `c:/pandoc/pandoc` add `--pandoc c:/pandoc/pandoc` or `-p c:/pandoc/pandoc` to each invocation of Obs2Org.

Example:

```ps1
python -m obs2org ./Markdown ../Org --pandoc c:/pandoc/pandoc
```

1. current directory

    ```ps1
    python -m obs2org
    ```

    Which is the same as

    ```ps1
    python -m obs2org ./
    ```

    Converts all markdown files with a suffix of `.md` in the current working
    directory and all its subdirectories to files in Org-Mode format with the
    same base filename but a `.org` suffix.

2. one file

    ```ps1
    python -m obs2org hugo.md -o sepp.org
    ```

    Converts the markdown document `hugo.md` to an Org-Mode document named
    `sepp.org`.

3. all files with extension `.md`

    ```ps1
    python -m obs2org *.md
    ```

    Converts all markdown files with a suffix of `.md` in the current working
    directory to files in Org-Mode format with the same base filename but a
    `.org` suffix.

4. convert files to given directory

    ```ps1
    python -m obs2org *.md ../Org
    ```

    Converts all markdown files with a suffix of `.md` in the current working
    directory to files in Org-Mode format with the same base filename but a
    `.org` suffix in the directory `../Org`.

5. convert files in given directory to other directory

    ```ps1
    python -m obs2org ./Markdown ../Org
    ```

    Converts all markdown files with a suffix of `.md` in the directory
    `./Markdown` and its subdirectories to files in Org-Mode format with
    the same base filename but a `.org` suffix in the directory `../Org`.

## Development

### Python, version > 3.9

You need Python 3.9 or newer.

### Setup

1. Run `pipenv install --dev` to install the Python environment in the project directory
2. Run `pipenv run pre-commit install` to install the pre commit hooks to git. Now every time you commit a change, the linters are run.

   - To run the pre commit checks manually: `pipenv run pre-commit run --all-files`

### Scripts

- [](./make_package.sh) - Linux, OS X: build the Obs2Org PyPI package
- [./make_package.bat](./make_package.bat) - Windows: build the Obs2Org PyPI package. This is disabled on Windows, because the scripts would not be executable because of the Windows filesystem.
- [./run_local_linters.sh](./run_local_linters.sh) - Linux, OS X: run all configured linters on the Source code and tests.
- [./run_local_linters.bat](./run_local_linters.bat) - Windows: run all configured linters on the Source code and tests.
- [./run_tests.sh](./run_tests.sh) - Linux, OS X: run all tests.
- [./run_tests.bat](./run_tests.bat) - Windows: run all tests.

### Documentation

Ths source files for the [Read the Docs](https://obs2org.readthedocs.io/en/latest) site are located in the directory [./obs2org/doc/source](./obs2org/doc/source)

### Sources

The sources of the program are in the directory [./obs2org/](./obs2org/), the test sources and fixtures in [./tests/](./tests/)

## License

Obs2ORg ist licensed under the GPLv3.0, see file [LICENCE](./LICENSE).

## Badges

### External Checks

[![DeepSource](https://deepsource.io/gh/Release-Candidate/Obs2Org.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/Release-Candidate/Obs2Org/?ref=repository-badge)
[![Maintainability](https://api.codeclimate.com/v1/badges/023820a03165a9846d8c/maintainability)](https://codeclimate.com/github/Release-Candidate/Obs2Org/maintainability)
[![codecov](https://codecov.io/gh/Release-Candidate/Obs2Org/branch/main/graph/badge.svg?token=VAYTZWLGPO)](https://codecov.io/gh/Release-Candidate/Obs2Org)

### Static Code Checks

[![Bandit](https://github.com/Release-Candidate/Obs2Org/actions/workflows/bandit.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/bandit.yml)
[![Black](https://github.com/Release-Candidate/Obs2Org/actions/workflows/black.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/black.yml)
[![Flake8](https://github.com/Release-Candidate/Obs2Org/actions/workflows/flake8.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/flake8.yml)
[![Pycodestyle](https://github.com/Release-Candidate/Obs2Org/actions/workflows/pycodestyle.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/pycodestyle.yml)
[![Pydocstyle](https://github.com/Release-Candidate/Obs2Org/actions/workflows/pydocstyle.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/pydocstyle.yml)
[![Pyflakes](https://github.com/Release-Candidate/Obs2Org/actions/workflows/pyflakes.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/pyflakes.yml)

### Tests

[![Mac OS X latest](https://github.com/Release-Candidate/Obs2Org/actions/workflows/osx.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/osx.yml)
[![Tests Mac OS X latest](https://github.com/Release-Candidate/Obs2Org/actions/workflows/osx_test.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/osx_test.yml)
[![Ubuntu 20.04](https://github.com/Release-Candidate/Obs2Org/actions/workflows/linux.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/linux.yml)
[![Tests Ubuntu 20.04](https://github.com/Release-Candidate/Obs2Org/actions/workflows/linux_test.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/linux_test.yml)
[![Windows 2019](https://github.com/Release-Candidate/Obs2Org/actions/workflows/windows.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/windows.yml)
[![Tests Windows 2019](https://github.com/Release-Candidate/Obs2Org/actions/workflows/windows_test.yml/badge.svg)](https://github.com/Release-Candidate/Obs2Org/actions/workflows/windows_test.yml)
