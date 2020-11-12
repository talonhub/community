tag: user.file_manager
-
title force: user.file_manager_refresh_title()
manager show: user.file_manager_toggle_pickers()
go docks: user.file_manager_open_user_directory("Documents")
go downloads: user.file_manager_open_user_directory("Downloads")
go pictures: user.file_manager_open_user_directory("Pictures")
go profile: user.file_manager_open_user_directory("")
go talon home: user.file_manager_open_directory(path.talon_home())
go talon user: user.file_manager_open_directory(path.talon_user())
go user: user.file_manager_open_directory(path.user_home())
go back: user.file_manager_go_back()
go forward: user.file_manager_go_forward()
daddy: user.file_manager_open_parent()

^follow <number>$: user.file_manager_open_directory(number - 1)
^follow {user.file_manager_directories}$: user.file_manager_open_directory(file_manager_directories)
^open <number>$: user.file_manager_open_file(number - 1)
^folder <number>$: user.file_manager_select_directory(number - 1)
^file <number>$: user.file_manager_select_file(number - 1)
^file {user.file_manager_files}$: user.file_manager_select_file(file_manager_files)

#new folder
folder new: user.file_manager_new_folder()

#show properties
properties show: user.file_manager_show_properties()

# open terminal at location
terminal here: user.file_manager_terminal_here()

folder next: user.file_manager_next_folder_page()
folder last: user.file_manager_previous_folder_page()

file next: user.file_manager_next_file_page()
file last: user.file_manager_previous_file_page()

