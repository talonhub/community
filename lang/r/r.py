from talon import Context, actions, settings

from ..tags.operators import Operators

ctx = Context()

ctx.matches = r"""
code.language: r
"""


operators = Operators(
    # code_operators_assignment
    ASSIGNMENT=" <- ",
    # code_operators_bitwise
    BITWISE_AND=" & ",
    # code_operators_math:
    MATH_SUBTRACT=" - ",
    MATH_ADD=" + ",
    MATH_MULTIPLY=" * ",
    MATH_EXPONENT=" ** ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" %% ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" & ",
    MATH_OR=" | ",
    MATH_IN=" %in% ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_insert_null():
        actions.insert("NULL")

    def code_insert_is_null():
        actions.user.insert_between("is.null(", ")")

    def code_insert_is_not_null():
        actions.user.insert_between("!is.null(", ")")

    def code_insert_true():
        actions.insert("TRUE")

    def code_insert_false():
        actions.insert("FALSE")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        result = "{} <- function () {{\n\n}}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.paste(result)
        actions.edit.up()
        actions.edit.up()
        actions.edit.line_end()
        actions.edit.left()
        actions.edit.left()
        actions.edit.left()

    def code_insert_library(text: str, selection: str):
        actions.user.insert_snippet_by_name("importStatement", {"0": text + selection})

    def code_insert_named_argument(parameter_name: str):
        actions.insert(f"{parameter_name} = ")
