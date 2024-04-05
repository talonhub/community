# VSCode support

It is recommended to install the [VSCode talon extension pack](https://marketplace.visualstudio.com/items?itemName=pokey.talon), which will enable a couple advanced commands and improve the speed / robustness of VSCode commands.

## Cursorless

If you'd like to use Cursorless, follow the instructions in the [cursorless-talon repo](https://github.com/pokey/cursorless-talon).

## Terminal

In order to use terminal commands when the VSCode terminal is focused, you must add the following line to your [VSCode `settings.json`](https://code.visualstudio.com/docs/getstarted/settings#_settingsjson):

```
"window.title": "${dirty}${activeEditorShort}${separator}${rootName}${separator}${profileName}${separator}${appName}${separator}focus:[${focusedView}]",
```
