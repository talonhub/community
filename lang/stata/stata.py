from talon import Context, actions, settings

from ..tags.operators import Operators

ctx = Context()

ctx.matches = r"""
code.language: stata
"""

# functions.py
ctx.lists["user.code_parameter_name"] = {
    # regressions
    "V C E cluster": "vce(cluster)",
    "V C E robust": "vce(robust)",
}

# functions_common.py
ctx.lists["user.code_common_function"] = {
    # base stata
    "global": "global",
    "local": "local",
    "reg": "reg",
    "regress": "reg",
    # packages
    "estadd": "estadd",
    "estout": "estout",
    "estpost": "estpost",
    "eststo": "eststo",
    "esttab": "esttab",
}

# libraries.py
ctx.lists["user.code_libraries"] = {
    "estout": "estout",
}

operators = Operators(
    # code_operators_array
    SUBSCRIPT=lambda: actions.user.insert_between("[", "]"),
    # code_operators_assignment
    ASSIGNMENT=" = ",
    # code_operators_math
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=lambda: actions.user.insert_between("mod(", ")"),
    MATH_EXPONENT=" ^ ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" & ",
    MATH_OR=" | ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    # functions.py
    def code_private_function(text: str):
        result = "program {} \n\nend".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.up()
        actions.key("tab")

    def code_default_function(text: str):
        actions.user.code_private_function(text)

    def code_insert_named_argument(parameter_name: str):
        actions.insert(f"{parameter_name} ")

    # functions_common.py
    def code_insert_function(text: str, selection: str):
        substitutions = {"1": text}
        if selection:
            substitutions["0"] = selection
        actions.user.insert_snippet_by_name("functionCall", substitutions)

    # imperative.py
    def code_block():
        actions.auto_insert("\n")

    def code_break():
        actions.insert("break")

    def code_next():
        actions.insert("continue")

    # libraries.py
    def code_insert_library(text: str, selection: str):
        library_text = text + selection
        actions.user.insert_snippet_by_name("importStatement", {"0": library_text})
