tag: user.rust
-
tag(): user.code_imperative
tag(): user.code_object_oriented
tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_comment_documentation
tag(): user.code_data_bool
tag(): user.code_functions
tag(): user.code_functions_gui
tag(): user.code_libraries
tag(): user.code_libraries_gui
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_math
tag(): user.code_operators_pointer

settings():
    user.code_private_function_formatter = "SNAKE_CASE"
    user.code_protected_function_formatter = "SNAKE_CASE"
    user.code_public_function_formatter = "SNAKE_CASE"
    user.code_private_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"

state unsafe: "unsafe "

state struct <user.text>:
    insert("struct ")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

state enum <user.text>:
    insert("enum ")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

toggle use: user.code_toggle_libraries()

state pub: "pub "
state pub crate: "pub(crate) "
state dyn: "dyn "
state imp: "impl "
state let mute: "let mut "
state let: "let "
state mute: "mut "
state ref mute: "ref mut "
state ref: "ref "
state trait: "trait "
state match: "match "
op arrow: " -> "
op dub arrow: " => "
state use: "use "

use <user.code_libraries>:
    user.code_insert_library(code_libraries, "")
    key(semicolon enter)
