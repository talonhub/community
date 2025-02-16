from talon import Context, actions, settings

from ..tags.operators import Operators

ctx = Context()
ctx.matches = r"""
code.language: csharp
"""
ctx.lists["user.code_common_function"] = {
    "integer": "int.TryParse",
    "print": "Console.WriteLine",
    "string": ".ToString",
}

operators = Operators(
    # code_operators_array
    SUBSCRIPT=lambda: actions.user.insert_between("[", "]"),
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

    def code_state_if():
        actions.user.insert_between("if(", ")")

    def code_state_else_if():
        actions.user.insert_between("else if(", ")")

    def code_state_else():
        actions.insert("else\n{\n}\n")
        actions.key("up")

    def code_state_switch():
        actions.user.insert_between("switch(", ")")

    def code_state_case():
        actions.insert("case \nbreak;")
        actions.edit.up()

    def code_state_for():
        actions.auto_insert("for ")

    def code_state_for_each():
        actions.insert("foreach() ")
        actions.key("left")
        actions.edit.word_left()
        actions.key("space")
        actions.edit.left()

    def code_state_go_to():
        actions.auto_insert("go to ")

    def code_state_while():
        actions.user.insert_between("while(", ")")

    def code_state_return():
        actions.auto_insert("return ")

    def code_break():
        actions.auto_insert("break;")

    def code_next():
        actions.auto_insert("continue;")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_define_class():
        actions.auto_insert("class ")

    def code_import():
        actions.auto_insert("using  ")

    def code_comment_line_prefix():
        actions.auto_insert("//")

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
