from talon import Context, actions, settings

from ..tags.operators import Operators

ctx = Context()
ctx.matches = r"""
code.language: php
"""

ctx.lists["user.code_type"] = {
    "int": "int",
    "float": "float",
    "string": "string",
    "bool": "bool",
    "array": "array",
    "null": "null",
    "void": "void",
}

operators = Operators(
    # code_operators_assignment
    ASSIGNMENT=" = ",
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
    BITWISE_NOT="~",
    # code_operators_math
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EXPONENT=" ** ",
    MATH_EQUAL=" === ",
    MATH_NOT_EQUAL=" !== ",
    MATH_WEAK_EQUAL=" == ",
    MATH_WEAK_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_NOT="!",
    MATH_AND=" && ",
    MATH_OR=" || ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_self():
        actions.auto_insert("$this")

    def code_operator_object_accessor():
        actions.auto_insert("->")

    def code_define_class():
        actions.user.insert_snippet_by_name("classDeclaration")

    def code_import():
        actions.user.insert_snippet_by_name("importStatement")

    def code_comment_line_prefix():
        actions.user.insert_snippet_by_name("commentLine")

    def code_comment_block():
        actions.user.insert_snippet_by_name("commentBlock")

    def code_comment_block_prefix():
        actions.auto_insert("/*")

    def code_comment_block_suffix():
        actions.auto_insert("*/")

    def code_comment_documentation():
        actions.user.insert_snippet_by_name("commentDocumentation")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_insert_null():
        actions.auto_insert("null")

    def code_insert_is_null():
        actions.auto_insert("is_null()")
        actions.edit.left()

    def code_insert_is_not_null():
        actions.auto_insert("isset()")
        actions.edit.left()

    def code_state_if():
        actions.user.insert_snippet_by_name("ifStatement")

    def code_state_else_if():
        actions.user.insert_snippet_by_name("elseIfStatement")

    def code_state_else():
        actions.user.insert_snippet_by_name("elseStatement")

    def code_state_while():
        actions.user.insert_snippet_by_name("whileLoopStatement")

    def code_state_for():
        actions.user.insert_snippet_by_name("forLoopStatement")

    def code_state_for_each():
        actions.user.insert_snippet_by_name("forEachStatement")

    def code_state_switch():
        actions.user.insert_snippet_by_name("switchStatement")

    def code_state_case():
        actions.user.insert_snippet_by_name("caseStatement")

    def code_state_do():
        actions.user.insert_snippet_by_name("doWhileLoopStatement")

    def code_state_go_to():
        actions.insert("goto ;")
        actions.edit.left()

    def code_break():
        actions.insert("break;")

    def code_next():
        actions.insert("continue;")

    def code_default_function(text: str):
        actions.user.code_public_function(text)

    def code_protected_function(text: str):
        """Inserts protected function declaration"""
        result = "protected function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_public_function(text: str):
        """Inserts public function declaration"""
        result = "public function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "private function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_private_static_function(text: str):
        """Inserts private static function declaration"""
        result = "private static function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_protected_static_function(text: str):
        """Inserts protected static function declaration"""
        result = "protected static function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_public_static_function(text: str):
        """Inserts public static function declaration"""
        result = "public static function {}()".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()

    def code_insert_return_type(type: str):
        actions.insert(f": {type}")
