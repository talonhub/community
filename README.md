# community

Voice command set for [Talon](https://talonvoice.com/), community-supported.

_(Originally called `knausj_talon`, after [its original creator :superhero:](https://github.com/knausj85))_

Can be used on its own, but shines when combined with:

- [Cursorless](https://www.cursorless.org/) for programming and text editing
- [Rango](https://github.com/david-tejada/rango) for browser navigation
- [gaze-ocr](https://github.com/wolfmanstout/talon-gaze-ocr) for advanced cursor control using eye tracking and text recognition (OCR)
- [AXKit](https://github.com/phillco/talon-axkit) (macOS only) to enhance Talon with native OS accessibility integrations
- [Other user file sets](https://talon.wiki/talon_user_file_sets/)

## Installation

### Prerequisites

- [Talon](https://talonvoice.com/)
- Mac, Windows, or Linux
- Talon's built-in Conformer (wav2letter) speech recognition engine (recommended), or Dragon NaturallySpeaking (Windows) / Dragon for Mac (although beware that Dragon for Mac is discontinued and its use deprecated).

Includes commands for working with an eye tracker; an [eye tracker](https://talon.wiki/Quickstart/Hardware/#eye-trackers) is not required.

### Linux & Mac

It is recommended to install `community` using [`git`](https://git-scm.com/).

1. Install [`git`](https://git-scm.com/)
2. Open a terminal ([Mac](https://support.apple.com/en-gb/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac) / [Ubuntu](https://ubuntu.com/tutorials/command-line-for-beginners#3-opening-a-terminal))
3. Paste the following into the terminal window then press Enter/Return:

   ```bash
   cd ~/.talon/user
   git clone https://github.com/talonhub/community community
   ```

Note that it is also possible to install `community` by [downloading and extracting a zip file](#alternate-installation-method-zip-file), but this approach is discouraged because it makes it more difficult to keep track of any changes you may make to your copy of the files.

### Windows

It is recommended to install `community` using [`git`](https://git-scm.com/).

1. Install [`git`](https://git-scm.com/)
2. Open a [command prompt](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows)
3. Paste the following into the command prompt window then press Enter:

   ```
   cd %AppData%\Talon\user
   git clone https://github.com/talonhub/community community
   ```

Note that it is also possible to install `community` by [downloading and extracting a zip file](#alternate-installation-method-zip-file), but this approach is discouraged because it makes it more difficult to keep track of any changes you may make to your copy of the files.

## Getting started with Talon

1. `help active` displays commands available in the active (frontmost) application.
   - Available commands can change by application, or even the window title.
   - Navigate help by voice using the displayed numbers (e.g., `help one one` or `help eleven` to open the item numbered 11), or by speaking button titles that don't start with numbers (e.g., `help next` to see the next page of contexts).
   - Help-related commands are defined in [help.talon](core/help/help.talon) and [help_open.talon](core/help/help_open.talon).
2. Search for commands by saying `help search <phrase>`. For example, `help search tab` displays all tab-related commands, and `help search help` displays all help-related commands.
3. Jump immediately to help for a particular help context with the name displayed the in help window (based on the name of the .talon file), e.g. `help context symbols` or `help context visual studio`
4. `help alphabet` displays words for letters of the alphabet; `help symbols` displays words for symbols.
5. `command history` toggles display of recent voice commands.
6. `help format` displays available [formatters](#formatters) with examples.
7. Many useful, basic commands are defined in [edit.talon](core/edit/edit.talon).
   - `undo that` and `redo that` are the default undo/redo commands.
   - `paste that`, `copy that`, and `cut that` for pasting/copy/cutting, respectively.
8. For community-generated documentation on Talon itself, please visit https://talon.wiki/.

It's recommended to learn the alphabet first, then get familiar with the keys, symbols, formatters, mouse, and generic_editor commands.

Once you have the basics of text input down, try copying some code from one window to another.

After that, explore using ordinal repetition for easily repeating a command without pausing (e.g., saying `go up fifth` will go up five lines), window switching (`focus chrome`), and moving around in your text editor of choice.

If you use vim, just start with the numbers and alphabet, otherwise look at generic_editor.talon as well at jetbrains, vscode, and any other integrations.

### Alphabet

The alphabet is defined in
[this Talon list file](core/keys/letter.talon-list).

Say `help alphabet` to open a window displaying the alphabet. `help close` closes the window.

Try saying e.g. `air bat cap` to insert abc.

### Keys

All key commands are defined in [keys.talon](core/keys/keys.talon). Say letters of the [Talon alphabet](#alphabet) for A–Z.

For modifier keys, say `help modifiers`. For example, say `shift air` to press `shift-a`, which types a capital `A`.

For symbols, say `help symbols`. These are defined in keys.py;
search for `modifier_keys` and then keep scrolling — roughly starting [here](core/keys/keys.py#L124).

On Windows, try commands such as:

- `control air` to press Control+A and select all.

- `super-shift-sun` to press Win+Shift+S, triggering the screenshot application (Windows 10). Then try `escape` to exit.

On Mac, try commands such as:

- `command air` to press ⌘A and select all.

- `control shift command 4` to press ⌃⇧⌘4, copying a screenshot of the selected area to the clipboard. Then try `escape` to exit. Please note the order of the modifiers doesn't matter.

Say any combination of modifiers, symbols, alphabet, numbers and function keys to execute keyboard shortcuts. Modifier keys can be tapped using `press`, for example `press control` taps the Control (⌃) key by itself.

### Symbols

Some symbols are defined in [keys.py](core/keys/keys.py#L144), so you can say, e.g. `control colon` to press those keys.

Multi-character punctuation (e.g., ellipses) is defined in [symbols.talon](plugin/symbols/symbols.talon).

### Formatters

Formatters allow you to insert words with consistent capitalization and punctuation. `help format` displays available formatters with examples of their output when followed by `one two three`.

Try using a formatter by saying `snake hello world`. This inserts "hello_world".

Multiple formatters can be chained together — for example, `dubstring snake hello world` inserts "hello_world".

Prose formatters (marked with \* in the help window) preserve hyphens and apostrophes. Non-prose (code) formatters strip punctuation instead, for example to generate a valid variable name. `title how's it going` inserts "How's It Going"; `hammer how's it going` inserts "HowsItGoing".

Reformat existing text with one or more formatters by selecting it, then saying the formatter name(s) followed by `that`. Say `help reformat` to display how each formatter reformats `one_two_three`.

Formatter names (snake, dubstring) are defined [here](core/formatters/formatters.py#L245). Formatter-related commands are defined in [text.talon](core/text/text.talon#L8).

### Mouse commands

See [mouse.talon](plugin/mouse/mouse.talon) for commands to click, drag, scroll, and use an eye tracker. To use a grid to click at a certain location on the screen, see [mouse_grid](core/mouse_grid).

### Generic editing commands

Editing commands in [edit.talon](core/edit/edit.talon) are global. Commands such as `go word left` will work in any text box that uses standard platform text navigation conventions.

### Repeating commands

Voice commands for repeating commands are defined in [repeater.talon](plugin/repeater/repeater.talon).

Say `go up fifth` or `go up five times` to go up five lines. `select up third` will press Shift+Up three times to select several lines of text.

### Window management

Global window management commands are defined in [window_management.talon](core/windows_and_tabs/window_management.talon).

- `running list` toggles a window displaying words you can say to switch to running applications. To customize the spoken forms for an app (or hide an app entirely from the list), edit the `app_name_overrides_<platform>.csv` files in the [core/app_switcher](core/app_switcher) directory.
- `focus chrome` will focus the Chrome application.
- `launch music` will launch the music application. Note this is currently only implemented on macOS.

### Screenshot commands

See [screenshot.talon](plugin/screenshot/screenshot.talon).

### Programming languages

Specific programming languages may be activated by voice commands, or via title tracking.

Activating languages via commands will enable the commands globally, e.g. they'll work in any application. This will also disable the title tracking method (code.language in .talon files) until the "clear language modes" voice command is used.

Commands for enabling languages are defined in [language_modes.talon](core/modes/language_modes.talon).

By default, title tracking activates languages in supported applications such as VSCode, Visual Studio (requires plugin), and Notepad++.

To enable title tracking for your application:

1. Ensure the active filename (including extension) is included in the window title.
2. Implement the required Talon-defined `filename` action to correctly extract the filename from the window title. See the [Visual Studio Code implementation](apps/vscode/vscode.py#L137-L153) for an example.

Python, C#, Talon and JavaScript language support is broken up into multiple tags in an attempt to standardize common voice commands for features available across languages. Each tag is defined in a .talon file named after a `user.code_` tag (e.g., `user.code_functions` → `functions.talon`) containing voice commands and a Python file declaring the actions that should be implemented by each concrete language implementation to support the voice commands. These files include:

- `lang/tags/comment_block.{talon,py}` - block comments (e.g., C++'s `/* */`)
- `lang/tags/comment_documentation.{talon,py}` - documentation comments (e.g., Java's `/** */`)
- `lang/tags/comment_line.{talon,py}` - line comments (e.g., Python's `#`)
- `lang/tags/data_null.{talon,py}` - null & null checks (e.g., Python's `None`)
- `lang/tags/data_bool.{talon,py}` - booleans (e.g., Haskell's `True`)
- `lang/tags/functions.{talon,py}` - functions and definitions
- `lang/tags/functions_common.{talon,py}` - common functions (also includes a GUI for picking functions)
- `lang/tags/imperative.{talon,py}` - statements (e.g., `if`, `while`, `switch`)
- `lang/tags/libraries.{talon,py}` - libraries and imports
- `lang/tags/object_oriented.{talon,py}` - objects and classes (e.g., `this`)
- `lang/tags/operators_array.{talon,py}` - array operators (e.g., Ruby's `x[0]`)
- `lang/tags/operators_assignment.{talon,py}` - assignment operators (e.g., C++'s `x += 5`)
- `lang/tags/operators_bitwise.{talon,py}` - bitwise operators (e.g., C's `x >> 1`)
- `lang/tags/operators_lambda.{talon,py}` - anonymous functions (e.g., JavaScript's `x => x + 1`)
- `lang/tags/operators_math.{talon,py}` - numeric, comparison, and logical operators
- `lang/tags/operators_pointer.{talon,py}` - pointer operators (e.g., C's `&x`)

Language-specific implementations of the above features are in files named `lang/{your-language}/{your-language}.py`.

To add support for a new language, ensure appropriate extension is added/uncommented in the [`language_extensions` dictionary in language_modes.py](core/modes/language_modes.py#L9). Then create the following files:

- `lang/{your-language}/{your-language}.py`
- `lang/{your-language}/{your-language}.talon`

Activate the appropriate tags in `{your-language}.talon` and implement the corresponding actions in `{your-language}.py`, following existing language implementations. Put additional voice commands for your language (not shared with other languages) in `{your-language}.talon`.

## File manager commands

For the following file manager commands to work, your file manager must display the full folder path in the title bar. tags/file_manager/file_manager.talon

For the Mac Finder, run this command in Terminal to display the full path in the window title:

```
defaults write com.apple.finder _FXShowPosixPathInTitle -bool YES
```

For Windows Explorer, [follow these directions](https://www.howtogeek.com/121218/beginner-how-to-make-explorer-always-show-the-full-path-in-windows-8/).

For the Windows command line, the `refresh title` command will force the title to the current directory, and all directory commands (`follow 1`) will automatically update the title.

Notes:

- Both Windows Explorer and Finder hide certain files and folders by default, so it's often best to use the imgui to list the options before issuing commands.

- If there no hidden files or folders, and the items are displayed in alphabetical order, you can typically issue the `follow <number>`, `file <number>` and `open <number>` commands based on the displayed order.

To implement support for a new program, implement the relevant file manager actions for your application and assert the `user.file_manager` tag. There are a number of example implementations in the repository. [Finder](apps/finder/finder.py) is a good example to copy and mdoify.

## Terminal commands

Many terminal applications are supported out of the box, but you may not want all the commands enabled.

To use command sets in your terminal applications, enable/disable the corresponding tags in the terminal application-specific .talon file.

```
tag(): user.file_manager
tag(): user.git
tag(): user.kubectl
tag(): user.tabs
```

For instance, kubectl commands (kubernetes) aren't relevant to everyone.

Note also that while some of the command sets associated with these tags are defined in talon files within [tags](tags), others, like git, are defined within [apps](apps). Commands for tabs are defined in [tabs.talon](core/windows_and_tabs/tabs.talon).

### Unix utilities

If you have a Unix (e.g. macOS) or Linux computer, you can enable support for a number of
common terminal utilities like `cat`, `tail`, or `grep` by uncommenting the following
line in [unix_shell.py](tags/terminal/unix_shell.py):

```
# ctx.tags = ["user.unix_utilities"]
```

Once you have uncommented the line, you can customize your utility commands by editing
`tags/terminal/unix_utility.talon-list`.

## Jetbrains commands

For Jetbrains commands to work you must install https://plugins.jetbrains.com/plugin/10504-voice-code-idea
into each editor.

## Additional commands

There are other commands not described fully within this file. As an overview:

- The apps folder has command sets for use within different applications
- The core folder has various commands described [here](core/README.md)
- The lang folder has commands for writing [programming languages](#programming-languages)
- The plugin folder has various commands described [here](plugin/README.md)
- The tags folder has various other commands, such as using a browser, navigating a filesystem in terminal, and managing multiple cursors

## Settings

Several options are configurable via a [single settings file](settings.talon) out of the box. Any setting can be made context specific as needed (e.g., per-OS, per-app, etc).

The most commonly adjusted settings are probably

- `imgui.scale` to improve the visibility of all imgui-based windows (help, history, etc). This is simply a scale factor, 1.3 = 130%.

- `user.help_max_command_lines_per_page` and `user.help_max_contexts_per_page` to ensure all help information is visible.

- `user.mouse_wheel_down_amount` and `user.mouse_continuous_scroll_amount` for adjusting the scroll amounts for the various scroll commands.

## Customizing words and lists

Most lists of words are provided as Talon list files, with an extension of `.talon-list`. Read about the syntax of these files [on the Talon wiki](https://talon.wiki/Customization/talon_lists).

Some lists with multiple spoken forms/alternatives are instead provided as CSV files. Some are in the `settings` folder and are not created until you launch Talon with `community` installed.

You can customize common Talon list and CSV files with voice commands: say the word `customize` followed by `abbreviations`, `additional words`, `alphabet`, `homophones`, `search engines`, `Unix utilities`, `websites`, `words to replace`, `contacts json` or `contacts csv`. These open the file in a text editor and move the insertion point to the bottom of the file so you can add to it.

You can also add words to the vocabulary or replacements (words_to_replace) by using the commands in [edit_vocabulary.talon](core/vocabulary/edit_vocabulary.talon).

## 💡 Tip: Overriding cleanly

You can override Talon lists by creating a new `.talon-list` file of your own, rather than changing the existing list in the repository.
This reduces how much manual `git merge`-ing you'll have to do in the future, when you go to merge new versions of this repository (colloquially called "upstream") with your local changes. This is because _new_ files you create will almost never conflict with upstream changes, whereas changing an existing file (especially hot spots, like commonly-customized lists) frequently do.
Your override files can even live outside of the `community` repository (anywhere in the Talon user directory), if you prefer, further simplifying merging.
To do so, simply create a `.talon-list` file with a more specific [context header](https://talon.wiki/Customization/talon-files#context-header) than the default. (For example, `lang: en` or `os: mac` main). Talon ensures that the most specific header (your override file) wins.

For example, to override `user.modifier_key`, you could create `modifier_keys_MYNAME.talon`:

```talon
list:  user.modifier_key
language: en
-

# My preferred modifier keys
rose: cmd
troll: control
shift: shift
alt: alt
```

## Other Talon user file sets

In addition to this repo, there are [other Talon user file sets](https://talon.wiki/talon_user_file_sets/) containing additional commands that you may want to experiment with if you're feeling adventurous 😊. Many of them are meant to be used alongside `community`, but a few of them are designed as replacements. If it's not clear which, please file an issue against the given GitHub repository for that user file set!

# Collaborators

This repository is now officially a team effort. The following contributors have direct access:

- @dwiel
- @fidgetingbits
- @knausj85
- @rntz
- @splondike
- @pokey

Collaborators will reply to issues and pull requests as time and health permits. Please be patient.

## Guidelines for collaborators

1. Collaborators prioritize their health and their personal/professional needs first. Their time commitment to this effort is limited.
2. For "minor" fixes and improvements/bugs/new apps, collaborators are free to contribute without any review
3. For "significant" new development and refactors, collaborators should seek appropriate input and reviews from each-other. Collaborators are encouraged to open a discussion before committing their time to any major effort.

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for our guidelines for contributors

## Automatic formatting/linters

This repository uses [`pre-commit`](https://pre-commit.com/) to run and manage its formatters/linters. Running these yourself is optional. If you wish to do so, first [install](https://pre-commit.com/#install) `pre-commit`:

```bash
$ pip install pre-commit
```

You then have a few options as to when to run it:

- Run yourself at any time on your locally changed files: `pre-commit run`
- Run yourself on all files in the repository: `pre-commit run --all-files`
- Run automatically on your PRs (fixes will be pushed automatically to your branch):
  - Visit https://pre-commit.ci/ and authorize the app to connect to your `community` fork.
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

## Talon documentation

For official documentation on Talon's API and features, please visit https://talonvoice.com/docs/.

For community-generated documentation on Talon, please visit https://talon.wiki/.

## Alternate installation method: Zip file

It is possible to install `community` by downloading and extracting a zip file instead of using `git`. Note that this approach is discouraged, because it makes it more difficult to keep track of any changes you may make to your copy of the files.

If you wish to install `community` by downloading and extracting a zip file, proceed as follows:

1. Download the [zip archive of community](https://github.com/talonhub/community/archive/refs/heads/main.zip).
1. Extract the files. If you don’t know how to extract zip files, a quick google search for "extract zip files" may be helpful.
1. Place these extracted files inside the `user` folder of the Talon Home directory. You can find this folder by right-clicking the Talon icon in the taskbar (Windows) or clicking the Talon icon in the menu bar (Mac), clicking Scripting > Open ~/talon, and navigating to `user`.
