from talon import Context, Module, actions, settings

from ..tags.operators import Operators

ctx = Context()
mod = Module()
ctx.matches = r"""
code.language: scala
"""

# Scala Common Types
scala_common_types = {
    "boolean": "Boolean",
    "int": "Int",
    "float": "Float",
    "byte": "Byte",
    "double": "Double",
    "short": "Short",
    "long": "Long",
    "char": "Char",
    "unit": "Unit",
    "any": "Any",
    "any val": "AnyVal",
    "string": "String",
    "thread": "Thread",
    "exception": "Exception",
    "throwable": "Throwable",
    "none": "None",
    "success": "Success",
    "failure": "Failure",
}

# Scala Common Generic Types
scala_common_generic_types = {
    "array": "Array",
    "deck": "Deque",
    "future": "Future",
    "list": "List",
    "map": "Map",
    "nil": "Nil",
    "option": "Option",
    "queue": "Queue",
    "seek": "Seq",
    "set": "Set",
    "some": "Some",
    "stack": "Stack",
    "try": "Try",
}

scala_types = scala_common_types.copy()
scala_types.update(scala_common_generic_types)
ctx.lists["user.code_type"] = scala_types

# Scala Modifies
scala_modifiers = {
    "public": "public",
    "private": "private",
    "protected": "protected",
}

mod.list("scala_modifier", desc="Scala Modifiers")
ctx.lists["user.scala_modifier"] = scala_modifiers

scala_keywords = {
    "abstract": "abstract",
    "case class": "case class",
    "def": "def",
    "extends": "extends",
    "implicit": "implicit",
    "lazy val": "lazy val",
    "new": "new",
    "object": "object",
    "override": "override",
    "package": "package",
    "sealed": "sealed",
    "throw": "throw",
    "trait": "trait",
    "type": "type",
    "val": "val",
    "var": "var",
    "with": "with",
    "yield": "yield",
}

mod.list("scala_keyword", desc="Scala Keywords")
ctx.lists["user.scala_keyword"] = scala_keywords

operators = Operators(
    # code_operators_array
    SUBSCRIPT=lambda: actions.user.insert_between("(", ")"),
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
    BITWISE_NOT="~",
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
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_NOT="!",
    MATH_OR=" || ",
    MATH_AND=" && ",
    MATH_EXPONENT=" ^ ",
    MATH_GREATER_THAN=" > ",
    MATH_LESS_THAN=" < ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_self():
        actions.insert("this")

    def code_insert_null():
        actions.insert("null")

    def code_insert_is_null():
        actions.insert(" == null")

    def code_insert_is_not_null():
        actions.insert(" != null")

    def code_break():
        actions.insert("break")

    def code_next():
        actions.insert("continue")

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    def code_state_return():
        actions.insert("return ")

    def code_comment_block_prefix():
        actions.insert("/*")

    def code_comment_block_suffix():
        actions.insert("*/")

    def code_insert_type_annotation(type: str):
        actions.insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.insert(f": {type}")

    def code_operator_object_accessor():
        actions.insert(".")

    def code_default_function(text: str):
        """Inserts function declaration"""
        actions.user.code_public_function(text)

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + f"({selection})"
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "private def {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_function(text: str):
        result = "protected def {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        result = "def {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)
