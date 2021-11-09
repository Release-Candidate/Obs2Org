Obs2Org
=======

Obs2Org is a cross platform command (works on \*BSD, Linux, OS X and
Windows) line program to convert `Obsidian <https://obsidian.md/>`__
style Markdown files to `Org-Mode <https://orgmode.org/>`__ files for
Emacs and other Editors that support Org-Mode.

It converts the Markdown files using
`Pandoc <https://pandoc.org/MANUAL.html>`__ and afterwards corrects the
links to headings in other Org-Mode files, converts the hash-tag style
Obsidian tags to Org-Mode style tags and puts angle brackets around
dates.

Example
-------

Obs2Org converts a Markdown file like to following:

.. code:: md

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

to the following Org-Mode file:

.. code:: org-mode

   #+title: Programming

   * Programming              :Programming:
     :PROPERTIES:
     :CUSTOM_ID: programming
     :END:

   * Lisp
      :PROPERTIES:
      :CUSTOM_ID: lisp
      :END:

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

See `Installation <#installation>`__ and `Usage <#usage>`__ for
information on how to do that.

The PyPI (pip) package can be found at `Obs2Org at
PyPI <https://pypi.org/project/Obs2Org/>`__

Additional Documentation can be found at `Read the
Docs <https://obs2org.readthedocs.io/en/latest>`__


Installation
------------

Pandoc
~~~~~~

`Pandoc <https://pandoc.org>`__ is needed to do the actual conversion of
Markdown files to Org-Mode files.

See `Installing pandoc <https://pandoc.org/installing.html>`__ on how to
install Pandoc for your OS.

.. _obs2org-1:

Obs2Org
~~~~~~~

Python, at Least Version 3.9
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The PyPI Obs2Org Package
^^^^^^^^^^^^^^^^^^^^^^^^

Install the PyPI (pip) package ``obs2org`` for all users on your
computer as administrator/root:

-  Linux, OS X:

   .. code:: shell

      sudo pip install obs2org

-  Windows:

   Open an administrator shell by writing ``cmd`` in the search field of
   the taskbar, ricght click on the command app and select “Run as
   Adminsitrator”. in this shell execute:

   .. code:: ps1

      pip install obs2org

Usage
-----

Use Obs2Org by running it as a normal user (**not** administrator or
root) as Python module using

-  Linux, OSX:

   .. code:: shell

      python3 -m obs2org --version

-  Windows

   .. code:: ps1

      python -m obs2org --version

This should yield the version string like

.. code:: ps1

   > python -m obs2org --version
   obs2org 1.0.0

To get a text explaining the usage of Obs2Org, use the argument
``--help`` or the short form ``-h``:

Windows:

.. code:: ps1

   python -m obs2org --help

Linux, OS X:

.. code:: shell

   python3 -m obs2org --help

Output:

.. code:: ps1

   > python -m obs2org --help

   usage: python -m obs2org [-h] [-V] [-p PANDOC] [-o OUT_PATH] [MARKDOWN_FILES ...]

   Converts markdown formatted files to Org-Mode formatted files using Pandoc.

   positional arguments:
     MARKDOWN_FILES        The path to the markdown files or directory to convert to
     ...

Examples
~~~~~~~~

These examples only work if Pandoc is in the PATH of your shell. If it
isn’t you can add the path to Pandoc by using the argument ``--pandoc``
or ``-p``.

To set the path to Pandoc to ``c:/pandoc/pandoc`` add
``--pandoc c:/pandoc/pandoc`` or ``-p c:/pandoc/pandoc`` to each
invocation of Obs2Org.

Example:

.. code:: ps1

   python -m obs2org ./Markdown ../Org --pandoc c:/pandoc/pandoc

1. current directory

   .. code:: ps1

      python -m obs2org

   Which is the same as

   .. code:: ps1

      python -m obs2org ./

   Converts all markdown files with a suffix of ``.md`` in the current
   working directory and all its subdirectories to files in Org-Mode
   format with the same base filename but a ``.org`` suffix.

2. one file

   .. code:: ps1

      python -m obs2org hugo.md -o sepp.org

   Converts the markdown document ``hugo.md`` to an Org-Mode document
   named ``sepp.org``.

3. all files with extension ``.md``

   .. code:: ps1

      python -m obs2org *.md

   Converts all markdown files with a suffix of ``.md`` in the current
   working directory to files in Org-Mode format with the same base
   filename but a ``.org`` suffix.

4. convert files to given directory

   .. code:: ps1

      python -m obs2org *.md ../Org

   Converts all markdown files with a suffix of ``.md`` in the current
   working directory to files in Org-Mode format with the same base
   filename but a ``.org`` suffix in the directory ``../Org``.

5. convert files in given directory to other directory

   .. code:: ps1

      python -m obs2org ./Markdown ../Org

   Converts all markdown files with a suffix of ``.md`` in the directory
   ``./Markdown`` and its subdirectories to files in Org-Mode format
   with the same base filename but a ``.org`` suffix in the directory
   ``../Org``.
