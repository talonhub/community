app: windows_power_shell
app: windows_terminal
and win.title: /PowerShell/
-
tag(): user.file_manager
tag(): user.git
tag(): user.kubectl
tag(): terminal

action(user.file_manager_refresh_title):
  insert('$Host.UI.RawUI.WindowTitle = "Windows PowerShell: " +  $(get-location)')
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