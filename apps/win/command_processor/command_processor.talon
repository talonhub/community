app: windows_command_processor
app: windows_terminal
and win.title: /Command Prompt/
-
# comment or remove tags for command sets you don't want
tag(): user.file_manager
tag(): user.generic_terminal
tag(): user.git
tag(): user.kubectl
tag(): terminal
  
action(user.file_manager_refresh_title):
	insert("title Command Prompt: %CD%")
	key(enter)

#action(user.file_manager_go_back):
#    key("alt-left")

#action(user.file_manager_go_forward):
#    key("alt-right")

action(user.file_manager_open_parent):
    insert("cd ..")
    key(enter)
    user.file_manager_refresh_title()

action(edit.delete_line): key(esc)