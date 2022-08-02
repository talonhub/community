import os

from talon import Context, actions, ui

# TODO: fit this to generic_terminal

ctx = Context()
ctx.matches = r"""
app: apple_terminal
"""
directories_to_remap = {}
directories_to_exclude = {}


@ctx.action_class("edit")
class EditActions:
    def delete_line():
        actions.key("ctrl-u")


@ctx.action_class("user")
class UserActions:
    def file_manager_current_path():
        title = ui.active_window().title

        # take the first split for the zsh-based terminal
        if " — " in title:
            title = title.split(" — ")[0]

        if "~" in title:
            title = os.path.expanduser(title)

        if title in directories_to_remap:
            title = directories_to_remap[title]

        if title in directories_to_exclude:
            title = None

        return title

    def file_manager_show_properties():
        """Shows the properties for the file"""

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.insert("cd ")
        path = f'"{path}"'
        actions.insert(path)
        actions.key("enter")

        # jtk - refresh title isn't necessary since the apple terminal does it for us
        # actions.user.file_manager_refresh_title()

    def file_manager_open_parent():
        actions.insert("cd ..")
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

    def file_manager_refresh_title():
        return


@ctx.action_class("app")
class app_actions:
    # other tab functions should already be implemented in
    # code/platforms/mac/app.py

    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_next():
        actions.key("ctrl-tab")
