code.language: javascript
code.language: typescript
code.language: javascriptreact
code.language: typescriptreact
-
tag(): user.code_imperative
tag(): user.code_object_oriented

tag(): user.code_block_c_like
tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_functions_common
tag(): user.code_keywords
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
op null else: " ?? "

state const: "const "

state let: "let "

state var: "var "

state export: "export "

state async: "async "

state await: "await "

dot {user.code_common_member_function}:
    user.insert_between(".{code_common_member_function}(", ")")

state map: app.notify('ERROR: Command deprecated; please use "dot map"')
state filter: app.notify('ERROR: Command deprecated; please use "dot filter"')
state reduce: app.notify('ERROR: Command deprecated; please use "dot reduce"')

state spread: "..."

from import: user.insert_between(' from  "', '"')
