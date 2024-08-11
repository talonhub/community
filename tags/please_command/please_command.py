from talon import Module

mod = Module()
mod.tag(
    "please_command",
    desc="A command for running an arbitrary command based on a search",
)


@mod.action_class
class please_command_actions:
    def please_command(command: str):
        """Searches for command based on text"""
