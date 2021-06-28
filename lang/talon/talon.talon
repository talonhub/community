mode: user.talon
mode: command
and code.language: talon
-
tag(): user.code_operators
tag(): user.code_comment

dot talon: insert(".talon")
#defintion blocks for the context
action block:
    insert("action():")
    edit.left()
    edit.left()
setting block:
    insert("settings():\n\t")
    #context requirements
win require:
    insert("os: windows\n")
mac require:
    insert("os: mac\n")
linux require:
    insert("os: linux\n")
title require:
    insert("win.title: ")
app require:
    insert("app: ")
tag require:
    insert("tag: ")
tag set:
    insert("tag(): ")
    #commands for dictating key combos
key <user.keys> over: "{keys}"
key <user.modifiers> over: "{modifiers}"
#funk commands, consistent with other languages
toggle funk: user.code_toggle_functions()
funk <user.code_functions>:
    user.code_insert_function(code_functions, "")
funk cell <number>:
    user.code_select_function(number - 1, "")
funk wrap <user.code_functions>:
    user.code_insert_function(code_functions, edit.selected_text())
funk wrap <number>:
    user.code_select_function(number - 1, edit.selected_text())
