os: windows
app: Windows Explorer
app: explorer.exe
-
settings():
    # enable if you'd like the picker gui to automatically appear when explorer has focus
    user.file_manager_auto_show_pickers = 0

show pickers: user.file_manager_show_pickers()
hide pickers: user.file_manager_hide_pickers()
go pictures: user.file_manager_open_directory("%UserProfile%\Pictures")
go downloads: user.file_manager_open_directory("%UserProfile%\Downloads")
go profile: user.file_manager_open_directory("%UserProfile%")
go docks: user.file_manager_open_directory("%UserProfile%\Documents")
go data: user.file_manager_open_directory("%AppData%")
go talon: user.file_manager_open_directory("%AppData%\Talon")
go back: user.file_manager_go_back()
go forward: user.file_manager_go_forward()
go up: user.file_manager_open_parent()

^follow <user.file_manager_directory_index>$: user.file_manager_open_directory(user.file_manager_directory_index)
^open <user.file_manager_file_index>$: user.file_manager_open_file(user.file_manager_file_index)

^(cell | sell | select) folder <user.file_manager_directory_index>$: user.file_manager_select_directory(user.file_manager_directory_index)
^(cell | sell | select) file <user.file_manager_file_index>$: user.file_manager_select_file(user.file_manager_file_index)
