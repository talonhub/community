app: ubuntu
app: windows_terminal
and win.title: /Ubuntu/
-
tag(): user.file_manager
tag(): user.git
tag(): user.kubectl
tag(): terminal

action(user.file_manager_refresh_title): skip()
action(user.file_manager_open_parent):
    insert("cd ..")
    key(enter)

^go <user.letter>$: user.file_manager_open_volume("/mnt/{letter}")
