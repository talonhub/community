from talon import Context, actions

from ..tags.operators import Operators

ctx = Context()
ctx.matches = r"""
code.language: sql
"""

operators = Operators(
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_EQUAL=" = ",
    MATH_NOT_EQUAL=" <> ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_IN=lambda: actions.user.insert_between(" IN (", ")"),
    MATH_NOT_IN=lambda: actions.user.insert_between(" NOT IN (", ")"),
    MATH_AND=" AND ",
    MATH_OR=" OR ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_insert_null():
        actions.auto_insert("NULL")

    def code_insert_is_null():
        actions.auto_insert(" IS NULL")

    def code_insert_is_not_null():
        actions.auto_insert(" IS NOT NULL")

    def code_insert_function(text: str, selection: str):
        substitutions = {"1": text}
        if selection:
            substitutions["2"] = selection
        actions.user.insert_snippet_by_name("functionCall", substitutions)
