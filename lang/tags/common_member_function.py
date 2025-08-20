from talon import actions, Module, Context

ctx = Context()
mod = Module()

mod.tag("code_common_member_function", desc="Tag for activating common member function insertion")
mod.list("code_common_member_function", desc="Function to use in a dotted chain, eg .foo()")

@mod.action_class
class Actions:
	def code_member_function(name: str):
		"""Inserts a member function call"""
		actions.user.insert_between(f".{name}(", ")")
