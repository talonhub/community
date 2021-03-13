"""
Stores terms that are used in many different places
"""
from talon import Module

mod = Module()

SELECT = "take"
TELEPORT = "hop"
OPERATOR = "do"


@mod.capture(rule=SELECT)
def select(m) -> str:
    """Term for select"""
    return str(m)


@mod.capture(rule=TELEPORT)
def teleport(m) -> str:
    """Verb to use for commands that teleport the cursor to another place"""
    return str(m)


@mod.capture(rule=OPERATOR)
def operator(m) -> str:
    """Prefix for operators"""
    return str(m)