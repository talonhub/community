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
4. `format help` will display the available formatters with examples.
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
`format help` will display the available formatters with examples of the output.

Try using formatters by saying e.g. `snake hello world`, which will insert hello_world

Mutliple formatters can be used togther, e.g. `dubstring snake hello world`. This will insert "hello_world"

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
2. Implement the required Talon-defined actions (filename, file_ext) to correctly extract the filename and extension from the programs's title. See https://github.com/knausj85/knausj_talon/blob/master/apps/vscode/vscode.py#L18 for an example.

Python, C#, Talon and javascript language support is currently broken up into ~four contexts in an attempt to define a common grammar where possible between languages

• operators.talon - operator commands

• comment.talon - commenting commands

• programming.talon - function, loop commands, etc

• {your-language-here}.talon - for implementation of the actioIans for the above, and any language-specific stuff


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

• Uncomment `tag(): user.mouse_grid_enabled` to enable the mouse grid.


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
snippets.talon
splits.talon
tabs.talon
```

- New programming languages should support the appropriate 'generic' grammars where possible as well
```
operators.talon
programming.talon
comment.talon
block_comment.talon
```

and should support the lists

```
user.code_functions
user.code_libraries
```

where appropriate. See e.g. csharp.py/csharp.talon. At least, until we come up with something better 👍 

## Automated tests

There are a number of automated tests in the repository which are run outside of the Talon environment. To run them make sure you have the `pytest` python package installed. You can then just run the `pytest` command from the repository root to execute all the tests.

# Talon documentation
For official documentation on Talon's API and features, please visit https://talonvoice.com/docs/. 

For community-generated documentation on Talon, please visit https://talon.wiki/
