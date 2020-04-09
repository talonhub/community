code.language: csharp
-
settings():
    user.lang_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.lang_protected_function_formatter = "PROTECTED_CAMEL_CASE"
    user.lang_public_function_formatter = "PROTECTED_CAMEL_CASE"
    user.lang_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.lang_protected_variable_formatter = "PROTECTED_CAMEL_CASE"
    user.lang_public_variable_formatter = "PROTECTED_CAMEL_CASE"

action(user.lang_operator_equal): " == "
action(user.lang_operator_not_equal): " != "
action(user.lang_operator_and): " and "
action(user.lang_operator_or): " or "
action(user.lang_operator_minus): " - "
action(user.lang_operator_minus_equals): " -= "
action(user.lang_operator_plus): " + "
action(user.lang_operator_plus_equals): " += "
action(user.lang_operator_multiply): " * "
action(user.lang_operator_multiply_equals): " *= "
action(user.lang_operator_exponent): " ** "
action(user.lang_operator_divide): " / "
action(user.lang_operator_divide_equals): " /= "
action(user.lang_operator_modulo): " % "
action(user.lang_operator_modulo_equals): " %= "
action(user.lang_operator_greater_than): " > "
action(user.lang_operator_greater_than_equals): " >= "
action(user.lang_operator_less_than): " < "
action(user.lang_operator_less_than_equals): " <= "
action(user.lang_bitwise_operator_and): " & "
action(user.lang_bitwise_operator_or): " | "
action(user.lang_bitwise_operator_exlcusive_or): " ^ "
action(user.lang_bitwise_operator_exlcusive_or_equals): " ^= "
action(user.lang_bitwise_operator_left_shift): " << "
action(user.lang_bitwise_operator_left_shift_equals): " <<= "
action(user.lang_bitwise_operator_right_shift): " >> "
action(user.lang_bitwise_operator_right_shift_equals): " >>= "
action(user.lang_null): "null"
action(user.lang_is_null): " == null"
action(user.lang_is_not_null): " != null"
action(user.lang_self): "this"
action(user.lang_state_if): 
	insert("if()")
	key(left)
action(user.lang_state_else_if): 
	insert("else if()")
	key(left)
action(user.lang_state_else): 
	insert("else\n{{\n}}\n")
	key(up )
action(user.lang_state_switch):
	insert("switch()") 
	edit.left()
action(user.lang_state_case):
	insert("case \nbreak;") 
	edit.up()
action(user.lang_state_for): "for "
action(user.lang_state_for_each): 
	insert("foreach() ")
	key(left)
	edit.word_left()
	key(space) 
	edit.left()
action(user.lang_state_go_to): "go to "
action(user.lang_state_while): 
	insert("while()")
	edit.left()
action(user.lang_type_definition): "typedef "	
action(user.lang_typedef_struct):	
	insert("typedef struct")
	insert("{{\n\n}}")
	edit.up()
	key(tab)
action(user.lang_type_class): "class "
action(user.lang_import): "using  "
action(user.lang_from_import):
	insert("from import ")
	key(left)
	edit.word_left()
	key(space) 
	edit.left()
action(user.lang_include):
	insert("using ")
	edit.left()
action(user.lang_include_system):
	insert("using ")
	edit.left()
action(user.lang_include_local):
	insert('using ')
	edit.left()
action(user.lang_comment_here): "//"
 
action(user.lang_private_function): insert("private ")
action(user.lang_public_static_function): insert("private static  ")
action(user.lang_protected_function): insert("protected  ")
action(user.lang_public_function): insert("public  ")
action(user.lang_public_static_function): insert("public static ")


	
