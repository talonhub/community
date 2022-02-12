app: vscode
mode: command
-

next match: key(enter)
previous match: key(shift-enter)

save file: key(ctrl-s)

(find file | hunt file): key(ctrl-p)

comment selection: key(ctrl-/)

quick fix: user.vscode_and_wait("editor.action.quickFix")
go to terminal: user.vscode_and_wait("workbench.action.terminal.toggleTerminal")

(hunt member | go to member): key(ctrl-shift-o)

jump bracket: user.vscode_and_wait("editor.action.jumpToBracket")

go to symbol <user.text>:
    key(ctrl-shift-o)
    sleep(50ms)
    insert(user.formatted_text(text, "NO_SPACES"))

go to symbol <user.format_text>:
    key(ctrl-shift-o)
    sleep(50ms)
    insert(format_text)

add to export:
    text = edit.selected_text()
    edit.file_end()
    user.find("export")
    user.find_previous()
    sleep(50ms)
    key(escape)
    user.vscode_and_wait("editor.action.jumpToBracket")
    user.vscode_and_wait("editor.action.jumpToBracket")
    edit.up()
    edit.line_end()
    insert(",")
    edit.line_insert_down()
    insert(text)
    # user.vscode_and_wait("editor.action.jumpToBracket")


