app: apple_terminal
-
# makes the commands in terminal.talon available
tag(): terminal

# use readline keybindings for various editing commands
tag(): user.readline

# activates the implementation of the commands/functions in terminal.talon
tag(): user.generic_unix_shell

# makes commands for certain applications available
# you can deactivate them if you do not use the application
tag(): user.git
tag(): user.anaconda
tag(): user.kubectl

# TODO: explain
tag(): user.tabs
tag(): user.file_manager

suspend: key(ctrl-z)
resume:
    insert("fg")
    key(enter)
