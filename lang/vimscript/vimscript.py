from talon import Context, Module, actions, settings

from ..tags.operators import Operators

mod = Module()
ctx = Context()
ctx.matches = r"""
code.language: vimscript
"""


mod.list("vimscript_scope", desc="vimscript scoping types for functions and variables")


@mod.capture(rule="<user.code_common_function>")
def vimscript_functions(m) -> str:
    actions.user.deprecate_capture("2026-11-10", "user.vimscript_functions")
    return m.code_common_function


@mod.capture(rule="{user.vimscript_scope}")
def vimscript_scope(m) -> str:
    return m.vimscript_scope


operators = Operators(
    # code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_DIVISION=" /= ",
    # code_operators_math
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
)


def code_function_declaration(text: str, formatter: str):
    formatted_text = actions.user.formatted_text(text, settings.get(formatter))
    actions.user.insert_snippet_by_name("functionDeclaration", {"1": formatted_text})


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_private_function(text: str):
        code_function_declaration(text, "user.code_private_function_formatter")

    def code_protected_function(text: str):
        code_function_declaration(text, "user.code_protected_function_formatter")

    def code_public_function(text: str):
        code_function_declaration(text, "user.code_public_function_formatter")

    def code_insert_function(text: str, selection: str):
        substitutions = {"1": text}
        if selection:
            substitutions["0"] = selection
        actions.user.insert_snippet_by_name("functionCall", substitutions)
