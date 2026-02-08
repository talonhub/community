from contextlib import suppress

from talon import Context, Module, actions, settings

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators

ctx = Context()
mod = Module()
ctx.matches = r"""
code.language: go
"""

operators = Operators(
    # code_operators_array
    SUBSCRIPT=create_described_insert_between("[", "]"),
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
    # code_operators_lambda
    LAMBDA=" -> ",
    # code_operators_math
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_OR=" || ",
    MATH_AND=" && ",
    MATH_EXPONENT=" ^ ",
    MATH_GREATER_THAN=" > ",
    MATH_LESS_THAN=" < ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    # code_operators_pointer
    POINTER_ADDRESS_OF="&",
    POINTER_INDIRECTION="*",
)

mod.list("user.float_type_bit_width", desc="Float type bit widths")
mod.list("user.complex_type_bit_width", desc="Complex type bit widths")


@mod.capture(rule="[{user.stdint_signed}] int {user.c_type_bit_width}")
def go_int_type(m) -> str:
    """fixed-width integer types (e.g. "uint32")"""
    prefix = ""
    with suppress(AttributeError):
        prefix = m.stdint_signed
    return f"{prefix}int{m.c_type_bit_width}"


@mod.capture(rule="float {user.float_type_bit_width}")
def go_float_type(m) -> str:
    """fixed-width float types (e.g. "float32")"""
    return f"float{m.float_type_bit_width}"


@mod.capture(rule="complex {user.complex_type_bit_width}")
def go_complex_type(m) -> str:
    """fixed-width complex types (e.g. "complex64")"""
    return f"complex{m.complex_type_bit_width}"


@ctx.capture(
    "user.code_type",
    rule="{user.code_type} | {user.go_int_type} | {user.go_float_type} | {user.go_complex_type}",
)
def code_type(m) -> str:
    """All go types"""
    return "".join(list(m))


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_self():
        actions.insert("this")

    def code_operator_object_accessor():
        actions.insert(".")

    def code_insert_null():
        actions.insert("nil")

    def code_insert_is_null():
        actions.insert(" == nil")

    def code_insert_is_not_null():
        actions.insert(" != nil")

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "func {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)
