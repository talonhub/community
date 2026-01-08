from talon import Module
from enum import Enum, auto
from contextlib import suppress

class GenericTypeConnector(Enum):
    AND = auto()
    OF = auto()
    DONE = auto()

mod = Module()

@mod.capture(rule="done")
def generic_type_connector_done(m) -> GenericTypeConnector:
	"""Denotes ending a nested generic type"""
	return GenericTypeConnector.DONE

@mod.capture(rule="and|of|<user.generic_type_connector_done>")
def generic_type_connector(m) -> GenericTypeConnector:
    """Determines how to put generic type parameters together"""
    with suppress(AttributeError):
        return m.generic_type_connector_done
    return GenericTypeConnector[m[0].upper()]
