# VS Code support

Installing several Talon community-developed VS Code extensions will improve your experience.

The [VS Code Talon extension pack](https://marketplace.visualstudio.com/items?itemName=pokey.talon) enables a couple advanced commands and improves the speed/robustness of Talon issuing VS Code commands.

The [Andreas Talon](https://marketplace.visualstudio.com/items?itemName=AndreasArvidsson.andreas-talon) extension (dependent on the command server in the extension pack) adds additional commands and useful features for editing your Talon configuration in VS Code.

## Cursorless

If you'd like to use Cursorless, [follow the instructions on the Cursorless site](https://www.cursorless.org/docs/user/installation/).

## Terminal

By default, Talon cannot recognize that you have the VS Code integrated terminal focused, so the `terminal` tag is never active in VS Code. Your goal is for the VS Code window title to reflect whether a terminal is focused, then to match the title in your Talon configuration. You can do so in two ways.

Note that the full window title may not be displayed at the top of VS Code windows. To be sure you are seeing the whole title, say _help scope_ and watch Misc > `win.title` in the scope window that appears.

### Option 1: Add focused view to window title

Change the [`window.title`](vscode://settings/window.title) setting to:

```
${activeEditorShort}${separator}${rootName}${separator}${profileName}${separator}focus:[${focusedView}]
```

This causes VS Code to include `focus:[Terminal]` in the window title whenever the terminal is focused (e.g. by saying _panel terminal_). [Community's VS Code support looks for this string in the window title](vscode_terminal.talon#L5) and activates the terminal tag.

If you have existing customizations to your window title you want to keep, ensure that `focus:[${focusedView}]` appears somewhere within your custom `window.title`.

To enable terminal commands, create a file in your Talon user directory that matches the terminal tag in VS Code, and activates any tags for commands you have installed/want to use, for example:

```talon
app: vscode
tag: terminal
-
tag(): user.generic_unix_shell
tag(): user.git
tag(): user.kubectl
tag(): user.readline
```

### Option 2: Open VS Code integrated terminals as editors

This option lets you enable different voice commands based on _what_ is running in the terminal — for example, if you use both PowerShell and WSL in VS Code integrated terminals.

Change the [`terminal.integrated.defaultLocation`](vscode://settings/terminal.integrated.defaultLocation) setting to `editor`. Then, create a terminal with the voice command _terminal new_.

In an otherwise-default VS Code setup, the first part of the window title as displayed in _help scope_ is the currently-running process, e.g. `zsh` or `powershell`; this is also displayed in the tab title. You can customize the terminal tab title/part of the window title with the [`terminal.integrated.tabs.title`](vscode://settings/terminal.integrated.tabs.title) setting.

To enable terminal commands, create one or more files in your Talon user directory that match the first portion of the window title, and activates **both** the `terminal` tag and any tags for commands you have installed/want to use. For example:

```talon
app: vscode
win.title: /^zsh /
-
tag(): terminal
tag(): user.generic_unix_shell
tag(): user.git
tag(): user.readline
```

```talon
app: vscode
win.title: /^powershell /
-
tag(): terminal
tag(): user.generic_windows_shell
tag(): user.git
```
