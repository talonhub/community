code.language: python
code.language: csharp

#todo tags
#tag: ???
-
logical and: user.lang_operator_and()
logical or: user.lang_operator_or()
state in: insert(" in ")
is not none: user.lang_is_not_null() 
is none: user.lang_is_null()
empty dict: insert("{}")
word (dickt | dictionary): "dict"
state (def | deaf | deft): "def "
state if: user.lang_state_if()
state else if: user.lang_state_else_if()
state else: user.lang_state_else()
state self: user.lang_self()
self taught: 
	user.lang_self()
	insert(".")
state while: user.lang_state_while()
state for: user.lang_state_for()
state switch: user.lang_state_switch()
state case: user.lang_state_case()
state goto: user.lang_state_go_to()
state import: user.lang_import()
from import: user.lang_from_import()
state class: user.lang_type_class()
state include: user.lang_include()
state include system: user.lang_include_system()
state include local: user.lang_include_local()
state type deaf: user.lang_type_definition()
state type deaf struct: user.lang_typedef_struct()
state (for in | foreign): user.lang_for_each()
state (no | nil): user.lang_null()
op (equals | assign): user.lang_operator_assign()
op (minus | subtract | sub): user.lang_operator_minus()
[op] (minus | subtract | sub) equals: user.lang_operator_minus_equals()
[op] (plus | add): user.lang_operator_plus()
[op] (plus | add) equals: user.lang_operator_plus_equals()
op (times | multiply): user.lang_operator_multiply()
[op] (times | multiply) equals: user.lang_operator_multiply_equals()
op divide: user.lang_operator_divide()
op divide equals: user.lang_operator_divide_equals()
op mod: user.lang_operator_modulo()
[op] mod equals: user.lang_operator_modulo_equals()
(op | is) (greater | more): user.lang_operator_greater_than()
(op | is) (less | below) [than]: user.lang_operator_less_than()
(op | is) equal: user.lang_operator_equal()
(op | is) not equal: user.lang_operator_not_equal()
(op | is) greater [than] or equal: user.lang_operator_greater_than_equals()
(op | is) less [than] or equal: user.lang_operator_less_than_equals()
(op (power | exponent) | to the power [of]): user.lang_operator_exponent()
(op | logical) and: user.lang_operator_and()
(op | logical) or: user.lang_operator_or()
[op] bitwise and: user.lang_bitwise_operator_and()
(op | logical | bitwise) and equals: user.lang_bitwise_operator_and_equals()
[op] bitwise or: user.lang_bitwise_operator_or()
(op | logical | bitwise) or equals: user.lang_bitwise_operator_or_equals()
(op | logical | bitwise) (ex | exclusive) or: user.lang_bitwise_operator_exlcusive_or()
[(op | logical | bitwise)] (left shift | shift left): user.lang_bitwise_operator_left_shift()
[(op | logical | bitwise)] (right shift | shift right): user.lang_bitwise_operator_right_shift()
(op | logical | bitwise) (ex | exclusive) or equals: user.lang_bitwise_operator_exlcusive_or_equals()
[(op | logical | bitwise)] (left shift | shift left) equals: user.lang_bitwise_operator_left_shift_equals()
[(op | logical | bitwise)] (left right | shift right) equals: user.lang_bitwise_operator_right_shift_equals()

^funky <phrase>$:
    user.lang_private_function()
    user.lang_private_function_formatter(phrase)
    insert("()")
    edit.left()
    sleep(100ms)
	
^pro funky <phrase>$:
    user.lang_protected_function()
    user.lang_protected_function_formatter(phrase)
    insert("()")
	key(left)
    sleep(100ms)
	
^pub funky <phrase>$:
	user.lang_public_function()
    user.lang_public_function_formatter(phrase)
	sleep(50ms)
	insert("()")

^static funky <phrase>$:
    user.lang_private_function()
    user.lang_private_function_formatter(phrase)
	
^pro static funky <phrase>$:
    user.lang_protected_static_function()
    user.lang_protected_function_formatter(phrase)

^pub static funky <phrase>$:
	user.lang_public_static_function()
    user.lang_public_function_formatter(phrase)

^pub static <phrase>$:
	user.lang_public_static_function()
    user.lang_public_function_formatter(phrase)

^comment$: user.lang_comment_here()

^comment line$: 
	edit.line_start()
	user.lang_comment_here()

^comment <phrase>$: 
	user.lang_comment_here()
	dictate.lower(phrase)

^comment line <phrase>$: 
	edit.line_start()
    user.lang_comment_here()
	dictate.lower(phrase)
    insert(" ")
    
^(line | inline) comment <phrase>$:
	edit.line_end()
   	user.lang_comment_here()
    dictate.lower(phrase)