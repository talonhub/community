tag: user.julia
-
tag(): user.code_imperative

tag(): user.code_comment_line
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_functions_common
tag(): user.code_keywords
tag(): user.code_operators_assignment
tag(): user.code_operators_array
tag(): user.code_operators_math

settings():
	user.code_private_function_formatter = "SNAKE_CASE"
	user.code_public_function_formatter = "SNAKE_CASE"
    user.code_private_variable_formatter = "SNAKE_CASE"
    user.code_protected_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"

[state] [at] assert: "@assert "
[state] [at] dassert one: "@dassert1 "
[state] [at] dassert two: "@dassert2 "

state end: "end"

maps to: " => "

symbol <user.text>: ":{user.formatted_text(text, 'SNAKE_CASE')}"
