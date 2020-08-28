# Talon documentation
For up-to-date documentation on Talon's API and features, please visit https://talon.wiki/. 

https://talon.wiki/unofficial_talon_docs/ is a great place to learn about Talon files, actions, and voice command definitions.

# knausj_talon

Talon configs for Mac, Windows, and Linux. Very much in progress. This is also intended to work with both Dragon Naturally Speaking and wav2letter.

Notes: 
- commands are subject to change. I do my best to minimize changes, but I am moving to an [object][verb] standard slowly but surely.
- I make extensive use of Talon's eye tracking features, so my grammar may be much smaller than others.

## Linux & Mac setup

Clone repo into `~/.talon/user`

```insert code:
cd ~/.talon/user
git clone git@github.com:knausj85/knausj_talon.git knausj_talon
```
    
Alternatively, access the directory by right clicking the Talon icon in taskbar, clicking Scripting>Open ~/talon, and navigating to user.

The folder structure should look like:

```insert code:
~/.talon/user/knausj_talon
~/.talon/user/knausj_talon/code
~/.talon/user/knausj_talon/lang
```


## Windows setup

Note: Talon for Windows should be placed in the Program Files directory (or another 'secure' directory): `C:\Program Files\talon` Talon has been signed and utilizes uiAccess for several goodies: this will allow Talon to work with applications that are run as admin.

Clone repo into `%AppData%\Talon\user` 

```insert code:
cd %AppData%\Talon\user
git clone git@github.com:knausj85/knausj_talon.git knausj_talon
```
    
Alternatively, access the directory by right clicking the Talon icon in taskbar, clicking Scripting>Open ~/talon, and navigating to user.
    
The folder structure should look like:

```insert code:
%AppData%\Talon\user\knausj_talon
%AppData%\Talon\user\knausj_talon\code
%AppData%\Talon\user\knausj_talon\lang
```

## Getting started with Talon for coding with this depot

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

Try saying e.g. `air bat cap` to insert abc.

### Keys
Keys are defined here
https://github.com/knausj85/knausj_talon/blob/master/code/keys.py#L67

Try saying e.g. `control air` to press control-a

All key-related voice commands are defined here
https://github.com/knausj85/knausj_talon/blob/master/misc/keys.talon

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

For example, saying `go up fifth` will go up five lines.

### Window management
Global window managment commands are defined here:
https://github.com/knausj85/knausj_talon/blob/master/misc/window_management.talon#L1

e.g., `focus chrome` will focus the chrome application.

### Activating Programming Languages

Specific programming languages may be activated by voice commands, or via title tracking.

Activating languages via commands will enable the commands globally, e.g. they'll work in any application. This will also disable the title tracking method (code.language in .talon files) until the "clear language modes" voice command is used.

The commands are defined here: 
https://github.com/knausj85/knausj_talon/blob/69d0207c873e860002b137f985dd7cb001183a47/modes/modes.talon#L29

By default, title tracking activates coding languages in supported applications such as VSCode, Visual Studio (requires plugin),  and Notepad++. 

To enable title tracking for your application: 
1. The active filename (including extension) must be included in the editor's title
2. Implement the required Talon-defined actions (filename, file_ext) to correctly extract the filename and extension from the programs's title. See https://github.com/knausj85/knausj_talon/blob/master/apps/vscode/vscode.py#L18 for an example.

Python, C#, Talon and javascript language support is currently broken up into ~four contexts in an attempt to define a common grammar where possible between languages

• operators.talon - operator commands

• comment.talon - commenting commands

• programming.talon - function, loop commands, etc

• {your-language-here}.talon - for implementation of the actions for the above, and any language-specific stuff


## File Manager commands
For the following file manager commands to work, your file manager must display the full folder path in the title bar. https://github.com/knausj85/knausj_talon/blob/baa323fcd34d8a1124658a425abe8eed59cf2ee5/apps/file_manager.talon


For Mac OS X's Finder, run this command in terminal to display the full path in the title.

```
defaults write com.apple.finder _FXShowPosixPathInTitle -bool YES
```

For Windows Explorer, follow these directions
https://www.howtogeek.com/121218/beginner-how-to-make-explorer-always-show-the-full-path-in-windows-8/

For the Windows command line, the `refresh title` command will force the title to the current directory, and all directory commands (`follow 1`) will automatically update the title.


## Jetbrains commands

For Jetbrains commands to work you must install https://plugins.jetbrains.com/plugin/10504-voice-code-idea
into each editor.

