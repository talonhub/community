tag: user.code_generic
-
block: user.code_block()

#todo should we have a keyword list? type list capture? stick with "word"?
#state in: insert(" in ")
is not (none|null): user.code_is_not_null()
is (none|null): user.code_is_null()
#todo: types?
#word (dickt | dictionary): user.code_type_dictionary()
state if: user.code_state_if()
state else if: user.code_state_else_if()
state else: user.code_state_else()
state self: user.code_self()
#todo: this is valid for many languages,
# but probably not all
self dot:
    user.code_self()
    insert(".")
state while: user.code_state_while()
state for: user.code_state_for()
state for in: user.code_state_for_each()
state switch: user.code_state_switch()
state case: user.code_state_case()
state do: user.code_state_do()
state goto: user.code_state_go_to()
state return: user.code_state_return()
state import: user.code_import()
from import: user.code_from_import()
state class: user.code_type_class()
state include: user.code_include()
state include system: user.code_include_system()
state include local: user.code_include_local()
state type deaf: user.code_type_definition()
state type deaf struct: user.code_typedef_struct()
state (no | nil | null): user.code_null()
state break: user.code_break()
state next: user.code_next()
state true: user.code_true()
state false: user.code_false()

# show and print functions and libraries
toggle funk: user.code_toggle_functions()
toggle library: user.code_toggle_libraries()
funk <user.code_functions>:
    old_clip = clip.text()
    user.code_insert_function(code_functions, "")
    clip.set_text(old_clip)
library <user.code_libraries>:
    insert("library()")
    key(left)
    user.code_insert_library(code_libraries, "")
    key(end enter)
funk cell <number>:
    old_clip = clip.text()
    user.code_select_function(number - 1, "")
    clip.set_text(old_clip)
funk wrap <user.code_functions>:
    old_clip = clip.text()
    edit.copy()
    sleep(100ms)
    user.code_insert_function(code_functions, clip.text())
    clip.set_text(old_clip)
funk wrap <number>:
    old_clip = clip.text()
    edit.copy()
    sleep(100ms)
    user.code_select_function(number - 1, clip.text())
    clip.set_text(old_clip)
