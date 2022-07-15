import os

from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
app: windows_command_processor
app: windows_terminal
and win.title: /Command Prompt/
"""

user_path = os.path.expanduser("~")
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
        # action(user.file_manager_go_back):
        #    key("alt-left")
        # action(user.file_manager_go_forward):
        #    key("alt-right")

    def file_manager_open_parent():
        actions.insert("cd ..")
        actions.key("enter")
        actions.user.file_manager_refresh_title()

    def file_manager_current_path():
        path = ui.active_window().title
        path = path.replace("Administrator:  ", "").replace("Command Prompt: ", "")
        if path in directories_to_remap:
            path = directories_to_remap[path]

        if path in directories_to_exclude:
            path = ""
        return path

    # def file_manager_terminal_here():
    #     actions.key("ctrl-l")
    #     actions.insert("cmd.exe")
    #     actions.key("enter")

    # def file_manager_show_properties():
    #     """Shows the properties for the file"""
    #     actions.key("alt-enter")

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.insert(f'cd "{path}"')
        actions.key("enter")
        actions.user.file_manager_refresh_title()

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(f'"{path}"')

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.insert(f'mkdir "{name}"')

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.insert(path)
        # actions.key("enter")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.insert(path)

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""
        actions.user.file_manager_open_directory(volume)

    def terminal_list_directories():
        """Lists directories"""
        actions.insert("dir")
        actions.key("enter")

    def terminal_list_all_directories():
        actions.insert("dir /a")
        actions.key("enter")

    def terminal_change_directory(path: str):
        actions.insert(f"cd {path}")
        # if path:
        # actions.key("enter")

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
