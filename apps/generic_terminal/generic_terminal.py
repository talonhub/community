from talon import app, Module, Context, actions, ui, imgui, settings, app, registry

mod = Module()
mod.tag("generic_terminal", desc="Tag for enabling generic terminal commands")


@mod.action_class
class Actions:
    def terminal_list_directories():
        """Lists directories"""

    def terminal_list_all_directories():
        """Lists all directories including hidden"""

    def terminal_change_directory(path: str):
        """Lists change directory"""

    def terminal_change_directory_root():
        """Root of current drive"""

    def terminal_clear_screen():
        """Clear screen"""

    def terminal_run_last():
        """Repeats the last command"""

    def terminal_kill_all():
        """kills the running command"""

