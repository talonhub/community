from talon import Context, Module

from ..c.c import operators
from ..tags.operators import Operators

ctx = Context()

ctx.matches = r"""
code.language: cpp
"""


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators
