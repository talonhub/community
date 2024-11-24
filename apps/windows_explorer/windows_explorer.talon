app: windows_explorer
app: windows_file_browser
-
settings():
    user.context_sensitive_dictation = true
    user.paste_to_insert_threshold = 0
    
tag(): user.address_bar
tag(): user.file_manager
tag(): user.navigation

^go <user.letter>$: user.file_manager_open_volume("{letter}:")
go app data: user.file_manager_open_directory("%AppData%")
go program files: user.file_manager_open_directory("%programfiles%")
