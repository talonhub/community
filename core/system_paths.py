"""
This module gives us the list {user.system_paths} and the capture <user.system_path> that wraps
the list to easily refer to system paths in talon and python files.
"""

import os

from talon import Context, Module, actions, app

mod = Module()
ctx = Context()

mod.list("system_paths", desc="List of system paths")

user_path = os.path.expanduser("~")


# We need to wait for ready before we can call "actions.path.talon_home()" and
# "actions.path.talon_user()"
def on_ready():
    default_system_paths = {
        "user": user_path,
        "profile": user_path,
        "desktop": os.path.join(user_path, "Desktop"),
        "desk": os.path.join(user_path, "Desktop"),
        "documents": os.path.join(user_path, "Documents"),
        "docks": os.path.join(user_path, "Documents"),
        "downloads": os.path.join(user_path, "Downloads"),
        "music": os.path.join(user_path, "Music"),
        "pictures": os.path.join(user_path, "Pictures"),
        "videos": os.path.join(user_path, "Videos"),
        "talon home": str(actions.path.talon_home()),
        "talon user": str(actions.path.talon_user()),
    }

    if app.platform == "windows":
        one_drive_path = os.path.expanduser(os.path.join("~", "OneDrive"))

        # this is probably not the correct way to check for onedrive, quick and dirty
        if os.path.isdir(os.path.expanduser(os.path.join("~", r"OneDrive\Desktop"))):
            onedrive_paths = {
                "desktop": os.path.join(one_drive_path, "Desktop"),
                "documents": os.path.join(one_drive_path, "Documents"),
                "one drive": one_drive_path,
                "pictures": os.path.join(one_drive_path, "Pictures"),
            }

            default_system_paths.update(onedrive_paths)

    ctx.lists["user.system_paths"] = default_system_paths


@mod.capture(rule="{user.system_paths}")
def system_path(m) -> str:
    return m.system_paths


app.register("ready", on_ready)
