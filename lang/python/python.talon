code.language: python
-
tag(): user.code_imperative
tag(): user.code_object_oriented

tag(): user.code_comment_documentation
tag(): user.code_comment_line
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
    user.code_private_function_formatter = "SNAKE_CASE"
    user.code_protected_function_formatter = "SNAKE_CASE"
    user.code_public_function_formatter = "SNAKE_CASE"
    user.code_private_variable_formatter = "SNAKE_CASE"
    user.code_protected_variable_formatter = "SNAKE_CASE"
    user.code_public_variable_formatter = "SNAKE_CASE"

#python-specific grammars
dunder in it: "__init__"
state (def | deaf | deft): "def "
state try: "try:\n"
state except: "except "
state raise: "raise "
self taught: "self."
pie test: "pytest"
state past: "pass"

[state] raise {user.python_exception}:
    user.insert_between("raise {python_exception}(", ")")
[state] except {user.python_exception}: "except {python_exception}:"

dock string: user.code_comment_documentation()
dock {user.python_docstring_fields}:
    insert("{python_docstring_fields}")
    edit.left()
dock type {user.code_type}: user.insert_between(":type ", ": {code_type}")
dock returns type {user.code_type}: user.insert_between(":rtype ", ": {code_type}")

import <user.code_libraries>:
    user.code_insert_library(code_libraries, "")
    key(end enter)

from import: user.insert_snippet_by_name("importFromStatement")

# the generic type commands are currently unstable and may be subject to change

# examples of using the <user.python_generic_type> capture:
# "list of string" -> list[str]
# "list of string or integer" -> list[str | int]
# types can be nested with `of`:
# "list of optional of integer" -> list[Optional[int]]
# `and` can be used for multiple arguments: 
# "tuple of integer and float" -> tuple[int, float]
# `done` can be used to exit a nesting:
# "tuple of optional of integer done string" -> tuple[Optional[int], str]

<user.python_generic_type>: insert(python_generic_type)
returns <user.python_generic_type>: insert(" -> {python_generic_type}")
is type <user.python_generic_type>: insert(": {python_generic_type}")