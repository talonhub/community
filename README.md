# knausj_talon

Talon configs for Mac, Windows, and Linux. Very much in progress. This is also intended to work with both Dragon Naturally Speaking and wav2letter.

Notes:
- commands are subject to change. We do our best to minimize changes, but we are moving to an [object][verb] standard slowly but surely.
- @knausj85 makes extensive use of Talon's eye tracking features, so the grammar for certain programs may be much smaller than you may require.
- The repository was mostly developed with Dragon, so commands are mostly still optimized for that speech engine.

## Linux & Mac setup

Clone repo into `~/.talon/user`

```insert code:
cd ~/.talon/user
git clone https://github.com/knausj85/knausj_talon knausj_talon
```

Alternatively, access the directory by right clicking the Talon icon in taskbar, clicking Scripting>Open ~/talon, and navigating to user.

The folder structure should look something like the below:

```insert code:
~/.talon/user/knausj_talon
~/.talon/user/knausj_talon/apps
~/.talon/user/knausj_talon/code
~/.talon/user/knausj_talon/lang
~/.talon/user/knausj_talon/misc
~/.talon/user/knausj_talon/modes
~/.talon/user/knausj_talon/mouse_grid
~/.talon/user/knausj_talon/talon_draft_window
~/.talon/user/knausj_talon/text
...
```

## Windows setup

Clone repo into `%AppData%\Talon\user`

```insert code:
cd %AppData%\Talon\user
git clone https://github.com/knausj85/knausj_talon knausj_talon
```

Alternatively, access the directory by right clicking the Talon icon in taskbar, clicking Scripting>Open ~/talon, and navigating to user.

The folder structure should look something like the below:

```insert code:
%AppData%\Talon\user\knausj_talon
%AppData%\Talon\user\knausj_talon\apps
%AppData%\Talon\user\knausj_talon\code
%AppData%\Talon\user\knausj_talon\lang
%AppData%\Talon\user\knausj_talon\misc
%AppData%\Talon\user\knausj_talon\modes
%AppData%\Talon\user\knausj_talon\mouse_grid
%AppData%\Talon\user\knausj_talon\talon_draft_window
%AppData%\Talon\user\knausj_talon\text
...
```

## Getting started with Talon

1. `help active` will display the available commands for the active application.
    - Available commands can change with the application, or even window title that has focus.
    - You may navigate help using the displayed numbers. e.g., `help one one` or `help eleven` to open the 11th item in the help list.
    - Without opening help first, you can also search for commands e.g. `help search tab` to display all tab-related commands
    - Without opening help first, you can also jump immediately into a particular help context display by recalling the name displayed in help window (based on the name of the .talon file) e.g. `help symbols` or `help visual studio`
    - All help-related commands are defined in misc/help.talon and misc/help_open.talon
2. `help alphabet` will display the alphabet
3. `command history` will toggle a display of the recent commands
4. `help format` will display the available formatters with examples.
5. Many useful, basic commands are defined in https://github.com/knausj85/knausj_talon/blob/master/misc/standard.talon#L36
    - `undo that` and `redo that` are the default undo/redo commands.
    - `paste that`, `copy that`, and `cut that` for pasting/copy/cutting, respectively.

It's recommended to learn the alphabet first, then get familiar with the keys, symbols, formatters, mouse, and generic_editor commands.

Once you have the basics of text input down, try copying some code from one window to another.

After that, explore using ordinal repetition for easily repeating a command without pausing (e.g., saying `go up fifth` will go up five lines), window switching (`focus chrome`), and moving around in your text editor of choice.

If you use vim, just start with the numbers and alphabet, otherwise look at generic_editor.talon as well at jetbrains, vscode, and any other integrations.

###  Alphabet
The alphabet is defined here
https://github.com/knausj85/knausj_talon/blob/master/code/keys.py#L6

`help alphabet` will open a window that displays the alphabet. `help close` to hide the window.

Try saying e.g. `air bat cap` to insert abc.


### Keys
Keys are defined in keys.py from line 83 - 182. The alphabet is used for A-Z.
https://github.com/knausj85/knausj_talon/blob/84c6f637ba8304352aa15e01b030e8fa36f4f1a2/code/keys.py#L83

All key commands are defined in keys.talon
https://github.com/knausj85/knausj_talon/blob/master/misc/keys.talon


For example, say

`shift air` to press `shift-a`, which types a capital `A`.


On Windows, try commands such as

`control air` to press `control-a` and select all.

`super-shift-sun` to press `windows-shift-s` to trigger the screenshot application (Windows 10). Then try `escape` to exit the screenshot application.


On Mac, try commands such as

`command air` to press `command-a` and select all.

`control shift command 4` to press ` ctrl-shift-cmd-4` to trigger the screenshot application. Then try `escape` to exit the screenshot application. Please note the order of the modifiers doesn't matter.


