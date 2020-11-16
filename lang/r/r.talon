mode: user.r
mode: command
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
action(user.code_operator_assignment): " <- "
action(user.code_operator_subtraction): " - "
action(user.code_operator_addition): " + "
action(user.code_operator_multiplication): " * "
action(user.code_operator_exponent): " ** "
action(user.code_operator_division): " / "
action(user.code_operator_modulo): " %% "
action(user.code_operator_equal): " == "
action(user.code_operator_not_equal): " != "
action(user.code_operator_greater_than): " > "
action(user.code_operator_greater_than_or_equal_to): " >= "
action(user.code_operator_less_than): " < "
action(user.code_operator_less_than_or_equal_to): " <= "
action(user.code_operator_in): " %in% "
action(user.code_operator_and): " & "
action(user.code_operator_or): " | "
action(user.code_operator_bitwise_and): " & "
action(user.code_null): "NULL"
action(user.code_state_if):
    insert("if () {}")
    key(left enter up end left:3)
action(user.code_state_else_if):
    insert(" else if () {}")
    key(left enter up end left:3)
action(user.code_state_else):
    insert(" else {}")
    key(left enter)
action(user.code_state_for):
    insert("for ( in ) {}")
    key(left enter up end left:7)
action(user.code_state_while):
    insert("while () {}")
    key(left enter up end left:3)
toggle library: user.code_toggle_libraries()
library <user.code_libraries>:
    user.code_insert_library(code_libraries, "")
    key(end enter)
action(user.code_import):
    insert("library()")
    key(left)
action(user.code_comment): "#"
action(user.code_state_return):
   insert("return()")
   key(left)
action(user.code_break): "break"
action(user.code_next): "next"
action(user.code_true): "TRUE"
action(user.code_false): "FALSE"

# R specific commands
(chain|pipe that):
    key(end)
    " %>%"
    key(enter)
state na:
    insert("NA")

^function define <user.text>$: user.code_private_function(text)
