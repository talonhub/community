mode: user.csharp
mode: user.auto_lang
and code.language: csharp
-
tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_generic
settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_public_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PUBLIC_CAMEL_CASE"
    user.code_public_variable_formatter = "PUBLIC_CAMEL_CASE"

action(user.code_operator_indirection): "*"
action(user.code_operator_address_of): "&"
action(user.code_operator_structure_dereference): "->"
action(user.code_operator_lambda): "=>"
action(user.code_operator_subscript):
    insert("[]")
    key(left)
action(user.code_operator_assignment): " = "
action(user.code_operator_subtraction): " - "
action(user.code_operator_subtraction_assignment): " -= "
action(user.code_operator_addition): " + "
action(user.code_operator_addition_assignment): " += "
action(user.code_operator_multiplication): " * "
action(user.code_operator_multiplication_assignment): " *= "
#action(user.code_operator_exponent): " ** "
action(user.code_operator_division): " / "
action(user.code_operator_division_assignment): " /= "
action(user.code_operator_modulo): " % "
action(user.code_operator_modulo_assignment): " %= "
action(user.code_operator_equal): " == "
action(user.code_operator_not_equal): " != "
action(user.code_operator_greater_than): " > "
action(user.code_operator_greater_than_or_equal_to): " >= "
action(user.code_operator_less_than): " < "
action(user.code_operator_less_than_or_equal_to): " <= "
action(user.code_operator_and): " && "
action(user.code_operator_or): " || "
action(user.code_operator_bitwise_and): " & "
action(user.code_operator_bitwise_and_assignment): " &= "
action(user.code_operator_bitwise_or): " | "
action(user.code_operator_bitwise_or_assignment): " |= "
action(user.code_operator_bitwise_exclusive_or): " ^ "
action(user.code_operator_bitwise_exclusive_or_assignment): " ^= "
action(user.code_operator_bitwise_left_shift): " << "
action(user.code_operator_bitwise_left_shift_assignment): " <<= "
action(user.code_operator_bitwise_right_shift): " >> "
action(user.code_operator_bitwise_right_shift_assignment): " >>= "
action(user.code_block):
    insert("{}")
	key(left enter enter up tab)
action(user.code_self): "this"
action(user.code_null): "null"
action(user.code_is_null): " == null "
action(user.code_is_not_null): " != null"
action(user.code_state_if):
    insert("if()")
    key(left)
action(user.code_state_else_if):
    insert("else if()")
    key(left)
action(user.code_state_else):
    insert("else\n{{\n}}\n")
    key(up )
action(user.code_state_switch):
    insert("switch()")
    edit.left()
action(user.code_state_case):
    insert("case \nbreak;")
    edit.up()
action(user.code_state_for): "for "
action(user.code_state_for_each):
    insert("foreach() ")
    key(left)
    edit.word_left()
    key(space)
    edit.left()
action(user.code_state_go_to): "go to "
action(user.code_state_while):
    insert("while()")
    edit.left()
action(user.code_state_return): "return "
action(user.code_break): "break;"
action(user.code_next): "continue;"
action(user.code_true): "true"
action(user.code_false): "false"

#action(user.code_type_definition): "typedef "
#action(user.code_typedef_struct):
#    insert("typedef struct")
#    insert("{{\n\n}}")
#    edit.up()
#    key(tab)
action(user.code_type_class): "class "
action(user.code_import): "using  "
action(user.code_from_import): "using "
action(user.code_include): insert("using ")
action(user.code_include_system): insert("using ")
action(user.code_include_local): insert('using ')
action(user.code_comment): "//"

^funky <user.text>$: user.code_default_function(text)
^pro funky <user.text>$: user.code_protected_function(text)
^pub funky <user.text>$: user.code_public_function(text)
^static funky <user.text>$: user.code_private_static_function(text)
^pro static funky <user.text>$: user.code_protected_static_function(text)
^pub static funky <user.text>$: user.code_public_static_function(text)