tag: user.file_manager
-
tag(): user.address
tag(): user.navigation

title force: user.file_manager_refresh_title()
manager show: user.file_manager_toggle_pickers()
manager close: user.file_manager_hide_pickers()
manager refresh: user.file_manager_update_lists()
(go parent | daddy): user.file_manager_open_parent()
^follow {user.file_manager_directories}$:
    user.file_manager_open_directory(file_manager_directories)
^follow numb <number_small>$:
    directory = user.file_manager_get_directory_by_index(number_small - 1)
    user.file_manager_open_directory(directory)
^[select | cell] folder {user.file_manager_directories}$:
    user.file_manager_select_directory(file_manager_directories)
^[select | cell] folder numb <number_small>$:
    directory = user.file_manager_get_directory_by_index(number_small - 1)
    user.file_manager_select_directory(directory)
^[select | cell] file {user.file_manager_files}$:
    user.file_manager_select_file(file_manager_files)
^[select | cell] file numb <number_small>$:
    file = user.file_manager_get_file_by_index(number_small - 1)
    user.file_manager_select_file(file)
^open {user.file_manager_files}$: user.file_manager_open_file(file_manager_files)
^open numb <number_small>$:
    file = user.file_manager_get_file_by_index(number_small - 1)
    user.file_manager_open_file(file)

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
