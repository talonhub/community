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
state def:
    user.deprecate_command("2026-11-11", "state def", "put def")
    insert("def ")
state defp:
    user.deprecate_command("2026-11-11", "state defp", "put def p")
    insert("defp ")
state if:
    user.deprecate_command("2026-11-11", "state if", "put if")
    insert("if ")
state else:
    user.deprecate_command("2026-11-11", "state else", "put else")
    insert("else")
state case:
    user.deprecate_command("2026-11-11", "state case", "put case")
    insert("case ")
state cond: "cond do"
state try: "try do"
state rescue:
    user.deprecate_command("2026-11-11", "state rescue", "put rescue")
    insert("rescue")
state after:
    user.deprecate_command("2026-11-11", "state after", "put after")
    insert("after")
state end:
    user.deprecate_command("2026-11-11", "state end", "put end")
    insert("end")

op pipe: " |> "
