mode: user.java
mode: user.auto_lang
and code.language: java
-
tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_block_comment
tag(): user.code_generic

action(user.code_state_import):
    insert("import ")

# Types Commands

type {user.java_primitive_types}: 
    insert(java_primitive_types)
    key("space")

type ({user.java_common_classes}|{user.java_generic_data_structures}): 
    insert(java_common_classes or java_generic_data_structures)
    key("space")

boxed [type] {user.java_boxed_types}: 
    insert(user.java_boxed_types)
    key("space")

generic [type] {user.java_generic_data_structures}:
    insert(java_generic_data_structures)
    insert("<>")
    key("left")

# Arrays
type {user.java_primitive_types} array:
    insert(user.java_primitive_types)
    user.code_operator_subscript()

type ({user.java_common_classes}|{user.java_generic_data_structures}) array:
    insert(java_common_classes or java_generic_data_structures)
    user.code_operator_subscript()    

[state] {user.java_access_modifiers}: 
    insert(user.java_access_modifiers)
    key("space")

[state] {user.java_other_modifiers}: 
    insert(user.java_other_modifiers)
    key("space") 

op array:
    user.code_operator_subscript()

op new:
    insert("new ")
op plus plus:
    insert("++")

code_block_comment 
