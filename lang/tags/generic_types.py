# This functionality is unstable and subject to change
# we want to implement generic type support for several languages before finalizing the general abstraction

from talon import Module
from enum import Enum, auto
from contextlib import suppress
from typing import Union

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

@mod.capture
def generic_type_parameter_argument(m) -> str:
	"""A type parameter for a generic data structure"""
	pass

@mod.capture(
    rule="<user.generic_type_connector> <user.generic_type_parameter_argument> [<user.generic_type_connector_done>]+"
)
def generic_type_continuation(m) -> list[Union[GenericTypeConnector, str]]:
    """A generic type parameter that goes after the first using connectors"""
    result = [m.generic_type_connector, m.generic_type_parameter_argument]
    with suppress(AttributeError):
        dones = m.generic_type_connector_done_list
        result.extend(dones)
    return result

@mod.capture(rule="<user.generic_type_continuation>+")
def generic_type_additional_type_parameters(
    m,
) -> list[Union[GenericTypeConnector, str]]:
    """Type parameters for a generic data structure after the first one"""
    result = []
    for continuation in m.generic_type_continuation_list:
        result.extend(continuation)
    return result