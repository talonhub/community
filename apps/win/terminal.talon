os: windows
app: Windows Command Processor
app: cmd.exe
-
settings():
    # enable if you'd like the picker gui to automatically appear when explorer has focus
    user.file_manager_auto_show_pickers = 0

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

force title: user.file_manager_refresh_title()
show pickers: user.file_manager_show_pickers()
hide pickers: user.file_manager_hide_pickers()
go pictures: user.file_manager_terminal_open_directory("%UserProfile%\Pictures")
go downloads: user.file_manager_terminal_open_directory("%UserProfile%\Downloads")
go profile: user.file_manager_terminal_open_directory("%UserProfile%")
go docks: user.file_manager_terminal_open_directory("%UserProfile%\Documents")
go data: user.file_manager_terminal_open_directory("%AppData%")
go talon: user.file_manager_terminal_open_directory("%AppData%\Talon")
go back: user.file_manager_go_back()
go forward: user.file_manager_go_forward()
go up: user.file_manager_open_parent()

^follow <user.file_manager_directory_index>$: user.file_manager_terminal_open_directory(user.file_manager_directory_index)

#^open <user.file_manager_file_index>$: user.file_manager_open_file(user.file_manager_file_index)

#todo: decide if select commands make sense in terminal
#^(cell | sell | select) folder <user.file_manager_directory_index>$: user.file_manager_select_directory(user.file_manager_directory_index)
#^(cell | sell | select) file <user.file_manager_file_index>$: user.file_manager_select_file(user.file_manager_file_index)

next folders: user.file_manager_next_folder_page()
previous folders: user.file_manager_previous_folder_page()

next files: user.file_manager_next_file_page()
previous files: user.file_manager_previous_file_page()