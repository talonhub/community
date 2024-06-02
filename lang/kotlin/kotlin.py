from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()
ctx.matches = r"""
code.language: kotlin
"""

# Java Modifies
ctx.lists["user.code_keyword"] = {
    "var": "var ",
    "val": "val ",
    "lateinit": "lateinit ",
    "public": "public ",
    "private": "private ",
    "protected": "protected ",
    "static": "static ",
    "synchronized": "synchronized ",
    "volatile": "volatile ",
    "transient": "transient ",
    "abstract": "abstract ",
    "interface": "interface ",
    "final": "final ",
}


@ctx.action_class("user")
class UserActions:
    def code_comment_line_prefix():
        actions.insert("// ")

    def code_operator_lambda():
        actions.auto_insert(" -> ")

    def code_operator_subscript():
        actions.user.insert_between("[", "]")

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

    def code_insert_null():
        actions.insert("null")

    def code_insert_is_null():
        actions.insert(" == null")

    def code_insert_is_not_null():
        actions.insert(" != null")

    def code_state_if():
        actions.user.insert_between("if (", ") ")

    def code_state_else_if():
        actions.user.insert_between("else if (", ") ")

    def code_state_else():
        actions.user.insert_between(" else {", "}")
        actions.key("enter")

    def code_state_switch():
        actions.user.insert_between("switch (", ") ")

    def code_state_case():
        actions.insert("case \nbreak;")
        actions.edit.up()

    def code_state_for():
        actions.user.insert_between("for (", ") ")

    def code_state_while():
        actions.user.insert_between("while (", ") ")

    def code_define_class():
        actions.auto_insert("class ")

    def code_state_return():
        actions.insert("return ")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_default_function(text: str):
        result = "fun {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )
        actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        actions.user.code_default_function(text)

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "private fun {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )
        actions.user.code_insert_function(result, None)
