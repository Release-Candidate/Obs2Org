# Obs2Org Changelog

## Version 1.3.0 (2023-03-14)

- Make the error message less cluttered.
- Add option `-u|--uuid` to add an UUID header to every file that doesn't have one.
- Add option `-n|--no-cite` to treat `[[@file]]` links as files instead of Pandoc citations.

### Bugfixes

- Fix the check for the output directory that didn't work. If more than one file to convert is given, the output argument must be a directory, not a single file.

### Internal Changes

- Change the format strings to 'f-strings'.
- Add pylint to `run_local_linters` scripts.

## Version 1.2.0 (2023-03-13)

- Copy directory structure to the output directory.
- Add documentation in [README.md](README.md).

### Bugfix

- Catch all exceptions when trying to read a file.
- Correctly convert links of the forms `[[#heading-id|Caption]]`, `[[file|Caption]]` and `[[#Heading]]`. Fix [#1](https://github.com/Release-Candidate/Obs2Org/issues/1).
- Correct documentation in [README.md](README.md).

## Version 1.1.0 (2023-03-11)

### Bugfix

- Convert Markdown links of the form `[[Note]]` to `[[file:Note.org::#note][Note]]`. Fix [#1](https://github.com/Release-Candidate/Obs2Org/issues/1)

## Version 1.0.1 (2021-11-09)

Full release including documentation.

## Version 0.9.0 (2021-11-09)

First release
