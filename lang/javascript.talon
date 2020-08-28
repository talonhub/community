mode: user.javascript
mode: command
and code.language: javascript
-
tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_generic

settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_variable_formatter = "PRIVATE_CAMEL_CASE"

action(user.code_is_not_null): " !== null"

action(user.code_is_null): " === null"

action(user.code_type_dictionary):
  insert("{}")
  key(left)

action(user.code_state_if):
  insert("if ()")
  key(left)

action(user.code_state_else_if):
  insert(" else if ()")
  key(left)

action(user.code_state_else):
  insert(" else {}")
  key(left enter)

action(user.code_block): 
  insert("{}") 
  key(left enter)
  
action(user.code_self): "this"

action(user.code_state_while):
  insert("while ()")
  key(left)

action(user.code_state_return):
  insert("return ")

action(user.code_state_for):
  insert("for ()")
  key(left)

action(user.code_state_switch):
  insert("switch ()")
  key(left)

action(user.code_state_case): "case :"

action(user.code_state_go_to): ""

action(user.code_import): "import "

action(user.code_from_import):
  insert(" from  \"\"")
  key(left)

action(user.code_type_class): "class "

action(user.code_include): ""

action(user.code_include_system): ""

action(user.code_include_local): ""

action(user.code_type_definition): ""

action(user.code_typedef_struct): ""

action(user.code_state_for_each):
  insert(".forEach()")
  key(left)

action(user.code_null): "null"

action(user.code_private_function): "function "
action(user.code_protected_function): "function "
action(user.code_public_function): "function "

action(user.code_operator_indirection): ""
action(user.code_operator_address_of): ""
action(user.code_operator_structure_dereference): ""
action(user.code_operator_lambda): " => "
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
(op | is) strict equal: " === "
(op | is) strict not equal: " !== "
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

state const: "const "

state let: "let "

state var: "var "

state async: "async "

state await: "await "

state map:
  insert(".map()")
  key(left)

state filter:
  insert(".filter()")
  key(left)

state reduce:
  insert(".reduce()")
  key(left)

state spread: "..."
