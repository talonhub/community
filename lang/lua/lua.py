from talon import Context, Module, actions, app, settings

from ...core.described_functions import (
    create_described_function,
    create_described_insert_between,
)
from ..tags.operators import Operators

mod = Module()
ctx = Context()
ctx.matches = r"""
code.language: lua
"""

mod.setting(
    "lua_version",
    type=float,
    default=5.1,
    desc="The default lua version to use. Dictates certain operators",
)
mod.tag("stylua", desc="Tag for stylua linting commands")

ctx.lists["user.code_libraries"] = {
    "bit": "bit",
    "I O": "io",
    "string": "string",
    "U T F eight": "utf8",
    "table": "table",
    "math": "math",
    "O S": "os",
    "debug": "debug",
    "L F S": "lfs",
    "socket": "socket",
    "H T T P": "http",
    "web": "http",
    "jason": "json",
}


@mod.capture(rule="{self.lua_functions}")
def lua_functions(m) -> str:
    "Returns a string"
    return m.lua_functions


###
# code_operators_bitwise
###


# NOTE: < 5.3 assumes Lua BitOp usage
#       > 5.2 assumes native bitwise operators
# TODO: Possibly add settings to define which library to use, as 5.2
# includes bit32. Neovim uses luajit, which uses Lua BitOp
def code_operator_bitwise_and():
    if settings.get("user.lua_version") > 5.2:
        actions.insert(" & ")
    else:
        actions.insert(" bit.band() ")


def code_operator_bitwise_or():
    if settings.get("user.lua_version") > 5.2:
        actions.insert(" | ")
    else:
        actions.insert(" bit.bor() ")


def code_operator_bitwise_exclusive_or():
    if settings.get("user.lua_version") > 5.2:
        actions.insert(" ~ ")
    else:
        actions.insert(" bit.xor() ")


def code_operator_bitwise_left_shift():
    if settings.get("user.lua_version") > 5.2:
        actions.insert(" << ")
    else:
        actions.insert(" bit.lshift() ")


def code_operator_bitwise_right_shift():
    if settings.get("user.lua_version") > 5.2:
        actions.insert(" >> ")
    else:
        actions.insert(" bit.rshift() ")


operators = Operators(
    # code_operators_array
    SUBSCRIPT=create_described_insert_between("[", "]"),
    # code_operators_assignment
    ASSIGNMENT=" = ",
    # code_operators_bitwise
    BITWISE_AND=create_described_function(
        code_operator_bitwise_and, "insert bitwise and based on lua version"
    ),
    BITWISE_OR=create_described_function(
        code_operator_bitwise_or, "insert bitwise or based on lua version"
    ),
    BITWISE_EXCLUSIVE_OR=create_described_function(
        code_operator_bitwise_exclusive_or,
        "insert bitwise exclusive or based on lua version",
    ),
    BITWISE_LEFT_SHIFT=create_described_function(
        code_operator_bitwise_left_shift,
        "insert bitwise left shift based on lua version",
    ),
    BITWISE_RIGHT_SHIFT=create_described_function(
        code_operator_bitwise_right_shift,
        "insert bitwise right shift based on lua version",
    ),
    # code_operators_assignment
    MATH_SUBTRACT=" - ",
    MATH_ADD=" + ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_INTEGER_DIVIDE=" // ",
    MATH_MODULO=" % ",
    MATH_EXPONENT=" ^ ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" ~= ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" and ",
    MATH_OR=" or ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    # tag-related actions listed first, indicated by comment. corresponds to
    # the tag(): user.code_imperative style declaration in the language .talon
    # file

    ##
    # code_comment_block
    ##
    def code_comment_block_prefix():
        actions.insert("--[[")

    def code_comment_block_suffix():
        actions.insert("--]]")

    ##
    # code_data_bool
    ##
    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    ##
    # code_data_null
    ##
    def code_insert_null():
        actions.insert("nil")

    def code_insert_is_null():
        actions.insert(" == nil")

    def code_insert_is_not_null():
        actions.insert(" ~= nil")

    ##
    # code_functions
    ##
    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "local function {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.insert("\n\nend")
        actions.key("up:2")
        actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        result = "function {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.insert("\n\nend")
        actions.key("up:2")
        actions.user.code_insert_function(result, None)

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + f"({selection})"
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    ##
    # code_libraries
    ##
    def code_insert_library(text: str, selection: str):
        substitutions = {"1": selection, "0": selection}
        actions.user.insert_snippet_by_name("importStatement", substitutions)

    # non-tag related actions
