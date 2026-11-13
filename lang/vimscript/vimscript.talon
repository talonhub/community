code.language: vimscript
-

tag(): user.code_imperative
tag(): user.code_operators_assignment
tag(): user.code_operators_math
tag(): user.code_comment_line
tag(): user.code_functions_common

# XXX - revisit these
settings():
    user.code_private_function_formatter = "SNAKE_CASE"
    user.code_protected_function_formatter = "SNAKE_CASE"
    user.code_public_function_formatter = "SNAKE_CASE"
    user.code_private_variable_formatter = "SNAKE_CASE"
    user.code_protected_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"

###
# VIM Script Specific
###
assign [<user.vimscript_scope>] (variable | var) [<user.text>] [over]:
    insert("let ")
    insert(vimscript_scope or "")
    user.code_private_variable_formatter(text)

[<user.vimscript_scope>] (variable | var) [<user.text>] [over]:
    insert(vimscript_scope or "")
    user.code_private_variable_formatter(text)

<user.code_common_function>: insert("{code_common_function} ")

state command: "command! "
state end if: "endif"
state end for: "endfor"
state end while: "endwhile"
state end function: "endfunction"
state continue: "continue"
