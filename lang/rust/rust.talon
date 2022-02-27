tag: user.rust
-
tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_comment_documentation

tag(): user.code_imperative
tag(): user.code_object_oriented

tag(): user.code_data_bool
tag(): user.code_data_null

tag(): user.code_functions
tag(): user.code_functions_gui

tag(): user.code_libraries
tag(): user.code_libraries_gui

tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_math

settings():
    user.code_private_function_formatter = "SNAKE_CASE"
    user.code_protected_function_formatter = "SNAKE_CASE"
    user.code_public_function_formatter = "SNAKE_CASE"
    user.code_private_variable_formatter = "SNAKE_CASE"
    user.code_protected_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"

# rust-specific grammars
borrow: "&"
borrow mutable: "&mut "
state constant: "const "
state dynamic: "dyn "
state (funk | func | function): "fn "
state implements: "impl "
state mutable: "mut "
state static: "static "
state (struct | structure): "struct "
self taught: "self."

## specialist flow control
if let some: user.code_insert_if_let_some()
if let error: user.code_insert_if_let_error()

## rust centric synonyms
is (some|sum): user.code_insert_is_not_null()

## for implementing
implement: user.code_state_implements()

## for annotating function parameters
is implemented trait {user.code_trait}: user.code_insert_trait_annotation(code_trait)
is implemented trait: ": impl "
returns implemented trait {user.code_trait}: user.code_insert_return_trait(code_trait)
returns implemented trait: " -> impl "

## for generic reference of traits
trait {user.code_trait}: insert("{code_trait}")
implemented trait {user.code_trait}: insert("impl {code_trait}")
dynamic trait {user.code_trait}: insert("dyn {code_trait}")

## for generic reference of macro
macro <user.code_macros>:
    user.code_insert_macro(code_macros, "")
macro array <user.code_macros>:
    user.code_insert_macro_array(code_macros, "")
macro block <user.code_macros>:
    user.code_insert_macro_block(code_macros, "")
macro wrap <user.code_macros>:
    user.code_insert_macro(code_macros, edit.selected_text())
macro array wrap <user.code_macros>:
    user.code_insert_macro_array(code_macros, edit.selected_text())
macro block wrap <user.code_macros>:
    user.code_insert_macro_block(code_macros, edit.selected_text())

## for unsafe rust
state unsafe: "unsafe "
unsafe block: user.code_state_unsafe()

toggle imports: user.code_toggle_libraries()
import <user.code_libraries>:
    user.code_insert_library(code_libraries, "")
    key(end enter)
state use: user.code_import()
use library <user.code_libraries>:
    user.code_insert_library(code_libraries, "")
    key(end enter)
