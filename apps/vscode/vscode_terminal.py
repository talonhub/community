from talon import Context, Module, actions, app

is_mac = app.platform == "mac"

ctx = Context()
mod = Module()

mod.apps.vscode_terminal = r"""
app: vscode
win.title: /focus:\[Terminal\]/
"""

ctx.matches = r"""
app: vscode_terminal
"""

@ctx.action_class("user")
class UserActions:
    def file_manager_open_parent():
        actions.insert("cd ..")
        actions.key("enter")

    def file_manager_current_path():
        actions.skip()

    def file_manager_show_properties():
        """Shows the properties for the file"""

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.insert("cd ")
        path = f'"{path}"'
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(path)

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        name = f'"{name}"'

        actions.insert("mkdir " + name)

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.insert(path)

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""
        actions.user.file_manager_open_directory(volume)