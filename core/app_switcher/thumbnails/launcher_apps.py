"""What the app launcher view lists: installed apps, how running apps map to them, and
launching.

Installed apps are the app switcher's launch list (shell:AppsFolder merged with
launch_applications.json: its display names, minus excluded entries such as Parallels'
"(Mac)" shortcuts); without the app switcher, shell:AppsFolder itself. Running apps are
matched to them by AppUserModelID, MMC console, executable or name, so a running app
appears once, in the Running section.

Apps launch through the shell (explorer.exe shell:AppsFolder\\<id>), like the app
switcher's `switcher_launch`, so Store apps, PWAs, MMC consoles and shortcuts start the
way the Start menu starts them.
"""

import os
import subprocess
import sys
import threading
import time
import zlib

from ..windows import app_icons, app_identity, shell_apps

COMMUNITY = "user.community.core.app_switcher.app_switcher"
# The launcher's icon size (its tiles' APP_ICON_PIXELS).
ICON_PIXELS = 128


def icon_source(app_id: str) -> str:
    """An installed app's icon source for app_icons."""
    return f"shell:AppsFolder\\{app_id}"


class InstalledApp:
    """A not-running app in the launcher. It stands in for an entry where the switcher
    expects one; its `hwnd` is a made-up negative number, as tiles, textures and menus
    are keyed by hwnd."""

    def __init__(self, name: str, app_id: str, hwnd: int):
        self.app_name = self.title = name
        self.app_id = app_id
        self.hwnd = hwnd
        self.windows = []
        # From the shared cache if it has it; load_icons fetches the rest.
        self.icon = app_icons.peek(icon_source(app_id), ICON_PIXELS)
        self.search_text = name.lower()
        self.exe_name = ""
        self.model_id = None
        self.key = ("launch", app_id.lower())
        self.minimized = self.away = False
        self.iconic = True
        self.desktop = self.desktop_key = self.desktop_number = None
        self.desktop_numbers = []
        self.screen_number = None
        self.screen_numbers = []

    def state_label(self) -> str:
        return self.title


def stand_in_hwnd(app_id: str, used: set[int]) -> int:
    """A made-up negative hwnd for an installed app, the same every time for the same
    app: textures are cached by hwnd, so a number taken from the app's place in the list
    would show a neighbour's icon once an app is added or removed."""
    hwnd = -(1 + zlib.crc32(app_id.lower().encode("utf-8")))
    while hwnd in used:
        hwnd -= 1
    used.add(hwnd)
    return hwnd


class LaunchList:
    """The installed apps, with lookups to match running apps against."""

    def __init__(self):
        apps: list[tuple[str, str, str | None]] = []
        community = sys.modules.get(COMMUNITY)
        entries = getattr(community, "APPLICATIONS_DICT", None) if community else None
        if entries:
            seen = set()
            for entry in entries.values():
                app_id = entry.unique_identifier
                if not app_id or app_id.lower() in seen or entry.exclude:
                    continue
                seen.add(app_id.lower())
                apps.append((entry.display_name, app_id, entry.path))
        else:
            apps = [(item.name, item.app_id, item.path) for item in shell_apps.apps_folder_items()]
        apps.sort(key=lambda app: app[0].lower())
        used: set[int] = set()
        self.apps = [InstalledApp(name, app_id, stand_in_hwnd(app_id, used)) for name, app_id, _path in apps]
        self.by_id = {app.app_id.lower(): app for app in self.apps}
        self.by_name = {app.app_name.lower(): app for app in self.apps}
        self.by_path = {}
        for app, (_name, _id, path) in zip(self.apps, apps):
            # Not by host executables: every MMC console is mmc.exe.
            if path and os.path.basename(path).lower() not in set(app_identity.HOST_DOCUMENTS) | app_identity.COMMAND_LINE_HOSTS:
                self.by_path.setdefault(str(path).lower(), app)

    def match(self, hwnd: int, fallback: str = "") -> InstalledApp | None:
        """The installed app a running window belongs to, if it's in the list."""
        identity = app_identity.resolve(hwnd, fallback)
        for key in (identity.model_id, identity.document_id):
            if key and key.lower() in self.by_id:
                return self.by_id[key.lower()]
        if identity.exe_path:
            app = self.by_path.get(identity.exe_path.lower())
            if app is None:
                app_id = shell_apps.app_id_for_path(identity.exe_path)
                app = self.by_id.get(app_id.lower()) if app_id else None
            if app is not None and identity.process not in app_identity.COMMAND_LINE_HOSTS:
                return app
        return self.by_name.get(identity.name.lower())


def launch(app_id: str | None = None, path: str | None = None):
    """Start an app: by its Apps folder id through the shell, else its executable. For a
    running app this starts another instance where the app supports one (single-instance
    apps bring up their window)."""
    if app_id:
        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])
    elif path:
        os.startfile(path)


def load_icons(apps: list[InstalledApp], size: int, on_progress):
    """Fill in the apps' icons from the shared cache (app_icons), fetching missing ones
    in the background (there can be hundreds); `on_progress` redraws the launcher as
    they arrive, at most every 0.1 s, and after the last one."""
    missing = [app for app in apps if app.icon is None]
    pending = {"left": len(missing), "last": 0.0}
    lock = threading.Lock()

    def arrived(app, icon):
        app.icon = icon
        with lock:
            pending["left"] -= 1
            now = time.monotonic()
            due = pending["left"] <= 0 or now - pending["last"] >= 0.1
            if due:
                pending["last"] = now
        if due:
            on_progress()

    # Most recent requests are fetched first: ask for the list's end first, so its
    # start (on screen when the launcher opens) comes first.
    for app in reversed(missing):
        icon = app_icons.get(icon_source(app.app_id), size, on_ready=lambda icon, app=app: arrived(app, icon))
        if icon is not None:
            app.icon = icon
            with lock:
                pending["left"] -= 1
    if missing and pending["left"] < len(missing):
        on_progress()
