from talon import Context, Module, actions

mod = Module()
ctx = Context()
ctx.matches = r"""
code.language: go
"""


def base_function(text: str, visibility: str):
    """Inserts a public function definition, this assumes a lot about how your editor works"""
    result = f"func {actions.user.formatted_text(text, visibility)}() {{\n\n}}"

    actions.user.insert_between(f"func {text}() {{\n", "")


@ctx.action_class("user")
class UserActions:
    def code_insert_true():
        actions.auto_insert(" true ")

    def code_insert_false():
        actions.auto_insert(" false ")

    def code_insert_null():
        actions.auto_insert(" nil ")

    def code_insert_is_null():
        actions.auto_insert(" == nil ")

    def code_insert_is_not_null():
        actions.auto_insert(" != nil ")

    def code_comment_documentation():
        """inserts godoc syntax"""
        actions.key("up")
        actions.auto_insert("// ")

    def code_default_function(text: str):
        if text == "main" or text == "mane":
            actions.user.code_private_function("main")
        else:
            actions.user.code_public_function(text)

    def code_public_function(text: str):
        base_function(text, "PUBLIC_CAMEL_CASE")

    def code_private_function(text: str):
        base_function(text, "PRIVATE_CAMEL_CASE")

    def code_insert_function(text: str, selection: str):
        actions.insert(text)
        actions.insert("()")
        actions.key("left")
        actions.insert(selection)

    def code_block():
        actions.user.insert_between("{\n", "")

    def code_state_if():
        actions.user.insert_between(" if ", " {")

    def code_state_else_if():
        actions.user.insert_between(" else if ", " {")

    def code_state_else():
        actions.insert(" else ")
        actions.user.code_block()

    def code_state_while():
        actions.user.code_state_for()

    def code_state_infinite_loop():
        actions.insert("for ")
        actions.user.code_block()

    def code_state_for():
        actions.user.insert_between("for ", " {")

    def code_state_for_each():
        actions.user.insert_between("for _, ", " := range  {")

    def code_state_switch():
        actions.user.insert_between("switch ", " {")

    def code_state_case():
        actions.user.insert_between("case ", ":")

    def code_state_go_to():
        actions.insert("goto ")

    def code_state_return():
        actions.insert("return ")

    def code_break():
        actions.insert("break ")

    def code_next():
        actions.insert("continue")

    def code_import():
        actions.user.insert_between("import (", ")")
        actions.insert("\n")

    def code_operator_subscript():
        actions.user.insert_between("[", "]")

    def code_operator_assignment():
        actions.auto_insert(" = ")

    def code_operator_subtraction_assignment():
        actions.auto_insert(" -= ")

    def code_operator_addition_assignment():
        actions.auto_insert(" += ")

    def code_operator_multiplication_assignment():
        actions.auto_insert(" *= ")

    def code_operator_division_assignment():
        actions.auto_insert(" /= ")

    def code_operator_modulo_assignment():
        actions.auto_insert(" %= ")

    def code_operator_increment():
        actions.auto_insert(" ++ ")

    def code_operator_bitwise_and_assignment():
        actions.auto_insert(" &= ")

    def code_operator_bitwise_or_assignment():
        actions.auto_insert(" |= ")

    def code_operator_bitwise_exclusive_or_assignment():
        actions.auto_insert(" ^= ")

    def code_operator_bitwise_left_shift_assignment():
        actions.auto_insert(" <<= ")

    def code_operator_bitwise_right_shift_assignment():
        actions.auto_insert(" >>= ")

    def code_operator_bitwise_and():
        actions.auto_insert(" & ")

    def code_operator_bitwise_or():
        actions.auto_insert(" | ")

    def code_operator_bitwise_exclusive_or():
        actions.auto_insert(" ^ ")

    def code_operator_bitwise_left_shift():
        actions.auto_insert(" << ")

    def code_operator_bitwise_right_shift():
        actions.auto_insert(" >> ")

    def code_operator_lambda():
        actions.user.insert_between("func() {", "}")

    def code_operator_subtraction():
        actions.auto_insert(" - ")

    def code_operator_addition():
        actions.auto_insert(" + ")

    def code_operator_multiplication():
        actions.auto_insert(" * ")

    def code_operator_division():
        actions.auto_insert(" / ")

    def code_operator_modulo():
        actions.auto_insert(" % ")

    def code_operator_equal():
        actions.auto_insert(" == ")

    def code_operator_not_equal():
        actions.auto_insert(" != ")

    def code_operator_less_than():
        actions.auto_insert(" < ")

    def code_operator_greater_than():
        actions.auto_insert(" > ")

    def code_operator_less_than_or_equal_to():
        actions.auto_insert(" <= ")

    def code_operator_greater_than_or_equal_to():
        actions.auto_insert(" >= ")

    def code_operator_and():
        actions.auto_insert(" && ")

    def code_operator_or():
        actions.auto_insert(" || ")

    def code_operator_indirection():
        actions.auto_insert("*")

    def code_operator_address_of():
        actions.auto_insert("&")

    def code_operator_structure_dereference():
        actions.auto_insert(".")
