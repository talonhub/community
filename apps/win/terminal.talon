app: windows_terminal
app: windows_command_processor
-
# comment or remove tags for command sets you don't want
tag(): user.file_manager
tag(): user.git
tag(): user.kubectl
tag(): user.tabs
tag(): terminal

run last: key(up enter)

kill all:
  key(ctrl-c)
  insert("y")
  key(enter)
  
action(user.file_manager_refresh_title):
	insert("title %CD%")
	key(enter)

#action(user.file_manager_go_back):
#    key("alt-left")

#action(user.file_manager_go_forward):
#    key("alt-right")

action(user.file_manager_open_parent):
    insert("cd ..")
    key(enter)
    user.file_manager_refresh_title()

