mode: user.java
mode: user.auto_lang
and code.language: java
-
tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_block_comment
tag(): user.code_generic

action(user.code_public_function):
 	insert("public ")
action(user.code_state_return):
    insert("return ")

action(user.code_state_import):
    insert("import ")

[state] {user.java_access_modifiers} : 
    insert(user.java_access_modifiers)
    key("space")
[state] {user.java_primitive_types}: 
    insert(user.java_primitive_types)
    key("space")