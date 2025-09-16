from contextlib import suppress

from talon import Context, Module, actions, settings

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators

mod = Module()

ctx = Context()
ctx.matches = r"""
code.language: c
"""

c_and_cpp_ctx = Context()
c_and_cpp_ctx.matches = r"""
code.language: c
code.language: cpp
"""

c_and_cpp_ctx.lists["user.c_pointers"] = {
    "pointer": "*",
    "pointer to pointer": "**",
}

c_and_cpp_ctx.lists["user.stdint_signed"] = {
    "signed": "",
    "unsigned": "u",
    "you": "u",
}

c_and_cpp_ctx.lists["user.c_type_bit_width"] = {
    "eight": "8",
    "sixteen": "16",
    "thirty two": "32",
    "sixty four": "64",
}

c_and_cpp_ctx.lists["user.c_signed"] = {
    "signed": "signed",
    "unsigned": "unsigned",
}

c_and_cpp_ctx.lists["user.stdint_types"] = {
    "character": "int8_t",
    "char": "int8_t",
    "short": "int16_t",
    "long": "int32_t",
    "long long": "int64_t",
    "int": "int32_t",
    "integer": "int32_t",
    "void": "void",
    "double": "double",
    "struct": "struct",
    "struck": "struct",
    "num": "enum",
    "union": "union",
    "float": "float",
}

c_and_cpp_ctx.lists["user.c_types"] = {
    "character": "char",
    "char": "char",
    "short": "short",
    "long": "long",
    "long long": "long long",
    "int": "int",
    "integer": "int",
    "void": "void",
    "double": "double",
    "long double": "long double",
    "struct": "struct",
    "struck": "struct",
    "num": "enum",
    "union": "union",
    "float": "float",
    "size tea": "size_t",
}

ctx.lists["user.code_libraries"] = {
    "assert": "assert.h",
    "type": "ctype.h",
    "error": "errno.h",
    "float": "float.h",
    "limits": "limits.h",
    "locale": "locale.h",
    "math": "math.h",
    "set jump": "setjmp.h",
    "signal": "signal.h",
    "arguments": "stdarg.h",
    "definition": "stddef.h",
    "input": "stdio.h",
    "output": "stdio.h",
    "library": "stdlib.h",
    "string": "string.h",
    "time": "time.h",
    "standard int": "stdint.h",
}

mod.list("c_pointers", desc="Common C pointers")
mod.list("c_signed", desc="Common C datatype signed modifiers")
mod.list("c_types", desc="Common C types")
mod.list("stdint_types", desc="Common stdint C types")
mod.list("stdint_signed", desc="Common stdint C datatype signed modifiers")
mod.list("c_type_bit_width", desc="Common C type bit widths")


# capture explicitly referenced from the C++ files
@mod.capture(rule="(fix|fixed) [{user.stdint_signed}] [int] {user.c_type_bit_width}")
def c_fixed_integer(m) -> str:
    """fixed-width integer types (e.g. "uint32_t")"""
    prefix = ""
    with suppress(AttributeError):
        prefix = m.stdint_signed
    return f"{prefix}int{m.c_type_bit_width}_t"


@mod.capture(rule="{user.c_pointers}")
def c_pointers(m) -> str:
    """A C pointer"""
    return m.c_pointers


# capture explicitly referenced from the C++ files
@mod.capture(rule="{user.c_signed}")
def c_signed(m) -> str:
    """Used for prefixing a signed or unsigned type"""
    return m.c_signed


# capture explicitly referenced from the C++ files
@mod.capture(rule="{user.c_types}")
def c_types(m) -> str:
    """Used for C data types"""
    return m.c_types


@mod.capture(rule="{user.stdint_types}")
def stdint_types(m) -> str:
    """Used for stdint types"""
    return m.stdint_types


@mod.capture(rule="{user.stdint_signed}")
def stdint_signed(m) -> str:
    """Used for a signed or unsigned prefix"""
    return m.stdint_signed


@mod.capture(rule="[<user.c_signed>] <user.c_types> [<user.c_pointers>+]")
def c_cast(m) -> str:
    """C casting"""
    return "(" + " ".join(list(m)) + ")"


@mod.capture(rule="[<user.stdint_signed>] <user.stdint_types> [<user.c_pointers>+]")
def stdint_cast(m) -> str:
    """C stdint casting"""
    return "(" + "".join(list(m)) + ")"


@mod.capture(rule="[<user.c_signed>] <user.c_types> [<user.c_pointers>]")
def c_variable(m) -> str:
    """Used to dictate a full C variable type"""
    return " ".join(list(m))


operators = Operators(
    SUBSCRIPT=create_described_insert_between("[", "]"),
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
    BITWISE_AND=" & ",
    BITWISE_OR=" | ",
    BITWISE_NOT="~",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    BITWISE_RIGHT_SHIFT=" >> ",
    MATH_SUBTRACT=" - ",
    MATH_ADD=" + ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" && ",
    MATH_OR=" || ",
    MATH_NOT="!",
    POINTER_INDIRECTION="*",
    POINTER_ADDRESS_OF="&",
    POINTER_STRUCTURE_DEREFERENCE="->",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_insert_null():
        actions.auto_insert("NULL")

    def code_insert_is_null():
        actions.auto_insert(" == NULL ")

    def code_insert_is_not_null():
        actions.auto_insert(" != NULL")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + f"({selection})"
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    # TODO - it would be nice that you integrate that types from c_cast
    # instead of defaulting to void
    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_private_static_function(text: str):
        """Inserts private static function"""
        result = "static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_insert_library(text: str, selection: str):
        actions.user.paste(f"#include <{text}>")
