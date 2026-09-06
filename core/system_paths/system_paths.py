"""
This module gives us the list {user.system_paths} and the capture <user.system_path> that wraps
the list to easily refer to system paths in Talon and Python files. It also creates a file
system_paths-<hostname>.talon-list in the core/system_paths folder, so the user can easily add
their own custom paths. The additional capture <user.possibly_virtual_system_path> represents a
combination of the lists {user.system_path} and {user.virtual_system_path}.
"""

import os.path
from pathlib import Path

from talon import Module, actions, app

mod = Module()
mod.list("system_paths", desc="List of system paths")
mod.list("virtual_system_path", desc="Path of virtual system folder like Recycle Bin")


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
        "talon home": talon_home,
        "talon recordings": talon_home / "recordings",
        "talon user": actions.path.talon_user(),
    }

    if app.platform == "windows":
        import winreg

        # Resolved forms of virtual folders whose locations the user may have changed.
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        ) as key:

            def get_path(value_name, fallback):
                try:
                    path, value_type = winreg.QueryValueEx(key, value_name)
                    assert value_type == winreg.REG_EXPAND_SZ
                except (FileNotFoundError, AssertionError):
                    path = fallback
                return Path(os.path.expandvars(path))

            local_downloads_path = get_path(
                "{7D83EE9B-2244-4E70-B1F5-5393042AF1E4}", r"%USERPROFILE%\Downloads"
            )

            default_system_paths.update(
                {
                    "desktop": get_path("Desktop", r"%USERPROFILE%\Desktop"),
                    "documents": get_path("Personal", r"%USERPROFILE%\Documents"),
                    "downloads": get_path(
                        "{374DE290-123F-4565-9164-39C4925E467B}", local_downloads_path
                    ),
                    "local downloads": local_downloads_path,
                    "music": get_path("My Music", r"%USERPROFILE%\Music"),
                    "pictures": get_path("My Pictures", r"%USERPROFILE%\Pictures"),
                    "videos": get_path("My Video", r"%USERPROFILE%\Videos"),
                }
            )

        # Paths from environment variables.
        def get_env_path(var_name):
            try:
                return Path(os.environ[var_name])
            except KeyError:
                return None

        onedrive_path = get_env_path("OneDrive")

        default_system_paths.update(
            {
                spoken_form: path
                for spoken_form, path in {
                    "system root": get_env_path("SystemRoot"),
                    "program files": get_env_path("ProgramFiles"),
                    "program files ex eighty six": get_env_path("ProgramFiles(x86)"),
                    "all users profile": get_env_path("ALLUSERSPROFILE"),
                    "public user profile": get_env_path("PUBLIC"),
                    "app data": get_env_path("APPDATA"),
                    "local app data": get_env_path("LOCALAPPDATA"),
                    "program data": get_env_path("ProgramData"),
                    "temp dir": get_env_path("TEMP"),
                    "one drive": onedrive_path,
                }.items()
                if path is not None
            }
        )

        # OneDrive subpaths.
        if onedrive_path:
            # this is probably not the correct way to check for OneDrive, quick and dirty
            onedrive_desktop_path = onedrive_path / "Desktop"
            if onedrive_desktop_path.is_dir():
                default_system_paths.update(
                    {
                        "one drive desktop": onedrive_desktop_path,
                        "one drive documents": onedrive_path / "Documents",
                        "one drive pictures": onedrive_path / "Pictures",
                    }
                )
    else:  # Mac and Linux.
        default_system_paths.update(
            {
                # TODO: Correct this for Mac and Linux.
                "desktop": home / "Desktop",
                "documents": home / "Documents",
                "downloads": home / "Downloads",
                "music": home / "Music",
                "pictures": home / "Pictures",
                "videos": home / "Videos",
            }
        )

    # Aliases.
    default_system_paths.update(
        {
            "desk": default_system_paths["desktop"],
            "docks": default_system_paths["documents"],
        }
    )

    if app.platform == "windows":
        default_system_paths.update(
            {
                "win dir": default_system_paths["system root"],
                "user profile": default_system_paths[
                    "user"
                ],  # We also have the long form for other profile folders.
            }
        )
    else:
        default_system_paths.update(
            {
                "home": default_system_paths["user"],
            }
        )

    # Build .talon-list file.
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


@mod.capture(rule="{user.system_paths} | {user.virtual_system_path}")
def possibly_virtual_system_path(m) -> str:
    """A physical or virtual system path, i.e., a combination of the lists `user.system_path` and `user.virtual_system_path`."""
    return str(m)


app.register("ready", on_ready)
