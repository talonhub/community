from talon import Context, Module

ctx = Context()
mod = Module()

# TODO: rename this tag to 'code_operators_pointer' for consistency?
mod.tag("code_operators_pointer", desc="Tag for enabling pointer operator commands")

@mod.action_class
class Actions:

    def code_operator_indirection():
        """code_operator_indirection"""

    def code_operator_address_of():
        """code_operator_address_of (e.g., C++ & op)"""

    def code_operator_structure_dereference():
        """code_operator_structure_dereference (e.g., C++ -> op)"""
