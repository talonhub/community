from typing import Optional

from talon import Module, Context, actions

mod = Module()

ctx = Context()


@mod.action_class
class Actions:
    def terminal_list_directories(path: Optional[str] = None):
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

    def terminal_rerun_search(command: str):
        """Searches through the previously executed commands"""

    def terminal_kill_all():
        """kills the running command"""


@ctx.action_class("user")
class TerminalActions:

    # def file_manager_current_path():
    #     pass

    # def file_manager_show_properties():
    #     """Shows the properties for the file"""

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.terminal_change_directory(path)

    def file_manager_open_parent():
        actions.terminal_change_directory("..")

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(path + "/")

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.insert(path)

    # def file_manager_refresh_title():
    #     return
