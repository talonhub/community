tag: user.r
-
tag(): user.code_imperative

tag(): user.code_comment_line
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_functions_gui
tag(): user.code_libraries
tag(): user.code_libraries_gui
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_math

settings():
    user.code_private_function_formatter = "SNAKE_CASE"
    user.code_protected_function_formatter = "SNAKE_CASE"
    user.code_public_function_formatter = "SNAKE_CASE"
    user.code_private_variable_formatter = "SNAKE_CASE"
    user.code_protected_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"

# NOTE: migrated from generic as it is only use here
(op | is) in: " %in% "

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

# TODO: migrate to function tag
^function define <user.text>$: user.code_private_function(text)

named arg {user.code_parameter_name}: user.code_insert_named_argument(code_parameter_name)
