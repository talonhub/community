import os
from typing import Optional

from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
app: windows_command_processor
app: windows_terminal
and win.title: /Command Prompt/
"""

directories_to_remap = {}
directories_to_exclude = {}

ctx.tags = ["user.file_manager", "user.git", "user.kubectl", "terminal"]


@ctx.action_class("edit")
class EditActions:
    def delete_line():
        actions.key("esc")


@ctx.action_class("user")
class UserActions:
    def file_manager_refresh_title():
        actions.insert("title Command Prompt: %CD%")
        actions.key("enter")

    def file_manager_current_path():
        path = ui.active_window().title
        path = path.replace("Administrator:  ", "").replace("Command Prompt: ", "")
        if path in directories_to_remap:
            path = directories_to_remap[path]

        if path in directories_to_exclude:
            path = ""
        return path

    def terminal_escape_relative_file(string: str) -> str:
        return f'"{string}"'

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.insert(f'cd "{path}"')
        actions.key("enter")
        actions.user.file_manager_refresh_title()

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""
        actions.insert(volume)
        actions.key("enter")
        actions.user.file_manager_refresh_title()

    def terminal_list_directories(path: Optional[str] = None):
        """Lists directories"""
        actions.insert(f"dir {path or ''}")
        actions.key("enter")

    def terminal_list_all_directories():
        actions.insert("dir /a")
        actions.key("enter")

    def terminal_change_directory(path: str):
        actions.insert(f"cd {path}")
        if path:
            actions.key("enter")

    def terminal_change_directory_root():
        """Root of current drive"""
        actions.insert("cd /")
        actions.key("enter")

    def terminal_clear_screen():
        """Clear screen"""
        actions.insert("cls")
        actions.key("enter")

    def terminal_run_last():
        actions.key("up enter")

    def terminal_kill_all():
        actions.key("ctrl-c")
        actions.insert("y")
        actions.key("enter")

    def terminal_escape_string(string: str) -> str:
        return string.replace(" ", r"\ ")
