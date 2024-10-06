from talon import Module

mod = Module()
mod.tag(
    "command_search",
    desc="A command for running an arbitrary command based on a search",
)


@mod.action_class
class command_search_actions:
    def command_search(command: str = ""):
        """Searches for command based on text"""
