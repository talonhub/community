tag: user.vimscript
-
tag(): user.code_imperative
tag(): user.code_operators_assignment
tag(): user.code_operators_math
tag(): user.code_comment_line

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
assign [<user.vimscript_scope>] (variable|var) [<user.text>] [over]:
    insert("let ")
    insert(vimscript_scope or '')
    user.code_private_variable_formatter(text)

[<user.vimscript_scope>] (variable|var) [<user.text>] [over]:
    insert(vimscript_scope or '')
    user.code_private_variable_formatter(text)

# see lang/vimscript/vimscript.py for list
<user.vimscript_functions>:
    insert("{vimscript_functions} ")

# XXX - possibly overlap with some programming.talon
state command: "command! "
state end if: "endif"
state end for: "endfor"
state end while: "endwhile"
state end function: "endfunction"
state continue: "continue"
