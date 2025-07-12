"""
This module gives us the list {user.system_paths} and the capture <user.system_path> that wraps
the list to easily refer to system paths in talon and python files. It also creates a file
system_paths-<hostname>.talon-list in the core folder so the user can easily add their own
custom paths.
"""

from pathlib import Path

from talon import Module, actions, app

mod = Module()
mod.list("system_paths", desc="List of system paths")


def on_ready():
    # If user.system_paths defined otherwise, don't generate a file
    if actions.user.talon_get_active_registry_list("user.system_paths"):
        return

    hostname = actions.user.talon_get_hostname()
    system_paths = Path(__file__).with_name(f"system_paths-{hostname}.talon-list")
    if system_paths.is_file():
        return

    home = Path.home()
    talon_home = Path(actions.path.talon_home())

    default_system_paths = {
        "user": home,
        "desktop": home / "Desktop",
        "desk": home / "Desktop",
        "documents": home / "Documents",
        "docks": home / "Documents",
        "downloads": home / "Downloads",
        "music": home / "Music",
        "pictures": home / "Pictures",
        "videos": home / "Videos",
        "talon home": talon_home,
        "talon recordings": talon_home / "recordings",
        "talon user": actions.path.talon_user(),
    }

    if app.platform == "windows":
        default_system_paths["profile"] = home
        onedrive_path = home / "OneDrive"

        # this is probably not the correct way to check for OneDrive, quick and dirty
        if (onedrive_path / "Desktop").is_dir():
            default_system_paths["desktop"] = onedrive_path / "Desktop"
            default_system_paths["documents"] = onedrive_path / "Documents"
            default_system_paths["one drive"] = onedrive_path
            default_system_paths["pictures"] = onedrive_path / "Pictures"
    else:
        default_system_paths["home"] = home

    with open(system_paths, "x") as f:
        print("list: user.system_paths", file=f)
        print(f"hostname: {hostname}", file=f)
        print("-", file=f)
        for spoken_form, path in default_system_paths.items():
            path = str(path)
            if not str.isprintable(path) or "'" in path or '"' in path:
                path = repr(path)

            print(f"{spoken_form}: {path}", file=f)


@mod.capture(rule="{user.system_paths}")
def system_path(m) -> str:
    return m.system_paths


app.register("ready", on_ready)
