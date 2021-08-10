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
tag(): user.splits

settings open : key(ctrl-,)
focus left: key(alt-left)
focus right: key(alt-right)
focus up: key(alt-up)
focus down: key(alt-down)
term menu: key(ctrl-shift-f1) # doesn't seem to work-> TODO: fix or remove