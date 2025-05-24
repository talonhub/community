code.language: elixir
-
tag(): user.code_functional
tag(): user.code_concurrent

tag(): user.code_comment_line
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_keywords
tag(): user.code_libraries
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_math
tag(): user.code_operators_lambda

settings():
    user.code_private_function_formatter = "SNAKE_CASE"
    user.code_public_function_formatter = "SNAKE_CASE"
    user.code_private_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"

# Elixir-specific grammars
state def: "def "
state defp: "defp "
state if: "if "
state else: "else"
state case: "case "
state cond: "cond do"
state try: "try do"
state rescue: "rescue"
state after: "after"
state end: "end"

op pipe: " |> "

# Elixir-specific keywords and symbols
[state] raise {user.elixir_exception}: user.insert_between("raise ", "")

[state] rescue {user.elixir_exception}: "rescue {elixir_exception}"
