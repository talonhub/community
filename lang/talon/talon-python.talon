app: vscode
win.title: /— user/
win.title: /— knausj_talon/
win.title: / - user - Visual Studio Code/
tag: user.python
-
tag(): user.talon_python 

action {user.talon_actions}:
    user.talon_code_insert_function(talon_actions, edit.selected_text(), 1)
