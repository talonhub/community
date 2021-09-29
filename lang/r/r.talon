mode: command
and mode: user.r
mode: command
and mode: user.auto_lang
and code.language: r
-
# TODO: functions

tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_generic
settings():
    user.code_private_function_formatter = "SNAKE_CASE"
    user.code_protected_function_formatter = "SNAKE_CASE"
    user.code_public_function_formatter = "SNAKE_CASE"
    user.code_private_variable_formatter = "SNAKE_CASE"
    user.code_protected_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"
toggle library: user.code_toggle_libraries()
library <user.code_libraries>:
    user.code_insert_library(code_libraries, "")
    key(end enter)

# R specific commands
(chain|pipe that):
    key(end)
    " %>%"
    key(enter)
state na:
    insert("NA")
    
^function define <user.text>$: user.code_private_function(text)

named arg {user.code_parameter_name}: user.code_insert_named_argument(code_parameter_name)