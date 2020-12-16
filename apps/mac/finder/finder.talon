os: mac
app: finder
-
tag(): user.file_manager

action(user.file_manager_open_parent):
    key(cmd-up)
        
action(user.file_manager_go_forward):
    key("cmd-]")

action(user.file_manager_go_back):
    key("cmd-[")