Any combination of the modifiers, symbols, alphabet, numbers and function keys can be executed via voice to execute shorcuts. Out of the box, only the modifier keys (command, shift, alt, super) cannot be triggered by themselves.

### Symbols
Some symbols are defined in keys.py, so you can say e.g. `control colon` to press those keys.
https://github.com/knausj85/knausj_talon/blob/master/code/keys.py#L93

Some other symbols are defined here:
https://github.com/knausj85/knausj_talon/blob/master/text/symbols.talon

### Formatters
`help format` will display the available formatters with examples of the output.

Try using formatters by saying e.g. `snake hello world`, which will insert hello_world

Multiple formatters can be used together, e.g. `dubstring snake hello world`. This will insert "hello_world"

Formatters (snake, dubstring) are defined here
https://github.com/knausj85/knausj_talon/blob/master/code/formatters.py#L146

All formatter-related commands are defined here
https://github.com/knausj85/knausj_talon/blob/master/misc/formatters.talon#L2


### Mouse commands
See https://github.com/knausj85/knausj_talon/blob/master/misc/mouse.talon

### Generic editor
https://github.com/knausj85/knausj_talon/blob/master/text/generic_editor.talon#L7

These generic commands are global. Commands such as `go word left` will work in any text box.

### Repeating commands
For repeating commands, useful voice commands are defined here:
https://github.com/knausj85/knausj_talon/blob/ced46aee4b59e6ec5e8545bb01434e27792c830e/misc/repeater.talon#L2

Try saying e.g. `go up fifth` will go up five lines.
Try saying e.g. `select up third` to hit `shift-up` three times to select some lines in a text field.

### Window management
Global window managment commands are defined here:
https://github.com/knausj85/knausj_talon/blob/master/misc/window_management.talon#L1

`running list` will toggle a GUI list of words you can say to switch to running applications.
`focus chrome` will focus the chrome application.
`launch music` will launch the music application. Note this is currently only implemented on Mac OS X.

### Screenshot commands

https://github.com/knausj85/knausj_talon/blob/master/misc/screenshot.talon

### Programming Languages

Specific programming languages may be activated by voice commands, or via title tracking.

Activating languages via commands will enable the commands globally, e.g. they'll work in any application. This will also disable the title tracking method (code.language in .talon files) until the "clear language modes" voice command is used.

The commands for enabling languages are defined here:
https://github.com/knausj85/knausj_talon/blob/master/modes/language_modes.talon

By default, title tracking activates coding languages in supported applications such as VSCode, Visual Studio (requires plugin), and Notepad++.

To enable title tracking for your application:
1. The active filename (including extension) must be included in the editor's title
2. Implement the required Talon-defined `filename` action to correctly extract the filename from the programs's title. See https://github.com/knausj85/knausj_talon/blob/8fc3ca75874398806b42d972c28dad91f1399653/apps/vscode/vscode.py#L109 for an example.

Python, C#, Talon and javascript language support is currently broken up into several tags in an attempt to define a common grammar where possible between languages. Each tag is defined by a .talon file, which defines the voice commands, and a Python file which declares the actions that should be implemented by each concrete language implementation to support those voice commands. Currently, the tags which are available are:

