from talon import Context, Module, actions

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators

mod = Module()

ctx = Context()
ctx.matches = r"""
code.language: swift
"""

# Lists and Captures #

mod.list("code_macros", desc="List of active macros for the active language")

# Macros

standard_library_macros = {
    "debug description": "@DebugDescription",
    "ob jay see": "@objc",
    "observable": "@Observable",
    "observation ignored": "@ObservationIgnored",
    "observation tracked": "@ObservationTracked",
    "resolvable": "@Resolvable",
    "task local": "@TaskLocal",
    "file": "#file",
    "file id": "#fileID",
    "file path": "#filePath",
    "function": "#function",
    "line": "#line",
    "column": "#column",
    "source location": "#sourceLocation",
    "availability": "#availability",
    "available": "#available",
    "unavailable": "#unavailable",
    "if": "#if",
    "else": "#else",
    "else if": "#elseif",
    "end if": "#endif",
    "warning": "#warning",
    "error": "#error",
    "external macro": "#externalMacro",
    "dee ess oh handle": "#dsohandle",
    "isolation": "#isolation",
}

# Types

number_types = {
    "int": "Int",
    "int eight": "Int8",
    "int sixteen": "Int16",
    "int thirty two": "Int32",
    "int sixty four": "Int64",
    "int one twenty eight": "Int128",
    "int one hundred and twenty eight": "Int128",
    "you int": "Int8",
    "you int eight": "UInt8",
    "you int sixteen": "UInt16",
    "you int thirty two": "UInt32",
    "you int sixty four": "UInt64",
    "you int one twenty eight": "UInt128",
    "you int one hundred and twenty eight": "UInt128",
    "float": "Float",
    "double": "Double",
    "float sixteen": "Float16",
    "float eighty": "Float80",
    "float thirty two": "Float32",
    "float sixty four": "Float64",
}

other_common_types = {
    "array": "[]",
    "tuple": "()",
    "bool": "Bool",
    "boolean": "Bool",
    "string": "String",
    "char": "Character",
    "character": "Character",
}

common_types = {
    **number_types,
    **other_common_types,
}

ctx.lists["user.code_type"] = common_types

# Operators
operators = Operators(
    # tag: user.code_operators_array
    SUBSCRIPT=create_described_insert_between("[", "]"),
    # tag: user.code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_DIVISION=" /= ",
    ASSIGNMENT_MODULO=" %= ",
    ASSIGNMENT_INCREMENT=" += 1 ",
    # tag: user.code_operators_bitwise
    BITWISE_AND=" & ",
    BITWISE_OR=" | ",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    BITWISE_RIGHT_SHIFT=" >> ",
    ASSIGNMENT_BITWISE_AND=" &= ",
    ASSIGNMENT_BITWISE_OR=" |= ",
    ASSIGNMENT_BITWISE_EXCLUSIVE_OR=" ^= ",
    ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    # tag: user.code_operators_math (comparisons)
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_LESS_THAN=" < ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    # tag: user.code_operators_math (basic)
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    # NEEDS FEEDBACK: pow() function requires import of Foundation; should it be included here as MATH_EXPONENT?
    MATH_AND=" && ",
    MATH_OR=" || ",
    MATH_NOT=" != ",
    # tag: user.code_operators_lambda
    LAMBDA=" -> ",
)


# Module and context action classes #


@mod.action_class
class Actions:
    def code_insert_macro(text: str):
        """Inserts the selected macro statement at the current cursor location"""

    def code_define_protocol():
        """Start a protocol definition (Swift's approximate equivalent to Java interfaces/Rust traits)"""

    def code_comment_documentation_block():
        """Inserts a block document comment and positions the cursor appropriately"""


@ctx.action_class("user")
class UserActions:
    # tags: user.code_operators_*
    def code_get_operators() -> Operators:
        return operators

    # tag: user.code_object_oriented
    def code_operator_object_accessor():
        actions.insert(".")

    def code_self():
        actions.insert("self")

    # tag: user.data_bool

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    # tag: user.code_data_null

    def code_insert_null():
        actions.insert("nil")

    def code_insert_is_null():
        actions.insert(" == nil")

    def code_insert_is_not_null():
        actions.insert(" != nil")

    # tag: user.code_functions
    # tag: user.code_functions_common
    # tag: user.code_libraries

    # Swift-specific grammar

    # def code_insert_macro(text: str):
    #    """Inserts the selected macro statement at the current cursor location"""
