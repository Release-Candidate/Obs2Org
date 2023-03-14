# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Obs2Org
# File:     parse_org_mode.py
# Date:     02.11.2021
# ===============================================================================
"""Parses a generated Org-Mode file and corrects the links to headers/sections
in other Org-Mode files, convert tags to Org-Mode tags and put dates on a line
in angle brackets.
"""

from __future__ import annotations

import re
from pathlib import Path, PurePath
from typing import Match, Tuple
from uuid import uuid4

# The first match group is the filename without suffix, the second match group
# is the header name in the file to link to.
# Not matching files with suffixes.
# `[[file#Heading]]` -> `file.org`, `#Heading`
_internal_wikilink_regexp: re.Pattern[str] = re.compile(
    r"\[\[(?!https?|ftp|file|cite|.*\.\w+)(\S[^\[\]]*)#(\S[^\[\]]*?)(?:\|.*)?\]\]"
)

# The first match group is the filename without suffix.
# `[[Heading]]` -> `Heading.org`, `#Heading`
# Not converting files with suffixes: `[[File.sfx]]`
# Not converting links starting with `http`, `https` or `ftp`
# `[[http://not/converted]]`
_internal_wikilink_regexp_file_only: re.Pattern[str] = re.compile(
    r"\[\[(?!\*|https?|ftp|file|cite|[^\[\]]*\.[^В\s]+\])\s*([^#|\[\]]*)\s*\]\]"
)

# The first match group is the heading to link to.
# `[[#Heading]]` -> `#Heading`
_internal_wikilink_same_doc_regexp: re.Pattern[str] = re.compile(
    r"\[\[\s*#\s*([^#|\[\]]*)\s*\]\]"
)

# The first ,match group is the filename, the second the link's caption.
# `[[file|Caption]]` -> `file`, `#Caption`
# Not matching files with a suffix.
_internal_wikilink_named_regexp: re.Pattern[str] = re.compile(
    r"\[\[(?!#)(?!.*\.\w+)(\S[^\[\]]*?)(?:#\^?\w+)?(?:#page=\d+)?\|(?:\S[^\[\]]*)\]\]"
)

# The first, match group is the heading to link to.
# `[[#Caption]]` -> `[[*Caption]]`
# Not matching files with a suffix.
_internal_header_named_regexp: re.Pattern[str] = re.compile(
    r"\[\[(?!.*\.\w+)(#\w[^\[\]]*?)(?:#\^?\w+)?(?:#page=\d+)?\|(\S[^\[\]]*)\]\]"
)

# The first ,match group is the filename, the second the link's caption.
# `[[file.sfx|Caption]]` -> `file.sfx`, `#Caption`
_file_wikilink_named_regexp: re.Pattern[str] = re.compile(
    r"\[\[(?!#)(\S[^\[\]]*?\.\w+)(?:#\^?\w+)?(?:#page=\d+)?\|(\S[^\[\]]*)\]\]"
)

# The first ,match group is the filename, the second the link's caption.
# `[[file.sfx]]` -> `file.sfx`
_file_wikilink_regexp: re.Pattern[str] = re.compile(
    r"\[\[(?!#|(?:file|http[s]?|ftp|zotero|cite:))(\S[^\[\]]*?\.[^В\s]+?)(?:#\^?\w+)?(?:#page=\d+)?\]\]"
)

# Date regexp, to get all variants of year, month and day placements and the
# delimiters between them. Date must be on a line of it's own.
_date_regexp: re.Pattern[str] = re.compile(
    r"^\s*(\d{1,4}[0-9.,/\\ -]\d{1,4}[0-9.,/\\ -]\d{1,4})\s*$", flags=re.MULTILINE
)

# Tag regexp, that captures the heading in the first match group, the list of
# tags in the third match group and anything in between in the second match
#  group.
_tag_regexp: re.Pattern[str] = re.compile(
    r"^(\s*\*{1,}\s[^\n]{1,})$([^*]*?)^\s*Keywords:\s*((?:#\S[^\n#,]*,?[^\S\n]*){1,})$",
    flags=re.MULTILINE,
)

