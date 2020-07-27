tag: file_manager
-
settings():
    # enable if you'd like the picker gui to automatically appear when explorer has focus
    user.file_manager_auto_show_pickers = 0

force title: user.file_manager_refresh_title()
show options: user.file_manager_show_pickers()
hide options: user.file_manager_hide_pickers()
go pictures: user.file_manager_open_user_directory("Pictures")
go downloads: user.file_manager_open_user_directory("Downloads")
go profile: user.file_manager_open_user_directory("")
go docks: user.file_manager_open_user_directory("Documents")
go back: user.file_manager_go_back()
go forward: user.file_manager_go_forward()
daddy: user.file_manager_open_parent()

^follow <number>$: user.file_manager_open_directory(number - 1)
^open <number>$: user.file_manager_open_file(number - 1)
^(cell | sell | select) folder <number>$: user.file_manager_select_directory(number - 1)
^(cell | sell | select) file <number>$: user.file_manager_select_file(number - 1)

#new folder
new folder: user.file_manager_new_folder()

#show properties
show properties: user.file_manager_show_properties()

# open terminal at location
terminal here: user.file_manager_terminal_here()

next folders: user.file_manager_next_folder_page()
previous folders: user.file_manager_previous_folder_page()

next files: user.file_manager_next_file_page()
previous files: user.file_manager_previous_file_page()


