tag: user.javascript
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

(op | is) strict equal: " === "
(op | is) strict not equal: " !== "

state const: "const "

state let: "let "

state var: "var "

state export: "export "

state async: "async "

state await: "await "

state map:
    user.insert_between(".map(", ")")

state filter:
    user.insert_between(".filter(", ")")

state reduce:
    user.insert_between(".reduce(", ")")

state spread: "..."

from import:
    user.insert_between(' from  "', '"')
