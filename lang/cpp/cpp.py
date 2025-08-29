from talon import Context, Module

from ..c.c import operators
from ..tags.operators import Operators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: cpp
"""


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

mod.list("cpp_standard_type", desc="Types from the cplusplus standard library")
mod.list("cpp_standard_prefix", desc="Prefixes for referring to the standard library")