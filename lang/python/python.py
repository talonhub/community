import re

from talon import Context, Module, actions, settings

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators
from ..tags.generic_types import format_type_parameter_arguments
from contextlib import suppress

mod = Module()
ctx = Context()
ctx.matches = r"""
code.language: python
"""

"""a set of fields used in python docstrings that will follow the
reStructuredText format"""
docstring_fields = {
    "class": ":class:",
    "function": ":func:",
    "parameter": ":param:",
    "raise": ":raise:",
    "returns": ":return:",
    "type": ":type:",
    "return type": ":rtype:",
    # these are sphinx-specific
    "see also": ".. seealso:: ",
    "notes": ".. notes:: ",
    "warning": ".. warning:: ",
    "todo": ".. todo:: ",
}

mod.list("python_docstring_fields", desc="python docstring fields")
ctx.lists["user.python_docstring_fields"] = docstring_fields

exception_list = [
    "BaseException",
    "SystemExit",
    "KeyboardInterrupt",
    "GeneratorExit",
    "Exception",
    "StopIteration",
    "StopAsyncIteration",
    "ArithmeticError",
    "FloatingPointError",
    "OverflowError",
    "ZeroDivisionError",
    "AssertionError",
    "AttributeError",
    "BufferError",
    "EOFError",
    "ImportError",
    "ModuleNotFoundError",
    "LookupError",
    "IndexError",
    "KeyError",
    "MemoryError",
    "NameError",
    "UnboundLocalError",
    "OSError",
    "BlockingIOError",
    "ChildProcessError",
    "ConnectionError",
    "BrokenPipeError",
    "ConnectionAbortedError",
    "ConnectionRefusedError",
    "ConnectionResetError",
    "FileExistsError",
    "FileNotFoundError",
    "InterruptedError",
    "IsADirectoryError",
    "NotADirectoryError",
    "PermissionError",
    "ProcessLookupError",
    "TimeoutError",
    "ReferenceError",
    "RuntimeError",
    "NotImplementedError",
    "RecursionError",
    "SyntaxError",
    "IndentationError",
    "TabError",
    "SystemError",
    "TypeError",
    "ValueError",
    "UnicodeError",
    "UnicodeDecodeError",
    "UnicodeEncodeError",
    "UnicodeTranslateError",
    "Warning",
    "DeprecationWarning",
    "PendingDeprecationWarning",
    "RuntimeWarning",
    "SyntaxWarning",
    "UserWarning",
    "FutureWarning",
    "ImportWarning",
    "UnicodeWarning",
    "BytesWarning",
    "ResourceWarning",
]
mod.list("python_exception", desc="python exceptions")
ctx.lists["user.python_exception"] = {
    " ".join(re.findall("[A-Z][^A-Z]*", exception)).lower(): exception
    for exception in exception_list
}

# This is not part of the long term stable API
# After we implement generics support for several languages,
# we plan on abstracting out from the specific implementations into a general grammar

mod.list("python_generic_type", desc="A python type that takes type parameter arguments")

# this should be moved to a talon-list file after this becomes stable
ctx.lists["user.python_generic_type"] = {
    "callable": "Callable",
    "dictionary": "dict",
    "iterable": "Iterable",
    "list": "list",
    "optional": "Optional",
    "set": "set",
    "tuple": "tuple",
    "union": "Union",
}

@ctx.capture("user.generic_type_parameter_argument", rule="<user.code_type> | <user.text>")
def generic_type_parameter_argument(m) -> str:
    """A Python type parameter for a generic data structure"""
    with suppress(AttributeError):
        return m.code_type
    return actions.user.formatted_text(m.text, "PUBLIC_CAMEL_CASE")

@ctx.capture("user.generic_data_structure", rule="{user.python_generic_type} | type <user.text>")
def generic_data_structure(m) -> str:
    """A Python generic data structure that takes type parameter arguments"""
    with suppress(AttributeError):
        return m.python_generic_type
    return actions.user.formatted_text(m.text, "PUBLIC_CAMEL_CASE")

@ctx.capture(
    "user.generic_type_parameter_arguments",
    rule="<user.generic_type_parameter_argument> [<user.generic_type_additional_type_parameters>]"
)
def generic_type_parameter_arguments(m) -> str:
    return format_type_parameter_arguments(
        m,
        ", ",
        "[",
        "]"
    )

@mod.capture(
    rule="<user.generic_data_structure> of <user.generic_type_parameter_arguments>"
)
def python_generic_type(m) -> str:
    """A generic type with specific type parameters"""
    parameters = m.generic_type_parameter_arguments
    return f"{m.generic_data_structure}[{parameters}]"

# End of unstable section

operators = Operators(
    # code_operators_array
    SUBSCRIPT=create_described_insert_between("[", "]"),
    # code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_DIVISION=" /= ",
    ASSIGNMENT_MODULO=" %= ",
    ASSIGNMENT_INCREMENT=" += 1",
    ASSIGNMENT_BITWISE_AND=" &= ",
    ASSIGNMENT_BITWISE_OR=" |= ",
    ASSIGNMENT_BITWISE_EXCLUSIVE_OR=" ^= ",
    ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    # code_operators_bitwise
    BITWISE_NOT="~",
    BITWISE_AND=" & ",
    BITWISE_OR=" | ",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    BITWISE_RIGHT_SHIFT=" >> ",
    # code_operators_lambda
    LAMBDA=create_described_insert_between("lambda ", ": "),
    # code_operators_math
    MATH_SUBTRACT=" - ",
    MATH_ADD=" + ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_INTEGER_DIVIDE=" // ",
    MATH_MODULO=" % ",
    MATH_EXPONENT=" ** ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" and ",
    MATH_OR=" or ",
    MATH_NOT=" not ",
    MATH_IN=" in ",
    MATH_NOT_IN=" not in ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_self():
        actions.auto_insert("self")

    def code_operator_object_accessor():
        actions.auto_insert(".")

    def code_insert_null():
        actions.auto_insert("None")

    def code_insert_is_null():
        actions.auto_insert(" is None")

    def code_insert_is_not_null():
        actions.auto_insert(" is not None")

    def code_insert_true():
        actions.auto_insert("True")

    def code_insert_false():
        actions.auto_insert("False")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_default_function(text: str):
        actions.user.code_public_function(text)

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "def _{}():".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.paste(result)
        actions.edit.left()
        actions.edit.left()

    def code_public_function(text: str):
        result = "def {}():".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.edit.left()
        actions.edit.left()

    def code_insert_type_annotation(type: str):
        actions.insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.insert(f" -> {type}")
