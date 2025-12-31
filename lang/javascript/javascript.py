from talon import Context, Module, actions, settings

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators

mod = Module()
ctx = Context()
ctx.matches = r"""
code.language: javascript
code.language: typescript
code.language: javascriptreact
code.language: typescriptreact
"""

ctx.lists["user.code_common_method"] = {
    "catch": "catch",
    "concat": "concat",
    "filter": "filter",
    "finally": "finally",
    "find": "find",
    "flat map": "flatMap",
    "for each": "forEach",
    "join": "join",
    "includes": "includes",
    "map": "map",
    "pop": "pop",
    "push": "push",
    "reduce": "reduce",
    "slice": "slice",
    "some": "some",
    "split": "split",
    "substring": "substring",
    "then": "then",
}

ctx.lists["user.code_keyword"] = {
    "a sink": "async ",
    "await": "await ",
    "break": "break",
    "class": "class ",
    "const": "const ",
    "continue": "continue",
    "default": "default ",
    "export": "export ",
    "false": "false",
    "function": "function ",
    "import": "import ",
    "let": "let ",
    "new": "new ",
    "null": "null",
    "private": "private ",
    "protected": "protected ",
    "public": "public ",
    "return": "return ",
    "throw": "throw ",
    "true": "true",
    "try": "try ",
    "undefined": "undefined",
    "yield": "yield ",
}

operators = Operators(
    # code_operators_array
    SUBSCRIPT=create_described_insert_between("[", "]"),
    # code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_OR=" ||= ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_DIVISION=" /= ",
    ASSIGNMENT_MODULO=" %= ",
    ASSIGNMENT_INCREMENT="++",
    ASSIGNMENT_BITWISE_AND=" &= ",
    ASSIGNMENT_BITWISE_OR=" |= ",
    ASSIGNMENT_BITWISE_EXCLUSIVE_OR=" ^= ",
    ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    # code_operators_bitwise
    BITWISE_AND=" & ",
    BITWISE_OR=" | ",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    BITWISE_RIGHT_SHIFT=" >> ",
    # code_operators_lambda
    LAMBDA=" => ",
    # code_operators_math
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EXPONENT=" ** ",
    MATH_EQUAL=" === ",
    MATH_NOT_EQUAL=" !== ",
    MATH_OR=" || ",
    MATH_AND=" && ",
    MATH_GREATER_THAN=" > ",
    MATH_LESS_THAN=" < ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_WEAK_EQUAL=" == ",
    MATH_WEAK_NOT_EQUAL=" != ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_insert_is_not_null():
        actions.auto_insert(" !== null")

    def code_insert_is_null():
        actions.auto_insert(" === null")

    def code_self():
        actions.auto_insert("this")

    def code_operator_object_accessor():
        actions.auto_insert(".")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_insert_null():
        actions.auto_insert("null")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_default_function(text: str):
        """Inserts function declaration without modifiers"""
        result = "function {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

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
