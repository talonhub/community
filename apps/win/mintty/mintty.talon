app: mintty
-
tag(): terminal
tag(): user.file_manager
tag(): user.generic_terminal
tag(): user.git
tag(): user.kubectl

action(user.file_manager_open_parent):
    insert("cd ..")
    key(enter)

action(edit.paste): key(shift-insert)
action(edit.copy): key(ctrl-insert)

action(edit.delete_line): key(ctrl-u)