• `lang/tags/comment_block.{talon,py}`         - block comments (e.g., C++'s `/* */`)
• `lang/tags/comment_documentation.{talon,py}` - documentation comments (e.g., Java's `/** */`)
• `lang/tags/comment_line.{talon,py}`          - line comments (e.g., Python's `#`)
• `lang/tags/data_null.{talon,py}`             - null & null checks (e.g., Python's `None`)
• `lang/tags/data_bool.{talon,py}`             - booleans (e.g., Haskell's `True`)
• `lang/tags/functions.{talon,py}`             - functions and definitions
• `lang/tags/functions_common.{talon,py}`      - common functions (also includes a GUI for picking functions)
• `lang/tags/imperative.{talon,py}`            - statements (e.g., `if`, `while`, `switch`)
• `lang/tags/libraries.{talon,py}`             - libraries and imports
• `lang/tags/libraries_gui.{talon,py}`         - graphical helper for common libraries
• `lang/tags/object_oriented.{talon,py}`       - objects and classes (e.g., `this`)
• `lang/tags/operators_array.{talon,py}`       - array operators (e.g., Ruby's `x[0]`)
• `lang/tags/operators_assignment.{talon,py}`  - assignment operators (e.g., C++'s `x += 5`)
• `lang/tags/operators_bitwise.{talon,py}`     - bitwise operators (e.g., C's `x >> 1`)
• `lang/tags/operators_lambda.{talon,py}`      - anonymous functions (e.g., JavaScript's `x => x + 1`)
• `lang/tags/operators_math.{talon,py}`        - numeric, comparison, and logical operators
• `lang/tags/operators_pointer.{talon,py}`     - pointer operators (e.g., C's `&x`)

The support for the language-specific implementations of actions are then located in:

• `lang/{your-language}/{your-language}.py`

To start support for a new language, ensure the appropriate extension is added to the [`extension_lang_map` in `code.py`](https://github.com/knausj85/knausj_talon/blob/12229e932d9d3de85fa2f9d9a7c4f31ed6b6445b/code/code.py#L32).
Then create the following files:

• `lang/{your-language}/{your-language}.py`
• `lang/{your-language}/{your-language}.talon`

Activate the appropriate tags in `{your-language}.talon` and implement the corresponding actions in `{your-language}.py`, following existing language implementations.
If you wish to add additional voice commands for your language, put those in `{your-language}.talon`.
You may also want to add a force command to `language_modes.talon`.

## File Manager commands
For the following file manager commands to work, your file manager must display the full folder path in the title bar. https://github.com/knausj85/knausj_talon/blob/baa323fcd34d8a1124658a425abe8eed59cf2ee5/apps/file_manager.talon


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
https://github.com/knausj85/knausj_talon/blob/5eae0b6a8f2269f24265e77feddbcc4bcf437c36/apps/mac/finder/finder.py#L16

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


## Jetbrains commands

For Jetbrains commands to work you must install https://plugins.jetbrains.com/plugin/10504-voice-code-idea
into each editor.

## Settings

Several options are configurable via a single settings file out of the box. Any setting can be made context specific as needed (e.g., per-OS, per-app, etc).

https://github.com/knausj85/knausj_talon/blob/master/settings.talon


```
#adjust the scale of the imgui to my liking
imgui.scale = 1.3
# enable if you'd like the picker gui to automatically appear when explorer has focus
user.file_manager_auto_show_pickers = 0
#set the max number of command lines per page in help
user.help_max_command_lines_per_page = 50
# set the max number of contexts display per page in help
user.help_max_contexts_per_page = 20
# The default amount used when scrolling continuously
user.mouse_continuous_scroll_amount = 80
#stop continuous scroll/gaze scroll with a pop
user.mouse_enable_pop_stops_scroll = 1
#enable pop click with 'control mouse' mode
user.mouse_enable_pop_click = 1
#When enabled, the 'Scroll Mouse' GUI will not be shown.
user.mouse_hide_mouse_gui = 0
#hide cursor when mouse_wake is called to enable zoom mouse
user.mouse_wake_hides_cursor = 0
#the amount to scroll up/down (equivalent to mouse wheel on Windows by default)
user.mouse_wheel_down_amount = 120
```

The most commonly adjusted settings are probably

• `imgui.scale` to improve the visibility of all imgui-based windows (help, history, etc). This is simply a scale factor, 1.3 = 130%.

• `user.help_max_command_lines_per_page` and `user.help_max_contexts_per_page` to ensure all help information is visible.

• `user.mouse_wheel_down_amount` and `user.mouse_continuous_scroll_amount` for adjusting the scroll amounts for the various scroll commands.

Also, you can add additional vocabulary words, words to replace, search engines and more. Complete the knausj_talon setup instructions above, then open the `settings` folder to see the provided CSV files and customize them as needed.

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

Anyone is welcome to submit PRs and report issues.

## Guidelines for contributions

- Any addition to the global grammar will be scrutinized a bit more thoroughly. The more specific a new context, the less scrutiny that is typically applied.

- New grammars should follow the [subject][verb] standard where-ever possible.

- For Mac OS X, the bundle id should be used for defining app contexts, rather than the name.

- For Windows, both the friendly app name and exe name should be used for defining app contexts when they are different. For some people, the MUICache breaks.

- For new web apps, ensure the domain is used to minimize potential mismatches
https://github.com/knausj85/knausj_talon/blob/master/apps/web/window_titles.md

- New applications should support the appropriate 'generic' grammars where possible

```
generic_browser.talon
find_and_replace.talon
line_commands.talon
multiple_cursors.talon
generic_snippets.talon
splits.talon
tabs.talon
generic_terminal.talon
```

- New programming languages should support the appropriate 'generic' grammars where possible, see above.

## Automatic formatting/linters

This repository uses [`pre-commit`](https://pre-commit.com/) to run manage its formatters/linters.

First, [install](https://pre-commit.com/#install) `pre-commit`:

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

There are a number of automated unit tests in the repository. These are all run *outside* of the Talon environment (e.g. we don't have access to Talon's window management APIs). These make use of a set of stubbed out Talon APIs in `tests/stubs/` and a bit of class loader trickery in `conftest.py`.

To run the test suite you just need to install the `pytest` python package in to a non-Talon Python runtime you want to use for tests (i.e. don't install in the `~/.talon/.venv directory`). You can then just run the `pytest` command from the repository root to execute all the tests.

# Talon documentation

For official documentation on Talon's API and features, please visit https://talonvoice.com/docs/.

For community-generated documentation on Talon, please visit https://talon.wiki/
