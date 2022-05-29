os: mac
win.title:/knausj_talon/
app: vscode
-

jump code:
    user.vscode("workbench.action.quickOpen")
    sleep(100ms)
    insert("vscode.talon")
    sleep(100ms)
    key(enter)

jump code pi:
    user.vscode("workbench.action.quickOpen")
    sleep(100ms)
    insert("vscode.py")
    sleep(100ms)
    key(enter)


