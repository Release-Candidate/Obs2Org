# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath("../../../"))

from PYTHON_TEMPLATE import VERSION  # noqa: E402


# -- Project information -----------------------------------------------------

project = "PYTHON_TEMPLATE"
copyright = "2021, Release-Candidate"
author = "Release-Candidate"
version = VERSION

# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Date format used to replace the tag |today|
today = ""
today_fmt = "%d.%m.%Y"

# Trim spaces before footnote references that are necessary for the reST parser
# to recognize the footnote, but do not look too nice in the output.
trim_footnote_reference_space = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_show_sourcelink = False

html_copy_source = False

html_last_updated_fmt = "%d.%m.%Y"

# Show copyright footer
html_show_copyright = False

# Show 'build with Sphinx' footer
html_show_sphinx = False

html_theme_options = {
    "analytics_anonymize_ip": True,
    "logo_only": False,
    "display_version": False,
    "prev_next_buttons_location": "both",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#5DB1DE",
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# Pygments source code style to use
# abap, algol, algol_nu, arduino, autumn, borland, bw, colourful,
# emacs, friendly, fruity, igor, lovelace, manni, monokai, murphy,
# native, paraiso_dark, paraiso_light, pastie, perldoc, rainbow_dash
# rrt, sas, stata, tango, trac, vim, vs, xcode
pygments_style = "tango"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
