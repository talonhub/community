code.language: haskell
-

tag(): user.code_comment_line
tag(): user.code_comment_block
tag(): user.code_data_bool
tag(): user.code_data_null

tag(): user.code_functions

tag(): user.code_functions_common
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_lambda
tag(): user.code_operators_math


# TODO: complete tags 

# following https://wiki.haskell.org/Programming_guidelines#Naming_Conventions
settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_variable_formatter = "PRIVATE_CAMEL_CASE"

# it is not assignement either!
op do equals: insert("<-")
op bind: insert("<-")