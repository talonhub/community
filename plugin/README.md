# plugin

The plugin folder has several other subfolders containing various commands and features:

- `are_you_sure` lets you require confirmation before executing an action, which can be useful for potentially destructive commands like shutting down your computer or exiting Talon.
- `breaking_changes_notice` notifies the user if the breaking changes file has been updated.
- `cancel` contains commands to make Talon ignore a command
- `command_history` has commands to see previous commands
- `datetimeinsert` has commands to automatically write the current date and time
- `desktops` has commands to navigate between the different computer desktops
- `draft_editor` has some of the commands to open and use a built-in pop-up text editor
- `dropdown` has commands to select an option from a dropdown menu
- `gamepad` has default bindings for using a gamepad device to do tasks like clicking, scrolling and moving your cursor.
- `listening_timeout` has a setting for turning off speech recognition if Talon does not detect any commands for the specified number of minutes.
- `macro` has commands to use macros
- `media` has commands for video and volume control
- `microphone_selection` has commands for selecting a microphone to use
- `mode_indicator` does not have commands, but has settings for enabling a graphical mode indicator
- `mouse` has commands to click, drag, scroll, and use an eye tracker
- `new_user_message` shows a message intended for new users.
- `repeater` has commands for repeating other commands, described briefly in the top level [README](https://github.com/talonhub/community?tab=readme-ov-file#repeating-commands)
- `screenshot` has commands for taking screenshots
- `symbols` has commands for inserting certain symbols, like pairs of parentheses or quotation marks
- `talon_draft_window` has the rest of the commands for using the draft editor window
- `talon_helpers` has commands helpful for debugging, opening the Talon directory, and getting updates
- `text_navigation` has commands for navigating the cursor in text
- `then` has a command that does nothing, which is sometimes useful for command chaining.
