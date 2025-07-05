code.language: php
-
tag(): user.code_imperative
tag(): user.code_object_oriented
tag(): user.code_libraries

tag(): user.code_comment_line
tag(): user.code_comment_block
tag(): user.code_comment_documentation
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_operators_assignment
tag(): user.code_operators_math
tag(): user.code_functions

settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_variable_formatter = "PRIVATE_CAMEL_CASE"

(op | is) loosely equal:
    user.deprecate_command("2025-03-20", "(op | is) loosely equal", "is weak equal")
    insert(" == ")
(op | is) loosely not equal:
    user.deprecate_command("2025-03-20", "(op | is) loosely not equal", "is weak not equal")
    insert(" != ")

state try: user.insert_snippet_by_name("tryStatement")
state catch: user.insert_snippet_by_name("catchStatement")

var <phrase> [over]:
    insert("$")
    insert(user.formatted_text(phrase, "PRIVATE_CAMEL_CASE"))
