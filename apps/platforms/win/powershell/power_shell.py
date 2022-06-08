from talon import Context, Module, actions, ui

ctx = Context()
mod = Module()
ctx.matches = r"""
app: windows_power_shell
app: windows_terminal
and win.title: /PowerShell/
"""

directories_to_remap = {}
directories_to_exclude = {}


@ctx.action_class("edit")
class EditActions:
    def delete_line():
        actions.key("esc")


@ctx.action_class("user")
class UserActions:
    def file_manager_refresh_title():
        actions.insert(
            "$Host.UI.RawUI.WindowTitle = 'Windows PowerShell: ' +  $(get-location)"
        )
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
        path = path.replace("Administrator:  ", "").replace("Windows PowerShell: ", "")

        if path in directories_to_remap:
            path = directories_to_remap[path]

        if path in directories_to_exclude:
            path = ""
        return path

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
