# This functionality is unstable and subject to change
# we want to implement generic type support for several languages before finalizing the general abstraction

from contextlib import suppress
from dataclasses import dataclass
from enum import Enum, auto
from typing import Union

from talon import Module


class CommonTypeConnector(Enum):
    """A common type connector for connecting type arguments for a generic type"""

    AND = auto()
    OF = auto()
    DONE = auto()


@dataclass(slots=True)
class SimpleLanguageSpecificTypeConnector:
    """A type connector that only requires inserting text with no other complexity,
    e.g. Python's `|` for union types
    """

    text: str


TypeConnector = Union[CommonTypeConnector, SimpleLanguageSpecificTypeConnector]

mod = Module()

# implement the following for a specific language


@mod.capture
def generic_type_parameter_argument(m) -> str:
    """A type parameter for a generic data structure. This should include standard types of a language and appropriate formatting of arbitrary text for user types"""
    pass


@mod.capture
def generic_data_structure(m) -> str:
    """A generic data structure that takes type parameter arguments"""
    pass


@mod.capture(
    rule="<user.generic_type_parameter_argument> [<user.generic_type_additional_type_parameters>]"
)
def generic_type_parameter_arguments(m) -> str:
    """This combines type parameter arguments, connectors,  and the containing type into a formatted string. This is usually formatted using format_type_parameter_arguments"""
    pass


# end of language specific section


@mod.capture(rule="done")
def generic_type_connector_done(m) -> CommonTypeConnector:
    """Denotes ending a nested generic type"""
    return CommonTypeConnector.DONE


@mod.capture(rule="and|of|<user.generic_type_connector_done>")
def common_generic_type_connector(m) -> CommonTypeConnector:
    """A common type connector for generic types"""
    with suppress(AttributeError):
        return m.generic_type_connector_done
    return CommonTypeConnector[m[0].upper()]


@mod.capture(rule="<user.common_generic_type_connector>")
def generic_type_connector(m) -> TypeConnector:
    """A generic type connector for determining how to put type parameters together.
    Override on a per language basis to add additional connectors.
    """
    return m.common_generic_type_connector


@mod.capture(
    rule="<user.generic_type_connector> <user.generic_type_parameter_argument> [<user.generic_type_connector_done>]+"
)
def generic_type_continuation(m) -> list[Union[TypeConnector, str]]:
    """A generic type parameter that goes after the first using connectors"""
    result = [m.generic_type_connector, m.generic_type_parameter_argument]
    with suppress(AttributeError):
        dones = m.generic_type_connector_done_list
        result.extend(dones)
    return result


@mod.capture(rule="<user.generic_type_continuation>+")
def generic_type_additional_type_parameters(
    m,
) -> list[Union[TypeConnector, str]]:
    """Type parameters for a generic data structure after the first one"""
    result = []
    for continuation in m.generic_type_continuation_list:
        result.extend(continuation)
    return result


def format_type_parameter_arguments(
    m,
    argument_separator: str,
    generic_parameters_start: str,
    generic_parameters_end: str,
) -> str:
    """Formats type parameter arguments for languages with simple generic typing"""
    parameters = [m.generic_type_parameter_argument]
    with suppress(AttributeError):
        parameters.extend(m.generic_type_additional_type_parameters)
    pieces = []
    nesting: int = 0
    is_immediately_after_nesting_exit = False
    for parameter in parameters:
        match parameter:
            case CommonTypeConnector.AND:
                pieces.append(argument_separator)
            case CommonTypeConnector.OF:
                pieces.append(generic_parameters_start)
                nesting += 1
            case CommonTypeConnector.DONE:
                pieces.append(generic_parameters_end)
                nesting -= 1
            case SimpleLanguageSpecificTypeConnector():
                pieces.append(parameter.text)
            case str():
                if is_immediately_after_nesting_exit:
                    pieces.append(argument_separator)
                pieces.append(parameter)
        is_immediately_after_nesting_exit = parameter == CommonTypeConnector.DONE
    if nesting > 0:
        pieces.append(generic_parameters_end * nesting)
    return "".join(pieces)
