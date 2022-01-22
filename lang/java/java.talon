mode: user.java
mode: user.auto_lang
and code.language: java
-
tag(): user.code_imperative
tag(): user.code_object_oriented

tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_functions_gui
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
boxed [type] {user.java_boxed_types}:
    insert(user.java_boxed_types)
    key("space")

generic [type] {user.java_generic_data_structures}:
    insert(java_generic_data_structures)
    insert("<>")
    key("left")

# Arrays
type {user.code_type} array:
    insert(user.code_type)
    user.code_operator_subscript()

[state] {user.java_access_modifiers}:
    insert(user.java_access_modifiers)
    key("space")

[state] {user.java_modifiers}:
    insert(user.java_modifiers)
    key("space")

op array:
    user.code_operator_subscript()

op new:
    insert("new ")
