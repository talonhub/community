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

