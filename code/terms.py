"""
Stores terms that are used in many different places
"""
from talon import Module

mod = Module()


@mod.capture(rule="take")
def select(m) -> str:
    """Term for select"""
    return str(m)


@mod.capture(rule="hop")
def teleport(m) -> str:
    """Verb to use for commands that teleport the cursor to another place"""
    return str(m)