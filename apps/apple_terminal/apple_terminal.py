import os

from talon import Context, actions, ui

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


@ctx.action_class("app")
class app_actions:
    # other tab functions should already be implemented in
    # code/platforms/mac/app.py

    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_next():
        actions.key("ctrl-tab")
