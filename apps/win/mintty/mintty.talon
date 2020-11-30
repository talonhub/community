app: mintty
-
tag(): terminal
tag(): user.kubectl
tag(): user.file_manager
tag(): user.git

action(user.file_manager_open_parent):
    insert("cd ..")
    key(enter)

action(edit.paste): key(shift-insert)
action(edit.copy): key(ctrl-insert)

action(edit.delete_line): key(ctrl-u)

run last: key(up enter)

kill all:
    key(ctrl-c)
    insert("y")
    key(enter)
