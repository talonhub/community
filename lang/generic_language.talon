code.language: python
code.language: csharp
code.language: talon

#todo tags
#tag: ???
-
#todo should we have a keyword list? type list capture?
#state in: insert(" in ")

is not none: user.language_is_not_null() 
is none: user.language_is_null()
word (dickt | dictionary): user.language_type_dictionary()
state if: user.language_state_if()
state else if: user.language_state_else_if()
state else: user.language_state_else()
state self: user.language_self()

#todo: this is valid for many languages,
# but probably not all
self taught: 
	user.language_self()
    insert(".")
state while: user.language_state_while()
state for: user.language_state_for()
state switch: user.language_state_switch()
state case: user.language_state_case()
state goto: user.language_state_go_to()
state import: user.language_import()
from import: user.language_from_import()
state class: user.language_type_class()
state include: user.language_include()
state include system: user.language_include_system()
state include local: user.language_include_local()
state type deaf: user.language_type_definition()
state type deaf struct: user.language_typedef_struct()
state for in: user.language_for_each()
state (no | nil): user.language_null()
op (equals | assign): user.language_operator_assign()
op (minus | subtract | sub): user.language_operator_minus()
[op] (minus | subtract | sub) equals: user.language_operator_minus_equals()
[op] (plus | add): user.language_operator_plus()
[op] (plus | add) equals: user.language_operator_plus_equals()
op (times | multiply): user.language_operator_multiply()
[op] (times | multiply) equals: user.language_operator_multiply_equals()
op divide: user.language_operator_divide()
op divide equals: user.language_operator_divide_equals()
op mod: user.language_operator_modulo()
[op] mod equals: user.language_operator_modulo_equals()
(op | is) (greater | more): user.language_operator_greater_than()
(op | is) (less | below) [than]: user.language_operator_less_than()
(op | is) equal: user.language_operator_equal()
(op | is) not equal: user.language_operator_not_equal()
(op | is) greater [than] or equal: user.language_operator_greater_than_equals()
(op | is) less [than] or equal: user.language_operator_less_than_equals()
(op (power | exponent) | to the power [of]): user.language_operator_exponent()
(op | logical) and: user.language_operator_and()
(op | logical) or: user.language_operator_or()
[op] bitwise and: user.language_bitwise_operator_and()
(op | logical | bitwise) and equals: user.language_bitwise_operator_and_equals()
[op] bitwise or: user.language_bitwise_operator_or()
(op | logical | bitwise) or equals: user.language_bitwise_operator_or_equals()
(op | logical | bitwise) (ex | exclusive) or: user.language_bitwise_operator_exlcusive_or()
[(op | logical | bitwise)] (left shift | shift left): user.language_bitwise_operator_left_shift()
[(op | logical | bitwise)] (right shift | shift right): user.language_bitwise_operator_right_shift()
(op | logical | bitwise) (ex | exclusive) or equals: user.language_bitwise_operator_exlcusive_or_equals()
[(op | logical | bitwise)] (left shift | shift left) equals: user.language_bitwise_operator_left_shift_equals()
[(op | logical | bitwise)] (left right | shift right) equals: user.language_bitwise_operator_right_shift_equals()

^funky <phrase>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.language_private_function()
    user.language_private_function_formatter(phrase)
    insert("()")
    edit.left()
    sleep(100ms)

^pro funky <phrase>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.language_protected_function()
    user.language_protected_function_formatter(phrase)
    #() surely isn't correct for all languages, will be part of the combined function above
    insert("()")
    key(left)
    sleep(100ms)
	
^pub funky <phrase>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.language_public_function()
    user.language_public_function_formatter(phrase)	
    sleep(50ms)
    insert("()")

^static funky <phrase>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.language_private_function()
    user.language_private_function_formatter(phrase)
	
^pro static funky <phrase>$:
    #todo: once .talon action definitions can take parameters, combine these functions
    user.language_protected_static_function()
    user.language_protected_function_formatter(phrase)

^pub static funky <phrase>$:
    #todo: once .talon action definitions can take parameters, combine these functions
	user.language_public_static_function()
    user.language_public_function_formatter(phrase)

^pub static <phrase>$:
    #todo: once .talon action definitions can take parameters, combine these functions
	user.language_public_static_function()
    user.language_public_function_formatter(phrase)

^comment$: user.language_comment()

#comments the line
^comment line$: 
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	edit.line_start()
    user.language_comment()
    
#adds comment to the start of the line
^comment line <phrase>$: 
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    edit.line_start()
    user.language_comment()
	dictate.lower(phrase)
    insert(" ")

^comment <phrase>$: 
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	user.language_comment()
	dictate.lower(phrase)
    
^(line | inline) comment <phrase>$:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	edit.line_end()
   	user.language_comment()
    dictate.lower(phrase)