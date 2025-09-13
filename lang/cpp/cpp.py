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
mod.list("cpp_standard_function", desc="Functions in the std namespace")
mod.list("cpp_standard_constant", desc="Constants in the std namespace")
mod.list("cpp_standard_prefix", desc="Prefixes for referring to the standard library")
mod.list("cpp_standard_header", desc="Header files of the C++ standard library")
mod.list("cpp_namespace", desc="Spoken forms for C++ namespaces")


@mod.capture(rule="{user.cpp_standard_prefix} {user.cpp_standard_type}")
def cpp_standard_type(m) -> str:
    """Discard the prefix word and properly prefix the type"""
    return "std::" + m[1]


@mod.capture(rule="{user.cpp_standard_prefix} {user.cpp_standard_function}")
def cpp_standard_function(m) -> str:
    """Discard the prefix word and insert properly prefixed function call"""
    return "std::" + m[1]


@mod.capture(rule="{user.cpp_standard_prefix} {user.cpp_standard_constant}")
def cpp_standard_constant(m) -> str:
    """Discard the prefix word and insert properly prefixed standard constant"""
    return "std::" + m[1]


@mod.capture(rule="{user.cpp_namespace}+")
def cpp_namespace_list(m) -> str:
    """List of namespaces followed by colons"""
    return "::".join(m) + "::"


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_insert_null():
        actions.auto_insert("nullptr")

    def code_insert_is_null():
        actions.auto_insert(" == nullptr")

    def code_insert_is_not_null():
        actions.auto_insert(" != nullptr")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_operator_object_accessor():
        actions.insert(".")

    def code_self():
        actions.insert("this")

    def code_self_accessor():
        actions.insert("this->")

    def code_insert_function(text: str, selection: str):
        substitutions = {"1": text}
        if selection:
            substitutions["0"] = selection
        actions.user.insert_snippet_by_name("functionCall", substitutions)


@mod.capture(
    rule="([<user.c_signed>] <user.c_types>) | <user.c_fixed_integer> | <user.cpp_standard_type>"
)
def code_type_raw(m) -> str:
    return " ".join(list(m))


@mod.capture(rule="<user.code_type_raw> [{user.cpp_pointers}+] <user.text>")
def variable_declaration(m) -> str:
    suffix = ""
    with suppress(AttributeError):
        suffix = "".join(m.cpp_pointers_list)
    return (
        m.code_type_raw
        + " "
        + suffix
        + actions.user.formatted_text(m.text, "SNAKE_CASE")
    )


@ctx.capture("user.code_type", rule="<user.code_type_raw> [{user.cpp_pointers}+]")
def code_type(m):
    """Returns a type with pointer or reference annotations"""
    suffix = ""
    with suppress(AttributeError):
        suffix = "".join(m.cpp_pointers_list)
    return m.code_type_raw + suffix
