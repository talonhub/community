tag: user.java
-
tag(): user.code_imperative
tag(): user.code_object_oriented

tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_libraries
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_lambda
tag(): user.code_operators_math

settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_variable_formatter = "PRIVATE_CAMEL_CASE"

# Types Commands
boxed [type] {user.java_boxed_type}:
    insert(user.java_boxed_type + " ")

generic [type] {user.java_generic_data_structure}:
    user.insert_between(java_generic_data_structure + "<", ">")

# Arrays
type {user.code_type} array:
    insert(user.code_type)
    user.code_operator_subscript()

[state] {user.java_modifier}:
    insert(user.java_modifier + " ")

op array:
    user.code_operator_subscript()

op new:
    insert("new ")
