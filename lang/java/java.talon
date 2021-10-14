mode: user.java
mode: user.auto_lang
and code.language: java
-
tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_block_comment
tag(): user.code_generic

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

# Methods    
^method <user.text>$: user.code_default_function(text)
^pro method <user.text>$: user.code_protected_function(text)
^pub method <user.text>$: user.code_public_function(text)
^static method <user.text>$: user.code_private_static_function(text)
^pro static method <user.text>$: user.code_protected_static_function(text)
^pub static method <user.text>$: user.code_public_static_function(text)
