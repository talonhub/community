# VSCode support

It is recommended to install the [VSCode talon extension pack](https://marketplace.visualstudio.com/items?itemName=pokey.talon), which will enable a couple advanced commands and improve the speed / robustness of VSCode commands.

## Cursorless

If you'd like to use Cursorless, follow the instructions in the [cursorless-talon repo](https://github.com/pokey/cursorless-talon).

## Terminal

By default the VSCode terminal is not going to recognize terminal commands from talon. In order for talon to configure terminal commands in VSCode the window has to include a word that it can use to match. This is possible using the VSCode setting to include word terminal in the title. You can do this with this setting in VSCode:

```
"window.title": "${dirty}${activeEditorShort}${separator}${rootName}${separator}${profileName}${separator}${appName}${separator}focus:[${focusedView}]",
```
