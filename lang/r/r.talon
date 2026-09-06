code.language: r
-

tag(): user.code_imperative

tag(): user.code_comment_line
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_functions_common
tag(): user.code_keywords
tag(): user.code_libraries
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

library <user.code_libraries>:
    # Import library - easier than 'snip import' for impossible to pronounce r
    # library names
    user.code_insert_library(code_libraries, "")
    key(end enter)

using <user.code_libraries>:
    # Insert library for function call, eg tidyr::
    insert(code_libraries)
    insert("::")

# R specific commands
chain | pipe that:
    key(end)
    insert(" %>%")
    key(enter)

op pipe: " %>% "
op pipe assign: " %<>% "
op pipe tee: " %T>% "
op pipe expose: " %$% "

state na:
    user.deprecate_command("2026-03-01", "state na", "put N A")
    user.insert("NA")

is N A: user.insert_between("is.na(", ")")
is not N A: user.insert_between("!is.na(", ")")

^function define <user.text>$: user.code_private_function(text)

named arg {user.code_parameter_name}:
    user.code_insert_named_argument(code_parameter_name)
