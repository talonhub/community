os: windows
app: windows_explorer
#many commands should work in most save/open dialog. 
#note the "show options" stuff won't work unless work 
#unless the path is displayed in the title, which is rare for those
app: /.*/
and title: /(Save|Open|Browse|Select)/
-
tag(): user.file_manager
action(user.file_manager_go_back):
    key("alt-left")
action(user.file_manager_go_forward):
    key("alt-right")
action(user.file_manager_open_parent):
    key("alt-up")
    
^go <user.letter>$: user.file_manager_open_volume("{letter}:")
go app data: user.file_manager_open_directory("%AppData%")
go program files: user.file_manager_open_directory("%programfiles%")
