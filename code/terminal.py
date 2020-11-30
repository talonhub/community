from talon import app, Module, Context, actions, ui, imgui, settings, app, registry

mod = Module()
mod.tag("generic_terminal", desc="Tag for enabling generic terminal commands")


@mod.action_class
class Actions:
    def terminal_list_directories():
        """Lists directories"""

    def terminal_change_directory(path: str):
        """Lists change directory"""

    def terminal_change_directory_root():
        """Root of current drive"""

    def terminal_clear_screen():
        """Clear screen"""

