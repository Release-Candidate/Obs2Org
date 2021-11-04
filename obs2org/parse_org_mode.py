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

from __future__ import annotations

import re
from pathlib import Path
from typing import Match, Tuple

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
# tags.
_tag_convert_regex = re.compile(r"(?:^\s*#)|(?:\s*,\s*#)|(?:$)")


# Regexp to remove all characters from a tag, that Org-Mode doesn't like.
_tag_remove_special_regex = re.compile(r"[^\w:]")


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
    correcteg_tags = _correct_org_mode_tags(text=text)
    corrected_dates = _correct_org_mode_date(text=correcteg_tags)
    corrected_links = _correct_org_mode_links(text=corrected_dates, dir=directory)
    return corrected_links


###############################################################################
def _correct_org_mode_tags(text: str) -> str:
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
    return _tag_regexp.sub(repl=_tag_replace_func, string=text)


###############################################################################
def _correct_org_mode_date(text: str) -> str:
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
def _correct_org_mode_links(text: str, dir: Path) -> str:
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
    return _internal_wikilink_regexp.sub(
        repl=lambda match_obj: _link_replace_func(match_obj=match_obj, dir=dir),
        string=text,
    )


###############################################################################
def _tag_replace_func(match_obj: Match[str]) -> str:
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
    tags = _tag_convert_regex.sub(repl=r":", string=match_obj.group(3))
    return (
        match_obj.group(1)
        + "\t\t\t"
        + _tag_remove_special_regex.sub(repl=r"", string=tags)
        + match_obj.group(2)
    )


###############################################################################
def _link_replace_func(match_obj: Match[str], dir: Path) -> str:
    """Search for the Org-Mode id of the given heading and replace that in the link.

    Open the file the link points to and search the id of the
    given heading and the real name of the heading. Replace the
    original link with a working link to the heading in the file,
    with the heading name as the link's title.

    Parameters
    ----------
    match_obj : Match[str]
        The `Match` object holding the filename and the heading
        name without special characters.
    dir : Path
        The directory the Org-Mode files to link to are located in.

    Returns
    -------
    str
        The working link to the heading in the file with the real
        heading as link title.
    """
    file_name: Path = dir / Path(match_obj.group(1) + ".org")
    heading_name = match_obj.group(2)
    header_link = ""
    try:
        header_link, heading_name = _parse_linkedfile(
            file_name=file_name, heading_name=heading_name
        )
    except FileNotFoundError:
        print(
            "Error, linked file '{file}' has not been found, link to section '{heading}' won't work!".format(
                file=file_name.absolute(), heading=heading_name
            )
        )

    return "[[file:" + file_name.name + header_link + "][" + heading_name + "]]"


###############################################################################
def _parse_linkedfile(file_name: Path, heading_name: str) -> Tuple[str, str]:
    """Parse the Org-Mode file at `file_name` for the id of the given heading.

    Return a tuple of strings `header_link`, `heading_name` with the
    id and the full name of the heading. If the heading has not been
    found, the id is the empty string `""` and heading_name is not the
    full name, but the argument `heading_name`.

    Parameters
    ----------
    file_name : Path
        The path to the file to parse.
    heading_name : str
        The heading name without special characters to search for.

    Returns
    -------
    Tuple[str, str]
        A tuple `header_link`, `header_name` containing the headings
        id and the full name of the heading.
    """
    heading_name_regexp = re.sub(
        string=heading_name, repl=r"[\\W]{1,}", pattern=r"^|\s|$"
    )

    with file_name.open(mode="r", encoding="utf-8") as fd:
        file_text = fd.read()
        header_link, heading_name = _parse_text_for_heading(
            text=file_text,
            file_name=file_name,
            heading_name_regexp=heading_name_regexp,
            heading_name=heading_name,
        )

    return header_link, heading_name


###############################################################################
def _parse_text_for_heading(
    text: str, heading_name_regexp: str, heading_name: str, file_name: Path
) -> Tuple[str, str]:
    """Parse the Org-Mode text `text` for the heading and return it's id and name.

    Parameters
    ----------
    text : str
        The Org-Mode text to parse.
    heading_name_regexp : str
        The rexept with which to search for the heading
    heading_name : str
        The name of the heading to search for.
    file_name : Path
        The name of the file to parse, for error mesages only.

    Returns
    -------
    Tuple[str, str]
        A tuple `header_link`, `header_name` containing the headings
        id and the full name of the heading.
    """
    header_link = ""
    header_pattern = (
        r"\*{1,}\s*("
        + heading_name_regexp
        + r")\s*[\w:.-]*\s*.*?\s*:CUSTOM_ID:\s*([\w.-]{1,})$"
    )
    file_match = re.search(pattern=header_pattern, string=text, flags=re.MULTILINE)
    if file_match is not None:
        header_link = "::#" + file_match.group(2)
        heading_name = file_match.group(1).strip(":").strip()
    else:
        print(
            "Error: heading {name} not found in file {file}".format(
                name=heading_name, file=file_name.absolute()
            )
        )

    return header_link, heading_name
