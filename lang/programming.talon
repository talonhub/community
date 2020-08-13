tag: user.code_generic
-
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
^funky <user.text>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.code_private_function()
    user.code_private_function_formatter(user.text)
    insert("()")
    edit.left()
    sleep(100ms)
^pro funky <user.text>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.code_protected_function()
    user.code_protected_function_formatter(user.text)
    #() surely isn't correct for all languages, will be part of the combined function above
    insert("()")
    key(left)
    sleep(100ms)
^pub funky <user.text>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.code_public_function()
    user.code_public_function_formatter(user.text)
    sleep(50ms)
    insert("()")
^static funky <user.text>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.code_private_static_function()
    user.code_private_function_formatter(user.text)
^pro static funky <user.text>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.code_protected_static_function()
    user.code_protected_function_formatter(user.text)
^pub static funky <user.text>$:
    #todo: once .talon action definitions can take parameters, combine these functions
	user.code_public_static_function()
    user.code_public_function_formatter(user.text)

# show and print functions
toggle funk: user.code_toggle_functions()
funk <user.code_functions>: 
    old_clip = clip.text()
    user.code_insert_function(code_functions, "")
    clip.set_text(old_clip)
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