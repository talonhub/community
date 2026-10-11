import re
from contextlib import suppress
import logging

from talon import Context, Module, actions, settings

from ...core.described_functions import create_described_insert_between
from ..tags.generic_types import (
    SimpleLanguageSpecificTypeConnector,
    format_type_parameter_arguments,
)
from ..tags.operators import Operators

mod = Module()
ctx = Context()
ctx.matches = r"""
code.language: haskell
"""

# TODO: change teh python copy pasta to haskell
operators = Operators(
    # code_operators_array
    SUBSCRIPT=" !! ",
    # code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_DIVISION=" /= ",
    ASSIGNMENT_MODULO=" %= ",
    ASSIGNMENT_INCREMENT=" += 1",
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
    LAMBDA=create_described_insert_between("lambda ", ": "),
    # code_operators_math
    MATH_SUBTRACT=" - ",
    MATH_ADD=" + ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_INTEGER_DIVIDE=" // ",
    MATH_MODULO=" % ",
    MATH_EXPONENT=" ** ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" and ",
    MATH_OR=" or ",
    MATH_NOT=" not ",
    MATH_IN=" in ",
    MATH_NOT_IN=" not in ",
)

@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators


    def code_insert_null():
        actions.insert("undefined")

    def code_insert_is_null():
        logging.warning("For the method null see common functions. Otherwise you can't check for undefined in Haskell. Use Maybe type instead.")

    def code_insert_is_not_null():
        logging.warning("For the method null see common functions. Otherwise you can't check for undefined in Haskell. Use Maybe type instead.")

    def code_insert_true():
        actions.insert("True")

    def code_insert_false():
        actions.insert("False")

    def code_insert_function(text: str, selection: str):
        text += f" {selection or ''} "
        actions.user.paste(text)
        actions.edit.left()