# TODO: remove unncessary imports copy pasted from python.py

from talon import Context, Module, actions, app, settings

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators

mod = Module()
ctx = Context()
ctx.matches = r"""
code.language: haskell
"""


# TODO: change teh python copy pasta to haskell + test
operators = Operators(
    # code_operators_array
    SUBSCRIPT=" !! ",
    # code_operators_assignment
    ASSIGNMENT=" = ",
    # don't really exist except for library lens
    # ASSIGNMENT_SUBTRACTION=" -= ",
    # ASSIGNMENT_ADDITION=" += ",
    # ASSIGNMENT_MULTIPLICATION=" *= ",
    # ASSIGNMENT_DIVISION=" /= ",
    # ASSIGNMENT_MODULO=" %= ",
    # ASSIGNMENT_INCREMENT=" += 1",
    # ASSIGNMENT_BITWISE_AND=" &= ",
    # ASSIGNMENT_BITWISE_OR=" |= ",
    # ASSIGNMENT_BITWISE_EXCLUSIVE_OR=" ^= ",
    # ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    # ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    # code_operators_bitwise
    # requires Data.Bits import
    BITWISE_NOT="complement ",
    BITWISE_AND=" .&. ",
    BITWISE_OR=" .|. ",
    BITWISE_EXCLUSIVE_OR=" .^. ",
    BITWISE_LEFT_SHIFT=" `shiftL` ",
    BITWISE_RIGHT_SHIFT=" `shiftR` ",
    # code_operators_lambda
    LAMBDA=create_described_insert_between("\\", "-> "),
    # code_operators_math
    MATH_SUBTRACT=" - ",
    MATH_ADD=" + ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_INTEGER_DIVIDE=" `div` ",
    MATH_MODULO=" `mod` ",
    MATH_EXPONENT=" ** ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" /= ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" && ",
    MATH_OR=" || ",
    MATH_NOT=" not ",
    MATH_IN=" in ",
    MATH_NOT_IN=" not in ",
)


def haskell_and_null_warning():
    app.notify(
        """For the method null see common functions.
        Otherwise you can't check for undefined in Haskell, which is not quite null anway.
        Maybe use Maybe type instead.
        See https://stackoverflow.com/questions/35198674/can-i-declare-a-null-value-in-haskell
        """
    )


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_insert_null():
        actions.insert("undefined")
        haskell_and_null_warning()

    def code_insert_is_null():
        actions.insert("null ")
        haskell_and_null_warning()

    def code_insert_is_not_null():
        haskell_and_null_warning()

    def code_insert_true():
        actions.insert("True")

    def code_insert_false():
        actions.insert("False")

    def code_insert_function(text: str, selection: str):
        text += f" {selection or ''}"
        actions.insert(text)
        # actions.user.paste in ghci loses the trailing space

    def code_default_function(text: str):
        actions.user.code_public_function(text)

    def code_private_function(text: str):
        app.notify("no private functions in haskell")

    def code_public_function(text: str):
        """Deliberately not adding = because that is easy to add
        You wanna call this twice because the type annotations are in a seperate line"""
        result = actions.user.formatted_text(
            text, settings.get("user.code_public_function_formatter")
        )

        actions.user.paste(result)

    def code_insert_type_annotation(type: str):
        actions.insert(f" {type} ")

    def code_insert_return_type(type: str):
        actions.insert(f" -> {type}")
