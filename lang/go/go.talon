code.language: go
-

tag(): user.code_comment_block_c_like
tag(): user.code_comment_documentation

tag(): user.code_data_bool
tag(): user.code_data_null

tag(): user.code_functions
tag(): user.code_functions_common
tag(): user.code_imperative
tag(): user.code_libraries

tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_lambda
tag(): user.code_operators_math
tag(): user.code_operators_pointer

settings:
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_public_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PUBLIC_CAMEL_CASE"
    user.code_public_variable_formatter = "PUBLIC_CAMEL_CASE"

(main|mane) function: user.code_private_function("main")

[state] context: " ctx "
[state] context (are you|argue): " ctx context.Context "
state any: " any "

state (air | err): "err"
error: " err "