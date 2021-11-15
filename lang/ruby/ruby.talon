mode: command
and mode: user.ruby
mode: command
and mode: user.auto_lang
and code.language: ruby
-
tag(): user.code_base_imperative
tag(): user.code_base_object_oriented
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_lambda
tag(): user.code_operators_math
tag(): user.code_comment

settings():
    user.code_private_function_formatter = "SNAKE_CASE"
    user.code_protected_function_formatter = "SNAKE_CASE"
    user.code_public_function_formatter = "SNAKE_CASE"
    user.code_private_variable_formatter = "SNAKE_CASE"
    user.code_protected_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"

^funky <user.text>$: user.code_default_function(text)

args pipe:
    insert("||")
    key(left)

# TODO: duplicate from tag code_base_imperative?
state do: "do "
state end: "end"
state begin: "begin"
state rescue: "rescue "
state module: "module "
^instance <user.text>$:
    insert("@")
    user.code_public_variable_formatter(text)
