from typing import Optional

from talon import Context, Module, actions

mod = Module()

ctx = Context()
ctx.matches = "tag: terminal"


@mod.action_class
class Actions:
    def terminal_list_directories(path: Optional[str] = None):
        """Lists directories"""

    def terminal_list_all_directories():
        """Lists all directories including hidden"""

    def terminal_change_directory(path: str):
        """Changes current directory"""

    def terminal_change_directory_root():
        """Root of current drive"""

    def terminal_clear_screen():
        """Clear screen"""

    def terminal_run_last():
        """Repeats the last command"""

    def terminal_rerun_search(command: str):
        """Searches through the previously executed commands"""

    def terminal_kill_all():
        """kills the running command"""

    def terminal_escape_string(string: str) -> str:
        """Escapes a string for a given terminal"""
        return f'"{string}"'

    def terminal_escape_relative_file(string: str) -> str:
        """Escapes a string for a given terminal"""
        return actions.user.terminal_escape_string(f"./{string}")

    def terminal_escape_relative_directory(string: str) -> str:
        """Escapes a string for a given terminal"""
        return actions.user.terminal_escape_string(f"{string}/")


@ctx.action_class("user")
class TerminalActions:
    # user.file_manager
    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.user.terminal_change_directory(
            actions.user.terminal_escape_relative_directory(path)
        )

    def file_manager_open_parent():
        actions.user.file_manager_open_directory("..")

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(actions.user.terminal_escape_relative_directory(path))

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.insert(actions.user.terminal_escape_relative_file(path))
        actions.key("enter")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.insert(actions.user.terminal_escape_relative_file(path))

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.insert(f'mkdir "{name}"')
