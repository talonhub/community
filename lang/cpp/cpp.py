from contextlib import suppress
from talon import Context, Module, actions

from ..c.c import operators
from ..tags.operators import Operators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: cpp
"""

ctx.lists["self.cpp_pointers"] = {
    "pointer": "*",
    "reference": "&",
    "ref": "&",
    "array": "[]",
}

mod.list("cpp_pointers", desc="C++ pointer and reference annotations")
mod.list("cpp_standard_type", desc="Types from the C++ standard library")
mod.list("cpp_standard_prefix", desc="Prefixes for referring to the standard library")


@mod.capture(rule="{user.cpp_standard_prefix} {user.cpp_standard_type}")
def cpp_standard_type(m) -> str:
    # Discard the prefix word and properly prefix the type
    return "std::" + m[1]


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

@mod.capture(rule="([<user.c_signed>] <user.c_types>) | <user.c_fixed_integer> | <user.cpp_standard_type>")
def code_type_raw(m) -> str:
    return " ".join(list(m))

@mod.capture(rule="<user.code_type_raw> [{user.cpp_pointers}+] <user.text>")
def variable_declaration(m) -> str:
    suffix = ""
    with suppress(AttributeError):
        suffix = "".join(m.cpp_pointers_list)
    return m.code_type_raw+" "+suffix+actions.user.formatted_text(m.text, "SNAKE_CASE")
 

@ctx.capture("user.code_type", rule="<user.code_type_raw> [{user.cpp_pointers}+]")
def code_type(m):
    """Returns a type with pointer or reference annotations"""
    suffix = ""
    with suppress(AttributeError):
        suffix = "".join(m.cpp_pointers_list)
    return m.code_type_raw+suffix
