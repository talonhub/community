code.language: c
code.language: cpp
-
tag(): user.code_imperative

tag(): user.code_block_c_like
tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_data_bool
tag(): user.code_data_null
# tag(): user.code_functions
tag(): user.code_functions_common
tag(): user.code_libraries
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
    user.code_protected_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"

# NOTE: migrated from generic, as they were only used here, though once cpp support is added, perhaps these should be migrated to a tag together with the commands below

include system: user.insert_between("#include <", ">")
include local: user.insert_between('#include "', '"')
include <user.code_libraries>:
    user.code_insert_library(code_libraries, "")

state type deaf: insert("typedef ")
state type deaf struct:
    insert("typedef struct")
    insert("{\n\n}")
    edit.up()
    key('tab')preprocessor

# XXX - create a preprocessor tag for these, as they will match cpp, etc
# state define: "#define "
# state (undefine | undeaf): "#undef "
# state if (define | deaf): "#ifdef "
[state] define <user.text>$:
    "#define {user.formatted_text(text, 'ALL_CAPS,SNAKE_CASE')}"
[state] (undefine | undeaf) <user.text>$:
    "#undef {user.formatted_text(text, 'ALL_CAPS,SNAKE_CASE')}"
[state] if (define | deaf) <user.text>$:
    "#ifdef {user.formatted_text(text, 'ALL_CAPS,SNAKE_CASE')}"



# XXX - preprocessor instead of pre?
state pre if: "#if "
state error: "#error "
state pre else if: "#elif "
state pre end: "#endif "
state pragma: "#pragma "
state default: "default:\nbreak;"

#control flow
#best used with a push like command
#the below example may not work in editors that automatically add the closing brace
#if so uncomment the two lines and comment out the rest accordingly
push (brace|braces):
    edit.line_end()
    insert("{")
    key(enter)
    # insert("{}")
    # edit.left()
    # key(enter)
    # key(enter)
    # edit.up()

push (semi|semicolon):
     edit.line_end()
     insert(";")
     key(enter)

# Declare variables or structs etc.
# Ex. * int myList
(var|variable) <user.c_variable> <phrase>:
    insert("{c_variable} ")
    insert(user.formatted_text(phrase, "SNAKE_CASE,NO_SPACES"))

# <user.c_variable> <user.letter>: insert("{c_variable} {letter} ")


cast to <user.c_type>: "({c_type})"


type <user.c_type>: "{c_type}"
[qualify|qualifier] <user.c_qualifier_list>: "{c_qualifier_list}"


## declaration of (local) variables
# "var unsigned you int thity two pointer foo' -> uint_32 *foo;
(var|variable) [<user.c_qualifier_list>] <user.c_type> <user.c_variable>:
    qualifiers = c_qualifier_list or ""
    insert("{qualifiers}{c_type} {c_variable}")

[<user.c_qualifier_list>] <user.c_type> funky <user.text>:
    qualifiers = c_qualifier_list or ""
    insert("{qualifiers} {text}")

int main: user.insert_between("int main(", ")")
