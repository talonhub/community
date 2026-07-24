from talon import Context, Module, actions

from ..tags.operators import Operators

mod = Module()
ctx = Context()
ctx.matches = """
code.language: css
code.language: scss
"""

mod.list("css_at_rule", desc="List of CSS @rules")
mod.list("css_unit", desc="List of CSS units")
mod.list("css_global_value", desc="CSS-wide values")

operators = Operators(
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_AND=" and ",
    MATH_OR=" or ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_insert_function(text: str, selection: str):
        substitutions = {"1": text}
        if selection:
            substitutions["0"] = selection
        actions.user.insert_snippet_by_name("functionCall", substitutions)
