mode: command
and mode: user.csharp
mode: command
and mode: user.auto_lang
and code.language: csharp
-
tag(): user.code_base_imperative
tag(): user.code_base_object_oriented
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_lambda
tag(): user.code_operators_math
tag(): user.code_operators_pointer
tag(): user.code_comment_line
tag(): user.code_gui_functions

settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_public_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PUBLIC_CAMEL_CASE"
    user.code_public_variable_formatter = "PUBLIC_CAMEL_CASE"


^funky <user.text>$: user.code_default_function(text)
^pro funky <user.text>$: user.code_protected_function(text)
^pub funky <user.text>$: user.code_public_function(text)
^static funky <user.text>$: user.code_private_static_function(text)
^pro static funky <user.text>$: user.code_protected_static_function(text)
^pub static funky <user.text>$: user.code_public_static_function(text)
