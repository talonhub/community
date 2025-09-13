from talon import Context, Module, actions

from ..c.c import operators
from ..tags.operators import Operators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: cpp
"""

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


@ctx.capture("user.code_type", rule="<user.c_types> | <user.cpp_standard_type>")
def code_type(m):
    return m[0]
