from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_operators_collection", desc="Tag for enabling collection operator commands")

@mod.action_class
class Actions:

    def code_operator_in():
        """code_operator_in (e.g. Python in)"""
