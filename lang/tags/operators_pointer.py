from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def code_operator_indirection():
        """code_operator_indirection"""

    def code_operator_address_of():
        """code_operator_address_of (e.g., C++ & op)"""

    def code_operator_structure_dereference():
        """code_operator_structure_dereference (e.g., C++ -> op)"""
