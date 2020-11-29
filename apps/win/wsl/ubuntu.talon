app: ubuntu
-
tag(): user.file_manager

action(user.file_manager_refresh_title): skip()
action(user.file_manager_open_parent):
    insert("cd ..")
    key(enter)

action(edit.paste): key(ctrl-shift-v)
action(edit.copy): key(ctrl-shift-c)

^go <user.letter>$: user.file_manager_open_volume("/mnt/{letter}")
