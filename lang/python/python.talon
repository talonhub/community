mode: command
and mode: user.python
mode: command
and mode: user.auto_lang
and code.language: python
-
tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_generic
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

^funky <user.text>$: user.code_default_function(text)
#^pro funky <user.text>$: user.code_protected_function(text)
^pub funky <user.text>$: user.code_public_function(text)
#^static funky <user.text>$: user.code_private_static_function(text)
#^pro static funky <user.text>$: user.code_protected_static_function(text)
#^pub static funky <user.text>$: user.code_public_static_function(text)
raise {user.python_exception}: user.insert_cursor("raise {python_exception}([|])")
except {user.python_exception}: "except {python_exception}:"

dock {user.python_docstring_fields}:
    insert("{python_docstring_fields}")
    edit.left()
dock type {user.code_type}:
    user.insert_cursor(":type [|]: {code_type}")
dock returns type {user.code_type}:
    user.insert_cursor(":rtype [|]: {code_type}")
toggle imports: user.code_toggle_libraries()
import <user.code_libraries>:
    user.code_insert_library(code_libraries, "")
    key(end enter)
