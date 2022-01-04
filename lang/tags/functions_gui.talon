tag: user.code_functions_gui
-
toggle funk: user.code_toggle_functions()
funk <user.code_functions>:
    user.code_insert_function(code_functions, "")
funk cell <number>:
    user.code_select_function(number - 1, "")
funk wrap <user.code_functions>:
    user.code_insert_function(code_functions, edit.selected_text())
funk wrap <number>:
    user.code_select_function(number - 1, edit.selected_text())
