app: windows_terminal
-
# makes the commands in generic_terminal available
tag(): terminal 

# activates the implementation of the commands/functions in generic_terminal
tag(): user.generic_windows_shell

# makes commands for certain applications available
# you can deactivate them if you do not use the application
tag(): user.git
tag(): user.anaconda
# tag(): user.kubectl
    
tag(): user.tabs
# TODO: file_manager
# TODO: decide wether to use user.splits

settings open : key(ctrl-,)
focus left: key(ctrl-alt-shift-left)
focus right: key(ctrl-alt-shift-right)
focus up: key(ctrl-alt-shift-up)
focus down: key(ctrl-alt-shift-down)
split right: key(ctrl-shift-h)
split down: key(ctrl-h)
term menu: key(ctrl-shift-f1) # doesn't seem to work-> TODO: fix or remove