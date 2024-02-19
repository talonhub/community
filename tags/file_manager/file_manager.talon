tag: user.file_manager
-
title force: user.file_manager_refresh_title()
go <user.directory>: user.file_manager_open_directory(directory)
go back: user.file_manager_go_back()
go forward: user.file_manager_go_forward()
(go parent | daddy) [<number_small>]: 
    number = number_small or 0
    user.file_manager_open_parent()
    repeat(number - 1)

^follow numb <number_small>$:
    directory = user.file_manager_get_directory_by_index(number_small - 1)
    user.file_manager_open_directory(directory)
^follow {user.file_manager_directories}$:
    user.file_manager_open_directory(file_manager_directories)
^take folder {user.file_manager_directories}$:
    user.file_manager_select_directory(file_manager_directories)
^take file {user.file_manager_files}$: user.file_manager_select_file(file_manager_files)

#new folder
folder new <user.text>: user.file_manager_new_folder(text)

#show properties
properties show: user.file_manager_show_properties()

# open terminal at location
terminal here: user.file_manager_terminal_here()

folder next: user.file_manager_next_folder_page()
folder last: user.file_manager_previous_folder_page()

file next: user.file_manager_next_file_page()
file last: user.file_manager_previous_file_page()
