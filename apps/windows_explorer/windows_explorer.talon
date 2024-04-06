app: windows_explorer
app: windows_file_browser
-
tag(): user.file_manager
tag(): user.history

^go <user.letter>$: user.file_manager_open_volume("{letter}:")
go app data: user.file_manager_open_directory("%AppData%")
go program files: user.file_manager_open_directory("%programfiles%")
address bar: key(ctrl-l)
address copy|copy address:
    key(ctrl-l ctrl-c)
