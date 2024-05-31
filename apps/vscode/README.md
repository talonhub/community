# VSCode support

It is recommended to install the [VSCode talon extension pack](https://marketplace.visualstudio.com/items?itemName=pokey.talon), which will enable a couple advanced commands and improve the speed / robustness of VSCode commands.

## Cursorless

If you'd like to use Cursorless, follow the instructions in the [cursorless-talon repo](https://github.com/pokey/cursorless-talon).

## Terminal

In order to use terminal commands when the VSCode terminal is focused, you must add the following line to your [VSCode `settings.json`](https://code.visualstudio.com/docs/getstarted/settings#_settingsjson):

```
"window.title": "${activeEditorShort}${separator}${rootName}${separator}${profileName}${separator}focus:[${focusedView}]",
```

This setting will cause VSCode to include a special string in the window title whenever the terminal is focused. Talon will look for this string in the window title and activate the terminal commands in response.

Note that if you have customizations in your window title that you'd like to keep, the important part is just to ensure that `focus:[${focusedView}]` appears somewhere within your custom window title.

In order to enable additional terminal commands you will need to set some tags when the terminal tag is active. You can do this by creating a file in your talon settings that looks something like this:

```
tag: terminal
-
tag(): user.generic_unix_shell
tag(): user.git
tag(): user.kubectl
tag(): user.readline
```