# Regexp to convert a comma separated list of hash-tags to Org-Mode style
# tags.
_tag_convert_regex = re.compile(r"(?:^\s*#)|(?:\s*,\s*#)|(?:$)")


# Regexp to remove all characters from a tag, that Org-Mode doesn't like.
_tag_remove_special_regex = re.compile(r"[^\w:]")

# Contains the actual link (including the '@') the the first match group.
# `[[cite:@Link]]` -> `@Link`
_cite_regex: re.Pattern[str] = re.compile(r"\[\[\s*cite:(@.*?)\s*\]\]")

# Pattern to match an Org-Roam file header.
_header_regex: re.Pattern[str] = re.compile(
    r"^\s*:PROPERTIES:\s*\n\s*:ID:\s*\S+\s*\n\s*:END:"
)

# Pattern to match the beginning of the file.
_start_of_file_regex: re.Pattern[str] = re.compile(r"^")


###############################################################################
def correct_org_mode_file(
    text: str,
    directory: Path,
    remove_citations: bool,
    add_uuid: bool,
) -> str:
    """Parse Org-Mode formatted text and correct wiki-style links, tags and
    date strings.

    Corrects wiki-style links to headings in other Org-Mode files,
    corrects hash-tags to Org-Mode tags and adds angle brackets to
    date strings.

    Parameters
    ----------
    text : str
        The Org-Mode text to parse.
    directory : Path
        The directory the Org-Mode files to link to are located in.
    remove_citations : bool
        Whether to remove Pandoc-style citations to treat them as normal links,
        or not.
    add_uuid : bool
        Whether to add an UUID-header to each file.

    Returns
    -------
    str
        Returns the corrected Org-Mode text.
    """
    corrected_tags = _correct_org_mode_tags(text=text)
    corrected_dates = _correct_org_mode_date(text=corrected_tags)
    if add_uuid:
        corrected_dates = _add_uuid_header(text=corrected_dates)
    if remove_citations:
        corrected_dates = _remove_pandoc_citations(text=corrected_dates)
    corrected_links = _correct_org_mode_links(text=corrected_dates, directory=directory)
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
def _add_uuid_header(text: str) -> str:
    """Add the Org-Roam UUID header to the start of the file if it doesn't
    already have one.

    :PROPERTIES:
    :ID: UUID
    :END:

    Parameters
    ----------
    text : str
        The content of the file.

    Returns
    -------
    str
        The file with an Org-Roam header added if it didn't already have one.
    """
    if _header_regex.match(string=text):
        return text
    uuid_string = f":PROPERTIES:\n:ID: {uuid4()}\n:END:\n"
    with_header = _start_of_file_regex.sub(repl=f"{uuid_string}\n", string=text)
    return with_header


###############################################################################
def _remove_pandoc_citations(text: str) -> str:
    """Remove Pandoc `cite` prefix from

    Parameters
    ----------
    text : str
        The content of the file to parse.

    Returns
    -------
    str
        The file content with removed `cite:` prefixes in links.
    """
    no_cites = _cite_regex.sub(repl=r"[[\1]]", string=text)
    return no_cites


