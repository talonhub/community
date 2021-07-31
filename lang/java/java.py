from talon import Context, Module, actions

ctx = Context()
mod = Module()
ctx.matches = r"""
mode: user.java
mode: user.auto_lang
and code.language: java
"""
ctx.tags = ["user.code_operators", "user.code_generic"]

java_primitive_types = {
    "boolean": "boolean",
    "int": "int",
    "string": "String",
    "float": "float",
    "byte": "byte",
    "double": "double",
    "short": "short",
    "long": "long",
    "char": "char",
    "void": "void"
}

mod.list("java_primitive_types", desc="Java types")
ctx.lists["self.java_primitive_types"] = java_primitive_types

java_access_modifiers = {
   "public": "public",
   "private": "private",
   "protected": "protected",
}

mod.list("java_access_modifiers", desc="Java Access Modifiers")
ctx.lists["self.java_access_modifiers"] = java_access_modifiers

java_other_modifiers = {
   "static": "static",
   "synchronized": "synchronized",
   "volatile": "volatile",
   "transient": "transient",
   "abstract": "abstract",
   "interface": "interface",
}

mod.list("java_other_modifiers", desc="Java Other Modifiers")
ctx.lists["self.java_other_modifiers"] = java_other_modifiers

@ctx.action_class("user")
class UserActions:
    def code_operator_indirection():
        actions.skip()

    def code_operator_address_of():
        actions.skip()

    def code_operator_lambda():
        actions.auto_insert(" -> ")

    def code_operator_subscript():
        actions.insert("[]")
        actions.key("left")

    def code_operator_assignment():
        actions.auto_insert(" = ")

    def code_operator_subtraction():
        actions.auto_insert(" - ")

    def code_operator_subtraction_assignment():
        actions.auto_insert(" -= ")

    def code_operator_addition():
        actions.auto_insert(" + ")

    def code_operator_addition_assignment():
        actions.auto_insert(" += ")

    def code_operator_multiplication():
        actions.auto_insert(" * ")

    def code_operator_multiplication_assignment():
        actions.auto_insert(" *= ")

    def code_operator_exponent():
        actions.auto_insert(" ^ ")

    def code_operator_division():
        actions.auto_insert(" / ")

    def code_operator_division_assignment():
        actions.auto_insert(" /= ")

    def code_operator_modulo():
        actions.auto_insert(" % ")

    def code_operator_modulo_assignment():
        actions.auto_insert(" %= ")

    def code_operator_equal():
        actions.auto_insert(" == ")

    def code_operator_not_equal():
        actions.auto_insert(" != ")

    def code_operator_greater_than():
        actions.auto_insert(" > ")

    def code_operator_greater_than_or_equal_to():
        actions.auto_insert(" >= ")

    def code_operator_less_than():
        actions.auto_insert(" < ")

    def code_operator_less_than_or_equal_to():
        actions.auto_insert(" <= ")

    def code_operator_and():
        actions.auto_insert(" && ")

    def code_operator_or():
        actions.auto_insert(" || ")

    def code_operator_bitwise_and():
        actions.auto_insert(" & ")

    def code_operator_bitwise_and_assignment():
        actions.auto_insert(' &= ')

    def code_operator_increment():        
        actions.auto_insert('++')

    def code_operator_bitwise_or():
        actions.auto_insert(" | ")

    def code_operator_bitwise_exclusive_or():
        actions.auto_insert(" ^ ")

    def code_operator_bitwise_left_shift():
        actions.auto_insert(" << ")

    def code_operator_bitwise_left_shift_assignment():
        actions.auto_insert(" <<= ")

    def code_operator_bitwise_right_shift():
        actions.auto_insert(" >> ")

    def code_operator_bitwise_right_shift_assignment():
        actions.auto_insert(" >>= ")

    def code_self():
        actions.auto_insert("this")

    def code_null():
        actions.auto_insert("null")

    def code_is_null():
        actions.auto_insert(" == null")

    def code_is_not_null():
        actions.auto_insert(" != null")

    def code_state_if():
        actions.insert("if () ")
        actions.key("left")
        actions.key("left")

    def code_state_else_if():
        actions.insert("else if () ")
        actions.key("left")
        actions.key("left")

    def code_state_else():
        actions.insert("else ")
        actions.key("enter")

    def code_state_switch():
        actions.insert("switch () ")
        actions.key("left")
        actions.edit.left()

    def code_state_case():
        actions.insert("case \nbreak;")
        actions.edit.up()

    def code_state_for():
        actions.insert("for () ")
        actions.key("left")
        actions.key("left")

    def code_state_while():
        actions.insert("while () ")
        actions.edit.left()
        actions.edit.left()

    def code_type_class():
        actions.auto_insert("class ")

    def code_private_function(text: str):
        actions.insert("private")

    def code_protected_function(text: str):
        actions.user.code_private_function()

    def code_public_function(text: str):
        actions.insert("public ")

    def code_state_return():
        actions.insert("return ")
