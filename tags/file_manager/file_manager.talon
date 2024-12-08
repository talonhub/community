tag: user.file_manager
-
tag(): user.address
tag(): user.navigation

title force: user.file_manager_refresh_title()
(go parent | daddy) [<number_small>]: 
    number = number_small or 0
    user.file_manager_open_parent()
    repeat(number - 1)

^follow {user.file_manager_directories}$:
    user.file_manager_open_directory(file_manager_directories)
^take folder {user.file_manager_directories}$:
    user.file_manager_select_directory(file_manager_directories)
^take file {user.file_manager_files}$: user.file_manager_select_file(file_manager_files)
^file {user.file_manager_files}$: user.file_manager_open_file(file_manager_files)

#new folder
folder new <user.text>: user.file_manager_new_folder(text)

#show properties
properties show: user.file_manager_show_properties()

# open terminal at location
terminal here: user.file_manager_terminal_here()
