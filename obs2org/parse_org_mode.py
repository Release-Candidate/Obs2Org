# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Obs2Org
# File:     parse_org_mode.py
# Date:     02.11.2021
# ===============================================================================
"""Parses a generated Org-Mode file and corrects the links to headers/seactions
in other Org-Mode files, convert tags to Org-Mode tags and put dates on a line in
angle brackets.
"""

from __future__ import annotations, with_statement

import re
from pathlib import Path
from typing import Match

# The first match group is the filename without suffix, the second match group
# is the header name in the file to link to.
_internal_wikilink_regexp = re.compile(r"\[\[(\w[^\[\]]*)#(\w[^\[\]]*)\]\]")

# Date regexp, to get all variants of year, month and day placements and the
# delimiters between them. Date must be on a line of it's own.
_date_regexp = re.compile(
    r"^\s*(\d{1,4}[0-9.,/\\ -]\d{1,4}[0-9.,/\\ -]\d{1,4})\s*$", flags=re.MULTILINE
)

# Tag regexp, that captures the heading in the first match group, the list of
# tags in the third match group and anything in between in the second match
#  group.
_tag_regexp = re.compile(
    r"^(\s*\*{1,}\s[^\n]{1,})$([^*]*?)^\s*Keywords:\s*((?:#\S[^\n#,]*,?[^\S\n]*){1,})$",
    flags=re.MULTILINE,
)

# Regexp to convert a comma separated list of hash-tags to Org-Mode style
# hash-tags.
_tag_convert_regex = re.compile(r"(?:^\s*#)|(?:\s*,\s*#)|(?:$)")


###############################################################################
def correct_org_mode_file(text: str, directory: Path) -> str:
    """Parse Org-Mode formatted text and correct wiki-style links, tags and date strings.

    Corrects wiki-style links to headings in other Org-Mode files,
    corrects hash-tags to Org-Mode tags and adds angle brackets to
    date strings.

    Parameters
    ----------
    text : str
        The Org-Mode text to parse.
    directory : Path
        The directory the Org-Mode files to link to are located in.

    Returns
    -------
    str
        Returns the corrected Org-Mode text.
    """
    correcteg_tags = correct_org_mode_tags(text=text)
    corrected_dates = correct_org_mode_date(text=correcteg_tags)
    corrected_links = correct_org_mode_links(text=corrected_dates, dir=directory)
    return corrected_links


###############################################################################
def correct_org_mode_tags(text: str) -> str:
    """Convert the hashtags of `text` to Org-Mode tags.

    Searches for hashtags in the text and pastes them in Org-Mode
    format after the heading they are located in.

    Parameters
    ----------
    text : str
        The text to parse and correct the tags in.

    Returns
    -------
    str
        The given Org-Mode text with tags in Org-Mode format.

    Examples
    --------
    Converts the lines

    * Heading
      :PROPERTIES:
      :CUSTOM_ID: heading
      :END:
    Keywords: #tag1, #tag2

    to the Org-Mode format tags

    * Heading         :tag1:tag2:
      :PROPERTIES:
      :CUSTOM_ID: heading
      :END:
    """

    def replace_func(match_obj: Match[str]) -> str:
        """Return the `_tag_regexp` matches in the correct Org-Mode tag format.

        Parameters
        ----------
        match_obj : Match[str]
            The `Match` object containing the 3 match groups of
            `_tag_regexp`.

        Returns
        -------
        str
            The Org-Mode formatted replaced tags in the heading.
        """
        return (
            match_obj.group(1)
            + "\t\t\t"
            + _tag_convert_regex.sub(r":", match_obj.group(3))
            + match_obj.group(2)
        )

    return _tag_regexp.sub(repl=replace_func, string=text)


###############################################################################
def correct_org_mode_date(text: str) -> str:
    """Search for dates on a line of it's own and add angle brackets to it.

    Search `text` for dates and add angle brackets to it so that
    Org-Mode knows about that date.

    Parameters
    ----------
    text : str
        The Org-Mode text to parse.

    Returns
    -------
    str
        The modified Org-Mode text.

    Examples
    --------
    `2021-05-28` is replaced by `<2021-05-28>`.
    """
    return _date_regexp.sub(r"<\1>", text)


###############################################################################
def correct_org_mode_links(text: str, dir: Path) -> str:
    """Correct wiki-style links in the Org-Mode text.

    Search for links to headings in other Org-Mode files and replace
    them with a working link to the section in this ORg-mode file.

    Parameters
    ----------
    text : str
        The Org-Mode text to parse and correct.
    dir : Path
        The directory the Org-Mode files to link to are located in.

    Returns
    -------
    str
        The modified Org-Mode text with working links.

    Examples
    --------
    `[[books#My Heading]]` is changed to
    `[[file:books.org::#my-heading][My Heading]]`.
    """

    def replace_func(match_obj: Match[str]) -> str:

        file_name: Path = dir / Path(match_obj.group(1) + ".org")
        heading_name = match_obj.group(2)
        heading_name_regexp = re.sub(
            string=heading_name, repl=r"[\\W]{1,}", pattern=r"^|\s|$"
        )
        header_link = ""
        with file_name.open(mode="r", encoding="utf-8") as fd:
            file_text = fd.read()
            header_pattern = (
                r"\*{1,}\s*"
                + heading_name_regexp
                + r"\s*[\w:.-]*\s*.*?\s*:CUSTOM_ID:\s*([\w.-]{1,})$"
            )
            file_match = re.search(
                pattern=header_pattern, string=file_text, flags=re.MULTILINE
            )
            if file_match is not None:
                header_link = "::#" + file_match.group(1)

        return "[[file:" + file_name.name + header_link + "][" + heading_name + "]]"

    return _internal_wikilink_regexp.sub(repl=replace_func, string=text)
