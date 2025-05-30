from talon import Context, Module, actions, settings

from ..tags.operators import Operators

ctx = Context()
mod = Module()
ctx.matches = r"""
code.language: kotlin
"""

ctx.lists["user.code_keyword"] = {
    "var": "var ",
    "val": "val ",
    "lateinit": "lateinit ",
    "public": "public ",
    "private": "private ",
    "protected": "protected ",
    "companion object": "companion object ",
    "synchronized": "synchronized ",
    "volatile": "volatile ",
    "transient": "transient ",
    "abstract": "abstract ",
    "interface": "interface ",
    "final": "final ",
    "return": "return ",
}

ctx.lists["user.code_type"] = {
    "boolean": "Boolean",
    "byte": "Byte",
    "short": "Short",
    "int": "Int",
    "long": "Long",
    "float": "Float",
    "double": "Double",
    "char": "Char",
    "string": "String",
    "array": "Array",
    "map": "Map",
    "any": "Any",
    "nothing": "Nothing",
    "unit": "Unit",
}

operators = Operators(
    # code_operators_array
    SUBSCRIPT=lambda: actions.user.insert_between("[", "]"),
    # code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_DIVISION=" /= ",
    ASSIGNMENT_MODULO=" %= ",
    ASSIGNMENT_INCREMENT="++",
    ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    # code_operators_bitwise
    BITWISE_AND=" & ",
    BITWISE_OR=" | ",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    BITWISE_RIGHT_SHIFT=" >> ",
    # code_operators_lambda
    LAMBDA=" -> ",
    # code_operators_bitwise
    MATH_SUBTRACT=" - ",
    MATH_ADD=" + ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EXPONENT=" ^ ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" && ",
    MATH_OR=" || ",
    MATH_NOT="!",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_comment_line_prefix():
        actions.user.insert_snippet_by_name("commentLine")

    def code_comment_block():
        actions.user.insert_snippet_by_name("commentBlock")

    def code_self():
        actions.auto_insert("this")

    def code_insert_null():
        actions.insert("null")

    def code_insert_is_null():
        actions.insert(" == null")

    def code_insert_is_not_null():
        actions.insert(" != null")

    def code_state_if():
        actions.user.insert_snippet_by_name("ifStatement")

    def code_state_else_if():
        actions.user.insert_snippet_by_name("elseIfStatement")

    def code_state_else():
        actions.user.insert_snippet_by_name("elseStatement")

    def code_state_switch():
        actions.user.insert_snippet_by_name("switchStatement")

    def code_state_case():
        actions.user.insert_snippet_by_name("caseStatement")

    def code_state_for():
        actions.user.insert_snippet_by_name("forEachStatement")

    def code_state_while():
        actions.user.insert_snippet_by_name("whileLoopStatement")

    def code_define_class():
        actions.user.insert_snippet_by_name("classDeclaration")

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
