app: vscode
# Treat the VSCode terminal as a terminal. This relies on VSCode to include the word terminal in the window title.
# Add this setting to your settings:
#   "window.title": "${dirty}${activeEditorShort}${separator}${rootName}${separator}${profileName}${separator}${appName}${separator}focus:[${focusedView}]",
win.title: /focus:\[Terminal\]/
-
tag(): terminal
