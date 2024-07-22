from talon import Module

mod = Module()
mod.tag("find", desc="Tag for enabling generic find commands")


@mod.action_class
class Actions:
    def find(text: str):
        """Finds text in current editor"""

    def find_next():
        """Navigates to the next occurrence"""

    def find_previous():
        """Navigates to the previous occurrence"""
