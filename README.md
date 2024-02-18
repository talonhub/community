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
- Can work with both Talon's built-in Conformer (wav2letter) speech recognition engine (recommended), or Dragon Naturally Speaking (Windows) / Dragon for Mac (although beware that Dragon for Mac is deprecated).
- Includes commands for working with an eye tracker, but not required

### Linux & Mac

It is recommended to install `community` using [`git`](https://git-scm.com/).

1. Install [`git`](https://git-scm.com/)
2. Open a terminal ([Mac](https://support.apple.com/en-gb/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac) / [Ubuntu](https://ubuntu.com/tutorials/command-line-for-beginners#3-opening-a-terminal))
3. Paste the following into the terminal and hit `enter`:

   ```bash
   cd ~/.talon/user
   git clone https://github.com/talonhub/community community
   ```

Note that it is also possible to install `community` by [downloading and extracting a zip file](#alternate-installation-method-zip-file), but this approach is discouraged because it makes it more difficult to keep track of any changes you may make to your copy of the files.

### Windows

It is recommended to install `community` using [`git`](https://git-scm.com/).

1. Install [`git`](https://git-scm.com/)
2. Open a [terminal](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows)
3. Paste the following into the terminal and hit `enter`:

   ```
   cd %AppData%\Talon\user
   git clone https://github.com/talonhub/community community
   ```

Note that it is also possible to install `community` by [downloading and extracting a zip file](#alternate-installation-method-zip-file), but this approach is discouraged because it makes it more difficult to keep track of any changes you may make to your copy of the files.

## Getting started with Talon

1. `help active` will display the available commands for the active application.
   - Available commands can change with the application, or even window title that has focus.
   - You may navigate help using the displayed numbers. e.g., `help one one` or `help eleven` to open the 11th item in the help list.
   - Note that all help-related commands are defined in [`core/help/help.talon`](https://github.com/talonhub/community/blob/main/core/help/help.talon) and [`core/help/help_open.talon`](https://github.com/talonhub/community/blob/main/core/help/help_open.talon)
2. You can also search for commands by saying `help search <phrase>`. For example, `help search tab` displays all tab-related commands, and `help search help` displays all help-related commands.
3. You can also jump immediately into a particular help context display by recalling the name displayed in help window (based on the name of the .talon file) e.g. `help symbols` or `help visual studio`
4. `help alphabet` will display the alphabet
5. `command history` will toggle a display of the recent commands
6. `help format` will display the available formatters with examples.
7. Many useful, basic commands are defined in https://github.com/talonhub/community/blob/main/core/edit/edit.talon
   - `undo that` and `redo that` are the default undo/redo commands.
   - `paste that`, `copy that`, and `cut that` for pasting/copy/cutting, respectively.
8. For community-generated documentation on Talon itself, please visit https://talon.wiki/

It's recommended to learn the alphabet first, then get familiar with the keys, symbols, formatters, mouse, and generic_editor commands.

Once you have the basics of text input down, try copying some code from one window to another.

After that, explore using ordinal repetition for easily repeating a command without pausing (e.g., saying `go up fifth` will go up five lines), window switching (`focus chrome`), and moving around in your text editor of choice.

If you use vim, just start with the numbers and alphabet, otherwise look at generic_editor.talon as well at jetbrains, vscode, and any other integrations.

### Alphabet

The alphabet is defined here
https://github.com/talonhub/community/blob/main/core/keys/keys.py#L3

`help alphabet` will open a window that displays the alphabet. `help close` to hide the window.

Try saying e.g. `air bat cap` to insert abc.

### Keys

Keys are defined in keys.py. The alphabet is used for A-Z. For the rest, search for `modifier_keys` and then keep scrolling through the file, eg. roughly https://github.com/talonhub/community/blob/main/core/keys/keys.py#L111

All key commands are defined in [keys.talon](https://github.com/talonhub/community/blob/main/core/keys/keys.talon). For example, say `shift air` to press `shift-a`, which types a capital `A`.

On Windows, try commands such as

- `control air` to press `control-a` and select all.

- `super-shift-sun` to press `windows-shift-s` to trigger the screenshot application (Windows 10). Then try `escape` to exit the screenshot application.

On Mac, try commands such as

- `command air` to press `command-a` and select all.

- `control shift command 4` to press ` ctrl-shift-cmd-4` to trigger the screenshot application. Then try `escape` to exit the screenshot application. Please note the order of the modifiers doesn't matter.

Any combination of the modifiers, symbols, alphabet, numbers and function keys can be executed via voice to execute shorcuts. Modifier keys can be tapped using `press`, for example `press control` to tap the control key by itself.

### Symbols

Some symbols are defined in keys.py, so you can say e.g. `control colon` to press those keys.
https://github.com/talonhub/community/blob/main/core/keys/keys.py#L140

Some other symbols are defined here: https://github.com/talonhub/community/blob/main/plugin/symbols/symbols.talon

### Formatters

`help format` will display the available formatters with examples of the output.

Try using formatters by saying e.g. `snake hello world`, which will insert hello_world

Multiple formatters can be used together, e.g. `dubstring snake hello world`. This will insert "hello_world"

Formatters (snake, dubstring) are defined here
https://github.com/talonhub/community/blob/main/core/text/formatters.py#L137

All formatter-related commands are defined here
https://github.com/talonhub/community/blob/main/core/text/text.talon#L8

### Mouse commands

See https://github.com/talonhub/community/blob/main/plugin/mouse/mouse.talon for commands to click, drag, scroll, and use an eye tracker. To use a grid to click at a certain location on the screen, see [mouse_grid](https://github.com/talonhub/community/tree/main/core/mouse_grid).

### Generic editing commands

https://github.com/talonhub/community/blob/main/core/edit/edit.talon

These generic commands are global. Commands such as `go word left` will work in any text box.

### Repeating commands

For repeating commands, useful voice commands are defined here: https://github.com/talonhub/community/blob/main/plugin/repeater/repeater.talon

Try saying e.g. `go up fifth` will go up five lines.
Try saying e.g. `select up third` to hit `shift-up` three times to select some lines in a text field.

### Window management

Global window managment commands are defined here:
https://github.com/talonhub/community/blob/main/core/windows_and_tabs/window_management.talon

- `running list` will toggle a GUI list of words you can say to switch to running applications.
- `focus chrome` will focus the chrome application.
- `launch music` will launch the music application. Note this is currently only implemented on Mac OS X.

### Screenshot commands

https://github.com/talonhub/community/blob/main/plugin/screenshot/screenshot.talon

### Programming Languages

Specific programming languages may be activated by voice commands, or via title tracking.

Activating languages via commands will enable the commands globally, e.g. they'll work in any application. This will also disable the title tracking method (code.language in .talon files) until the "clear language modes" voice command is used.

The commands for enabling languages are defined here: https://github.com/talonhub/community/blob/main/core/modes/language_modes.talon

By default, title tracking activates coding languages in supported applications such as VSCode, Visual Studio (requires plugin), and Notepad++.

To enable title tracking for your application:

1. The active filename (including extension) must be included in the editor's title
2. Implement the required Talon-defined `filename` action to correctly extract the filename from the programs's title. See https://github.com/talonhub/community/blob/main/apps/vscode/vscode.py#L122-L138 for an example.

Python, C#, Talon and javascript language support is currently broken up into several tags in an attempt to define a common grammar where possible between languages. Each tag is defined by a .talon file, which defines the voice commands, and a Python file which declares the actions that should be implemented by each concrete language implementation to support those voice commands. Currently, the tags which are available are:

- `lang/tags/comment_block.{talon,py}` - block comments (e.g., C++'s `/* */`)
- `lang/tags/comment_documentation.{talon,py}` - documentation comments (e.g., Java's `/** */`)
- `lang/tags/comment_line.{talon,py}` - line comments (e.g., Python's `#`)
- `lang/tags/data_null.{talon,py}` - null & null checks (e.g., Python's `None`)
- `lang/tags/data_bool.{talon,py}` - booleans (e.g., Haskell's `True`)
- `lang/tags/functions.{talon,py}` - functions and definitions
- `lang/tags/functions_common.{talon,py}` - common functions (also includes a GUI for picking functions)
- `lang/tags/imperative.{talon,py}` - statements (e.g., `if`, `while`, `switch`)
- `lang/tags/libraries.{talon,py}` - libraries and imports
- `lang/tags/libraries_gui.{talon,py}` - graphical helper for common libraries
- `lang/tags/object_oriented.{talon,py}` - objects and classes (e.g., `this`)
- `lang/tags/operators_array.{talon,py}` - array operators (e.g., Ruby's `x[0]`)
- `lang/tags/operators_assignment.{talon,py}` - assignment operators (e.g., C++'s `x += 5`)
- `lang/tags/operators_bitwise.{talon,py}` - bitwise operators (e.g., C's `x >> 1`)
- `lang/tags/operators_lambda.{talon,py}` - anonymous functions (e.g., JavaScript's `x => x + 1`)
- `lang/tags/operators_math.{talon,py}` - numeric, comparison, and logical operators
- `lang/tags/operators_pointer.{talon,py}` - pointer operators (e.g., C's `&x`)

The support for the language-specific implementations of actions are then located in:

- `lang/{your-language}/{your-language}.py`

To start support for a new language, ensure the appropriate extension is added to the [`language_extensions` in language_modes.py](https://github.com/talonhub/community/blob/main/core/modes/language_modes.py#L9).
Then create the following files:

- `lang/{your-language}/{your-language}.py`
- `lang/{your-language}/{your-language}.talon`

Activate the appropriate tags in `{your-language}.talon` and implement the corresponding actions in `{your-language}.py`, following existing language implementations.
If you wish to add additional voice commands for your language, put those in `{your-language}.talon`.
You may also want to add a force command to `language_modes.talon`.

## File Manager commands

For the following file manager commands to work, your file manager must display the full folder path in the title bar. https://github.com/talonhub/community/blob/main/tags/file_manager/file_manager.talon

For Mac OS X's Finder, run this command in terminal to display the full path in the title.

```
defaults write com.apple.finder _FXShowPosixPathInTitle -bool YES
```

For Windows Explorer, follow these directions
https://www.howtogeek.com/121218/beginner-how-to-make-explorer-always-show-the-full-path-in-windows-8/

For the Windows command line, the `refresh title` command will force the title to the current directory, and all directory commands (`follow 1`) will automatically update the title.

Notes:

• Both Windows Explorer and Finder hide certain files and folder by default, so it's often best to use the imgui to list the options before issuing commands.

• If there no hidden files or folders, and the items are displayed in alphabetical order, you can typically issue the `follow <number>`, `file <number>` and `open <number>` commands based on the displayed order.

To implement support for a new program, you need to implement the relevant file manager actions for your application and assert the user.file_manager tag.

- There are a number of example implementations in the repository. Finder is a good example to copy and customize to your application as needed.
  https://github.com/talonhub/community/blob/main/apps/finder/finder.py

## Terminal commands

Many terminal programs are supported out of the box, but you may not want all the commands enabled.

To disable various commandsets in your terminal, find the relevant talon file and enable/disable the tags for command sets as appropriate.

```
tag(): user.file_manager
tag(): user.git
tag(): user.kubectl
tag(): user.tabs
```

For instance, kubectl commands (kubernetes) aren't relevant to everyone.

Note also that while some of the command sets associated with these tags are defined in talon files within [tags](https://github.com/talonhub/community/tree/main/tags), others, like git, are defined within [apps](https://github.com/talonhub/community/tree/main/apps). Additionally, the commands for tabs are defined in [tabs.talon](https://github.com/talonhub/community/blob/main/core/windows_and_tabs/tabs.talon).

### Unix utilities

If you have a Unix (e.g. OSX) or Linux computer, you can enable support for a number of
common terminal utilities like `cat`, `tail`, or `grep` by uncommenting the following
line in [unix_shell.py](tags/terminal/unix_shell.py):

```
# ctx.tags = ["user.unix_utilities"]
```

Once you have uncommented the line, you can customize your utility commands by editing
`settings/unix_utilities.csv`. Note: this directory is created when first running Talon
with community enabled.

## Jetbrains commands

For Jetbrains commands to work you must install https://plugins.jetbrains.com/plugin/10504-voice-code-idea
into each editor.

## Additional commands

There are other commands not described fully within this file. As an overview:

- The apps folder has command sets for use within different applications
- The core folder has various commands described [here](https://github.com/talonhub/community/blob/main/core/README.md)
- The lang folder has commands for writing [programming languages](https://github.com/talonhub/community?tab=readme-ov-file#programming-languages)
- The plugin folder has various commands described [here](https://github.com/talonhub/community/blob/main/plugin/README.md)
- The tags folder has various other commands, such as using a browser, navigating a filesystem in terminal, and managing multiple cursors

## Settings

Several options are configurable via a [single settings file](settings.talon) out of the box. Any setting can be made context specific as needed (e.g., per-OS, per-app, etc).

The most commonly adjusted settings are probably

• `imgui.scale` to improve the visibility of all imgui-based windows (help, history, etc). This is simply a scale factor, 1.3 = 130%.

• `user.help_max_command_lines_per_page` and `user.help_max_contexts_per_page` to ensure all help information is visible.

• `user.mouse_wheel_down_amount` and `user.mouse_continuous_scroll_amount` for adjusting the scroll amounts for the various scroll commands.

Also, you can add additional vocabulary words, words to replace, search engines and more. Complete the community setup instructions above, then open the `settings` folder to see the provided CSV files and customize them as needed.

## Other talon user file sets

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

For community-generated documentation on Talon, please visit https://talon.wiki/

## Alternate installation method: Zip file

It is possible to install `community` by downloading and extracting a zip file instead of using `git`. Note that this approach is discouraged, because it makes it more difficult to keep track of any changes you may make to your copy of the files.

If you wish to install `community` by downloading and extracting a zip file, proceed as follows:

1. Download the [zip archive of community](https://github.com/talonhub/community/archive/refs/heads/main.zip)
1. Extract the files. If you don’t know how to extract zip files, a quick google search for "extract zip files" may be helpful.
1. Place these extracted files inside the `user` folder of the Talon Home directory. You can find this folder by right clicking the Talon icon in taskbar, clicking Scripting > Open ~/talon, and navigating to `user`.
