mode: user.typescript
mode: command 
and code.language: typescript
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
    user.code_type_formatter = "PUBLIC_CAMEL_CASE"
    user.code_interface_formatter = "PUBLIC_CAMEL_CASE"

action(user.code_is_not_null): " !== null"

action(user.code_is_null): " === null"

action(user.code_type_dictionary):
  insert("{}")
  key(left)

action(user.code_state_if):
  insert("if () {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left left)

action(user.code_state_else_if):
  insert(" else if () {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left left)

action(user.code_state_else):
  insert(" else () {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left left)

action(user.code_self): "this"

action(user.code_state_while):
  insert("while () {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left left)

action(user.code_state_do):
  insert("do {}")
  edit.left()
  key(enter)
  edit.down()
  edit.line_end()
  insert(" while()")
  edit.left()

action(user.code_state_return):
  insert("return ")

action(user.code_state_for):
  insert("for () {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left left)

action(user.code_state_switch):
  insert("switch () {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left left)

action(user.code_state_case):
  "case :\n\tbreak;"
  edit.up()
  edit.line_end()
  edit.left()

action(user.code_state_go_to): ""

action(user.code_import): "import "

action(user.code_from_import):
  insert(" from  \"\"")
  key(left)

action(user.code_type_class):
  insert("class  {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  edit.left()
  edit.left()

action(user.code_include): ""

action(user.code_include_system): ""

action(user.code_include_local): ""

action(user.code_type_definition): ""

action(user.code_typedef_struct): ""

action(user.code_state_for_each):
  insert(".forEach()")
  key(left)

action(user.code_null): "null"

action(user.code_private_function):
  insert("private  {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left)

action(user.code_protected_function):
  insert("protected  {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left)

action(user.code_public_function):
  insert("public  {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left)

action(user.code_operator_indirection): ""
action(user.code_operator_address_of): ""
action(user.code_operator_structure_deference): ""
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
action(user.code_operator_bitwise_exlcusive_or): " ^ "
action(user.code_operator_bitwise_exlcusive_or_assignment): " ^= "
action(user.code_operator_bitwise_left_shift): " << "
action(user.code_operator_bitwise_left_shift_assignment): " <<= "
action(user.code_operator_bitwise_right_shift): " >> "
action(user.code_operator_bitwise_right_shift_assignment): " >>= "

state inline block:
  insert("{{  }}")
  key(left left)

state block:
  insert("{}")
  key(left enter)

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

^state export class <user.text>$:
  insert("export class  {}")
  edit.left()
  key(enter)
  edit.up()
  edit.line_end()
  key(left left)
  user.code_type_formatter(user.text)

^state extends <user.text>$:
  insert(" extends ")
  user.code_type_formatter(user.text)

^state implements <user.text>$:
  insert(" implements I")
  user.code_interface_formatter(user.text)

^state param <user.text>$:
  user.code_private_variable_formatter(user.text)
  insert(": ")

^state next param <user.text>$:
  insert(", ")
  user.code_private_variable_formatter(user.text)
  insert(": ")

state return default:
  edit.right()
  insert(": ")
  insert("void")

^state return type <user.text>$:
  edit.right()
  insert(": ")
  user.code_type_formatter(user.text)
