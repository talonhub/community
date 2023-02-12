from talon import Module

mod = Module()


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

    def terminal_change_directory_up(count: int):
        """Traverse a given number of directories upwards"""

    def terminal_change_directory_back():
        """Traverse back to the previous directory on the directory stack"""

    def terminal_change_directory_toggle():
        """Toggle traversal between the two most recent directories"""

    def terminal_clear_screen():
        """Clear screen"""

    def terminal_run_last():
        """Repeats the last command"""

    def terminal_rerun_search(command: str):
        """Searches through the previously executed commands"""

    def terminal_kill_all():
        """kills the running command"""
