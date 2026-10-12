from talon import Context, Module, actions, settings

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators

mod = Module()

@mod.action_class
class Actions:
    def code_state_protocol():
        """Inserts a protocol block, and positions the cursor accordingly"""

    def code_state_extension():    
        """Inserts a type extension block, and positions the cursor accordingly"""
    
    def code_state_actor():
        """Inserts an actor block, and positions the cursor accordingly"""

    def code_state_repeat_while():
        """Inserts a repeat while loop, the Swift equivalent of a do while loop, and positions the cursor accordingly"""


ctx = Context()
ctx.matches = r"""
code.language: swift
"""

number_types = {
    "int": "Int",
    "int eight": "Int8",
    "int sixteen": "Int16",
    "int thirty two": "Int32",
    "int sixty four": "Int64",
    "int one twenty eight": "Int128",
    "int one hundred and twenty eight": "Int128",
    "you int": "Int8",
    "you int eight": "UInt8",
    "you int sixteen": "UInt16",
    "you int thirty two": "UInt32",
    "you int sixty four": "UInt64",
    "you int one twenty eight": "UInt128",
    "you int one hundred and twenty eight": "UInt128",
    "float": "Float",
    "double": "Double",
    "float sixteen": "Float16",
    "float eighty": "Float80",
    "float thirty two": "Float32",
    "float sixty four": "Float64",
}

other_common_types = {
    "array": "[]",
    "tuple": "()",
    "bool": "Bool",
    "boolean": "Bool",
    "string": "String",
    "char": "Character",
    "character": "Character",
}

standard_dictionary_types = {
    **number_types,
    **other_common_types,
}

# tag: functions
ctx.lists["user.code_type"] = standard_dictionary_types