# This file provides support for defining functions that have an associated description
# The talon version of python does not have adequate inspection support to get the doc string of a function, so this serves as an alternative

from talon import Module, actions
from typing import Callable

class DescribedFunction:
	def __init__(self, function, description: str):
		self.function = function
		self.description = description

	def __call__(self, *args, **kwargs):
		return self.function(*args, **kwargs)

	def __repr__(self):
		return self.description

mod = Module()
@mod.action_class
class Actions:
	def described_function_create(function: Callable, description: str):
		"""Create a function with an associated description"""
		return DescribedFunction(function, description)

	def described_function_create_insert_between(before: str, after: str) -> DescribedFunction:
		"""Creates a described function for calling actions.user.insert_between"""
		return DescribedFunction(lambda: actions.user.insert_between(before, after), f"actions.user.insert_between('{before}', '{after}')")