from talon import Context, actions, settings, app

from ..tags.operators import Operators

ctx = Context()
ctx.matches = r"""
code.language: csharp
"""

operators: Operators
def on_ready():
    global operators
    operators = Operators(
        # code_operators_array
        SUBSCRIPT=actions.user.described_function_create_insert_between("[", "]"),
        # code_operators_assignment
        ASSIGNMENT=" = ",
        ASSIGNMENT_ADDITION=" += ",
        ASSIGNMENT_SUBTRACTION=" -= ",
        ASSIGNMENT_DIVISION=" /= ",
        ASSIGNMENT_MULTIPLICATION=" *= ",
        ASSIGNMENT_MODULO=" %= ",
        ASSIGNMENT_BITWISE_AND=" &= ",
        ASSIGNMENT_BITWISE_EXCLUSIVE_OR=" ^= ",
        ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
        ASSIGNMENT_BITWISE_OR=" |= ",
        ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
        ASSIGNMENT_INCREMENT="++",
        # code_operators_bitwise
        BITWISE_NOT="~",
        BITWISE_AND=" & ",
        BITWISE_EXCLUSIVE_OR=" ^ ",
        BITWISE_LEFT_SHIFT=" << ",
        BITWISE_OR=" | ",
        BITWISE_RIGHT_SHIFT=" >> ",
        # code_operators_lambda
        LAMBDA="=>",
        # code_operators_pointer
        MATH_ADD=" + ",
        MATH_SUBTRACT=" - ",
        MATH_MULTIPLY=" * ",
        MATH_DIVIDE=" / ",
        MATH_MODULO=" % ",
        MATH_EQUAL=" == ",
        MATH_NOT_EQUAL=" != ",
        MATH_OR=" || ",
        MATH_AND=" && ",
        MATH_NOT="!",
        MATH_GREATER_THAN_OR_EQUAL=" >= ",
        MATH_GREATER_THAN=" > ",
        MATH_LESS_THAN_OR_EQUAL=" <= ",
        MATH_LESS_THAN=" < ",
        # code_operators_pointer
        POINTER_ADDRESS_OF="&",
        POINTER_INDIRECTION="*",
        POINTER_STRUCTURE_DEREFERENCE="->",
    )

app.register("ready", on_ready)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_self():
        actions.auto_insert("this")

    def code_operator_object_accessor():
        actions.auto_insert(".")

    def code_insert_null():
        actions.auto_insert("null")

    def code_insert_is_null():
        actions.auto_insert(" == null ")

    def code_insert_is_not_null():
        actions.auto_insert(" != null")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "private void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_private_static_function(text: str):
        """Inserts private static function"""
        result = "private static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_function(text: str):
        result = "private void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_static_function(text: str):
        result = "protected static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        result = "public void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_static_function(text: str):
        result = "public static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)
