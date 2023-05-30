# Contributing

## Automatic formatting/linters

This repository uses [`pre-commit`](https://pre-commit.com/) to run and manage its formatters/linters. Running these yourself is optional. If you wish to do so, first [install](https://pre-commit.com/#install) `pre-commit`:

```bash
$ pip install pre-commit
```

You then have a few options as to when to run it:

- Run yourself at any time on your locally changed files: `pre-commit run`
- Run yourself on all files in the repository: `pre-commit run --all-files`
- Run automatically on your PRs (fixes will be pushed automatically to your branch):
  - Visit https://pre-commit.ci/ and authorize the app to connect to your knausj fork.
- Set up an editor hook to run on save:
  - You could follow the instructions for [Black](https://black.readthedocs.io/en/stable/integrations/editors.html), which are well written; simply replace `black <path>` with `pre-commit run --files <file>`.
  - It's more performant to only reformat the specific file you're editing, rather than all changed files.
- Install a git pre-commit hook with `pre-commit install` (optional)
  - This essentially runs `pre-commit run` automatically before creating local commits, applying formatters/linters on all changed files. If it "fails", the commit will be blocked.
  - Note that because many of the rules automatically apply fixes, typically you just need to stage the changes that they made, then reattempt your commit.
  - Whether to use the hook comes down to personal taste. If you like to make many small incremental "work" commits developing a feature, it may be too much overhead.

If you run into setup difficulty with `pre-commit`, you might want to ensure that you have a modern Python 3 local environment first. [pyenv](https://github.com/pyenv/pyenv) is good way to install such Python versions without affecting your system Python (recommend installing 3.9 to match Talon's current version). On macOS you can also `brew install pre-commit`.

## Automated tests

There are a number of automated unit tests in the repository. These are all run _outside_ of the Talon environment (e.g. we don't have access to Talon's window management APIs). These make use of a set of stubbed out Talon APIs in `test/stubs/` and a bit of class loader trickery in `conftest.py`.

To run the test suite you just need to install the `pytest` python package in to a non-Talon Python runtime you want to use for tests (i.e. don't install in the `~/.talon/.venv directory`). You can then just run the `pytest` command from the repository root to execute all the tests.

## Coding principles

This section documents some agreed upon approaches toward reviewing and including code so we can all more easily make consistent decisions.

Each of the principles is numbered for easy referencing. The body is formatted as a short single-line summary of the principle followed by elaboration and discussion links.

### Voice command principles

- P01 - Prefer [object][verb] rather than [verb][object] for new commands. For example 'file save' is better than 'save file'. It may not sound as natural, but it helps for grouping related commands in lists and avoiding conflicting names.
- P02 - Use `browser.host` matcher for web apps. Though this matcher requires a [browser extension](https://github.com/knausj85/knausj_talon/blob/main/apps/README.md) on some operating systems it is the only unambiguous way of referring to a web app.

### Coding principles

- P03 - Use the `app.bundle` matcher for apps on OSX. This is the least ambiguous way of referring to a particular program.
- P04 - Use both `app.name` and `app.exe` matchers for apps on Windows. That is the context should OR together one matcher of each type. Apparently the [MUICache](https://www.magnetforensics.com/blog/forensic-analysis-of-muicache-files-in-windows/) can break, perhaps making one of these matchers stop working.
