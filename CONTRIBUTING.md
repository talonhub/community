This document attempts to list a set of principles for contributors to the `community` repository to consider. The idea is to document some agreed upon approaches toward reviewing and including code so we can all more easily make consistent decisions.

Each of the principles is numbered for easy referencing. The body is formatted as a short single-line summary of the principle followed by elaboration and discussion links.

# Voice command principles

- P01 - Prefer [object][verb] rather than [verb][object] for new commands. For example 'file save' is better than 'save file'. It may not sound as natural, but it helps for grouping related commands in lists and avoiding conflicting names.
- P02 - Use `browser.host` matcher for web apps. Though this matcher requires a [browser extension](https://github.com/talonhub/community/blob/main/apps/README.md) on some operating systems it is the only unambiguous way of referring to a web app.

# Coding principles

- P03 - Use the `app.bundle` matcher for apps on OSX. This is the least ambiguous way of referring to a particular program.
- P04 - Use both `app.name` and `app.exe` matchers for apps on Windows. That is the context should OR together one matcher of each type. Apparently the [MUICache](https://www.magnetforensics.com/blog/forensic-analysis-of-muicache-files-in-windows/) can break, perhaps making one of these matchers stop working.
