mode: user.ruby
mode: command
and code.language: ruby
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

action(user.code_operator_indirection): ""
action(user.code_operator_address_of): ""
action(user.code_operator_structure_dereference): ""
action(user.code_operator_lambda): "->"
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
action(user.code_operator_exponent): " ** "
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
action(user.code_self): "self"
action(user.code_null): "nil"
action(user.code_is_null): ".nil?"
# Technically .present? is provided by Rails
action(user.code_is_not_null): ".present?"
action(user.code_state_if):
    insert("if ")
action(user.code_state_else_if):
    insert("elsif ")
action(user.code_state_else):
    insert("else")
    key(enter)
action(user.code_state_switch):
    insert("case ")
action(user.code_state_case):
    insert("when ")
action(user.code_state_for_each):
    insert(".each do ||")
    key(left)
action(user.code_type_class): "class "
action(user.code_import):
    "require \"\""
    key(left)
action(user.code_comment): "# "
action(user.code_state_return):
	insert("return ")
action(user.code_true): "true"
action(user.code_false): "false"
action(user.code_document_string):
    insert("##")
    key(enter)
    key(space)

### Extra non-standard things

^funky <user.text>$: user.code_default_function(text)

args pipe:
    insert("||")
    key(left)

state do: "do "
state end: "end"
state begin: "begin"
state rescue: "rescue "
state module: "module "

# Do instance variables
^instance <user.text>$:
    insert("@")
    user.code_public_variable_formatter(text)
