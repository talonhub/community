from talon import Module, Context, actions, settings

mod = Module()
ctx = Context()
ctx.matches = """
tag: user.javascript
"""
# tbd
# ctx.lists["user.code_functions"] = {
#     "integer": "int.TryParse",
#     "print": "Console.WriteLine",
#     "string": ".ToString",
# }


@ctx.action_class("user")
class UserActions:
    def code_insert_is_not_null():
        actions.auto_insert(" !== null")

    def code_insert_is_null():
        actions.auto_insert(" === null")

    def code_type_dictionary():
        actions.insert("{}")
        actions.key("left")

    def code_state_if():
        actions.insert("if ()")
        actions.key("left")

    def code_state_else_if():
        actions.insert(" else if ()")
        actions.key("left")

    def code_state_else():
        actions.insert(" else {}")
        actions.key("left enter")

    def code_block():
        actions.insert("{}")
        actions.key("left enter")

    def code_self():
        actions.auto_insert("this")

    def code_operator_object_accessor():
        actions.auto_insert('.')

    def code_state_while():
        actions.insert("while ()")
        actions.key("left")

    def code_state_do():
        actions.auto_insert("do ")

    def code_state_return():
        actions.insert("return ")

    def code_state_for():
        actions.insert("for ()")
        actions.key("left")

    def code_state_switch():
        actions.insert("switch ()")
        actions.key("left")

    def code_state_case():
        actions.auto_insert("case :")

    def code_state_go_to():
        actions.auto_insert("")

    def code_import():
        actions.auto_insert("import ")

    def code_define_class():
        actions.auto_insert("class ")

    def code_state_for_each():
        actions.insert(".forEach()")
        actions.key("left")

    def code_break():
        actions.auto_insert("break;")

    def code_next():
        actions.auto_insert("continue;")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_insert_null():
        actions.auto_insert("null")

    def code_operator_lambda():
        actions.auto_insert(" => ")

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
        actions.auto_insert(" ** ")

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
        actions.auto_insert(" &= ")

    def code_operator_bitwise_or():
        actions.auto_insert(" | ")

    def code_operator_bitwise_or_assignment():
        actions.auto_insert(" |= ")

    def code_operator_bitwise_exclusive_or():
        actions.auto_insert(" ^ ")

    def code_operator_bitwise_exclusive_or_assignment():
        actions.auto_insert(" ^= ")

    def code_operator_bitwise_left_shift():
        actions.auto_insert(" << ")

    def code_operator_bitwise_left_shift_assignment():
        actions.auto_insert(" <<= ")

    def code_operator_bitwise_right_shift():
        actions.auto_insert(" >> ")

    def code_operator_bitwise_right_shift_assignment():
        actions.auto_insert(" >>= ")

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "function {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    # def code_private_static_function(text: str):
    #     """Inserts private static function"""
    #     result = "private static void {}".format(
    #         actions.user.formatted_text(
    #             text, settings.get("user.code_private_function_formatter")
    #         )
    #     )

    #     actions.user.code_insert_function(result, None)

    def code_protected_function(text: str):
        result = "function {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    # def code_protected_static_function(text: str):
    #     result = "protected static void {}".format(
    #         actions.user.formatted_text(
    #             text, settings.get("user.code_protected_function_formatter")
    #         )
    #     )

    #     actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        result = "function {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    # def code_public_static_function(text: str):
    #     result = "public static void {}".format(
    #         actions.user.formatted_text(
    #             text, settings.get("user.code_public_function_formatter")
    #         )
    #     )

    #     actions.user.code_insert_function(result, None)
