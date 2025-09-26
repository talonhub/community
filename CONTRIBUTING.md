This document attempts to list a set of principles for contributors to the `community` repository to consider. The idea is to document some agreed upon approaches toward reviewing and including code so we can all more easily make consistent decisions.

Each of the principles is numbered for easy referencing. The body is formatted as a short single-line summary of the principle followed by elaboration and discussion links.

# Voice command principles

- P01 - Prefer [object][verb] rather than [verb][object] for new commands. For example 'file save' is better than 'save file'. It may not sound as natural, but it helps for grouping related commands in lists and avoiding conflicting names.
- P02 - Use `browser.host` matcher for web apps. Though this matcher requires a [browser extension](https://github.com/talonhub/community/blob/main/apps/README.md) on some operating systems it is the only unambiguous way of referring to a web app.

# Coding principles

- P03 - Use the `app.bundle` matcher for apps on OSX. This is the least ambiguous way of referring to a particular program.
- P04 - Use both `app.name` and `app.exe` matchers for apps on Windows. That is the context should OR together one matcher of each type. Apparently the [MUICache](https://www.magnetforensics.com/blog/forensic-analysis-of-muicache-files-in-windows/) can break, perhaps making one of these matchers stop working.
- P05 - Use `.talon-list` files for talon lists unless there is a good reason not to. `.talon-list` files are easier for users to edit — especially users who are not programmers. If a list needs to be constructed or referenced through Python code, it may make sense to instead leave it in Python.
- P06 - Communicate with maintainers before submitting a large pull request. Not everything that is useful for a specific user belongs in community itself. To avoid wasting your time, it is recommended to file an issue to give a chance for maintainers to respond before doing a lot of work on a feature that may or may not get accepted. Maintainers may additionally have useful suggestions on how to implement your desired changes that can save you considerable work and reduce the amount of changes requested in peer review.
- P07 - Try to create pull requests that focus on a single feature at a time. Separating pieces of code that do not depend on each other into separate pull requests makes peer review easier and will usually lead to changes getting merged faster. Large or unfocused pull requests trying to do too much at once often lose momentum and become abandoned in peer review. The reason for this is usually that there are too many pieces that need to be properly reviewed before the entire thing can be merged. Smaller, more focused pull requests allow uncontroversial changes to merged quickly while facilitating more focused discussions for those changes that do merit it. 
