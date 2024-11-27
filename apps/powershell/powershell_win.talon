app: windows_power_shell
-
settings():
	user.powershell_always_refresh_title = false

# makes the commands in terminal.talon available
tag(): terminal

# activates the implementation of the commands/functions in terminal.talon
tag(): user.generic_windows_shell

# makes commands for certain applications available
# you can deactivate them if you do not use the application
tag(): user.git
tag(): user.anaconda
# tag(): user.kubectl

tag(): user.file_manager