###############################################################################
def _correct_org_mode_links(text: str, directory: Path) -> str:
    """Correct wiki-style links in the Org-Mode text.

    Search for links to headings in other Org-Mode files and replace
    them with a working link to the section in this ORg-mode file.

    Parameters
    ----------
    text : str
        The Org-Mode text to parse and correct.
    directory : Path
        The directory the Org-Mode files to link to are located in.

    Returns
    -------
    str
        The modified Org-Mode text with working links.

    Examples
    --------
    `[[books#My Heading]]` is changed to
    `[[file:books.org::#my-heading][My Heading]]`.

    `[[Note]]` is changed to
    `[[file:Note.org::#note][Note]]`.

    `[[#heading-id|Caption]]` is changed to
    `[[#heading-id][Caption]]`

    `[[file|Caption]]` is changed to
    `[[file][Caption]]`

    `[[#Heading]]` is changed to
    `[[*Heading]]`
    """
    first_pass = _internal_wikilink_regexp.sub(
        repl=lambda match_obj: _link_replace_func(
            match_obj=match_obj, directory=directory
        ),
        string=text,
    )
    second_pass = _internal_wikilink_same_doc_regexp.sub(
        repl=r"[[*\1]]", string=first_pass
    )

    third_pass = _internal_wikilink_named_regexp.sub(
        repl=lambda match_obj: _link_replace_func(
            match_obj=match_obj, directory=directory
        ),
        string=second_pass,
    )

    fourth_pass = _file_wikilink_named_regexp.sub(repl=r"[[\1][\2]]", string=third_pass)

    fifth_pass = _file_wikilink_regexp.sub(repl=r"[[file:\1]]", string=fourth_pass)

    sixth_pass = _internal_header_named_regexp.sub(
        repl=r"[[\1][\2]]", string=fifth_pass
    )

    return _internal_wikilink_regexp_file_only.sub(
        repl=lambda match_obj: _link_replace_func(
            match_obj=match_obj, directory=directory
        ),
        string=sixth_pass,
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
def _link_replace_func(match_obj: Match[str], directory: Path) -> str:
    """Search for the Org-Mode id of the given heading and replace that in
    the link.

    Open the file the link points to and search the id of the
    given heading and the real name of the heading. Replace the
    original link with a working link to the heading in the file,
    with the heading name as the link's title.

    Parameters
    ----------
    match_obj : Match[str]
        The `Match` object holding the filename and the heading
        name without special characters.
    directory : Path
        The directory the Org-Mode files to link to are located in.

    Returns
    -------
    str
        The working link to the heading in the file with the real
        heading as link title.
    """
    file_name: Path = directory / Path(match_obj.group(1) + ".org")
    if match_obj.lastindex == 1:
        heading_name = PurePath(match_obj.group(1)).name
    else:
        heading_name = match_obj.group(2)
    header_link = ""
    try:
        header_link, heading_name = _parse_linkedfile(
            file_name=file_name, heading_name=heading_name
        )
    except FileNotFoundError:
        print(
            f"Error, linked file '{file_name.absolute()}' has not been found, "
            f"link to section '{heading_name}' won't work!"
        )
    except OSError as excp:
        print(f"Error reading file '{file_name}': '{excp}'")
    except Exception as excp:
        print(f"Error reading file '{file_name}': {excp}")

    return (
        "[[file:"
        + match_obj.group(1)
        + ".org"
        + header_link
        + "]["
        + heading_name
        + "]]"
    )


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
    heading_name_regexp = heading_name.strip()

    with file_name.open(mode="r", encoding="utf-8") as f_d:
        file_text = f_d.read()
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
    """Parse the Org-Mode text `text` for the heading and return it's id and
    name.

    Parameters
    ----------
    text : str
        The Org-Mode text to parse.
    heading_name_regexp : str
        The regexp with which to search for the heading
    heading_name : str
        The name of the heading to search for.
    file_name : Path
        The name of the file to parse, for error messages only.

    Returns
    -------
    Tuple[str, str]
        A tuple `header_link`, `header_name` containing the headings
        id and the full name of the heading.
    """
    header_link = ""
    header_pattern = (
        r"^\s*\*{1,}\s*("
        + re.escape(heading_name_regexp)
        + r")\s*[\w:.-]+\s*.*?\s*^:CUSTOM_ID:\s*([^\s]+)$"
    )
    file_match = re.search(
        pattern=header_pattern, string=text, flags=re.MULTILINE | re.IGNORECASE
    )
    if file_match is not None:
        header_link = "::#" + file_match.group(2)
        heading_name = file_match.group(1).strip(":").strip()
    else:
        print(f"Error: heading {heading_name} not found in file {file_name.absolute()}")

    return header_link, heading_name
