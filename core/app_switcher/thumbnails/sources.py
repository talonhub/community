"""Which windows the switcher shows: candidates in z-order, every window, one app's."""

import os
from talon import actions, ui
from . import dwm_thumbnails as dwm
from .model import is_switchable, window_model_id


def is_candidate(window: ui.Window) -> bool:
    try:
        return (
            bool(window.title)
            # Talon's own windows: the HUD, this switcher, ...
            and dwm.window_pid(window.id) != os.getpid()
            and is_switchable(window.id)
        )
    except Exception:
        return False


def sort_by_z_order(windows: list[ui.Window]) -> list[ui.Window]:
    order = dwm.z_order()
    return sorted(windows, key=lambda w: order.get(w.id, len(order)))


def all_windows() -> list[ui.Window]:
    """Every open or minimized top-level window, on any virtual desktop.

    ui.windows() rather than each foreground app's windows: an app whose windows are
    all on other desktops counts as a background app.
    """
    windows = [w for w in ui.windows() if is_candidate(w)]
    # A window can be listed twice, e.g. a console under cmd and conhost; keep the
    # first window object.
    unique = {w.id: w for w in reversed(windows)}
    return sort_by_z_order(list(unique.values()))


def application_windows(name: str) -> list[ui.Window]:
    """Windows for an entry of the community user.running_applications list.

    Entries are "<app name>" or "<app name>-::*::-<AppUserModelID>"; with an ID, only
    the windows carrying that ID are shown, so e.g. one PWA hosted by a browser.
    """
    splits = name.split("-::*::-")
    app_name = splits[0]
    model_id = splits[1] if len(splits) > 1 and splits[1] != "None" else None

    try:
        found = actions.user.get_running_app(app_name)
    except Exception:
        found = [a for a in ui.apps(background=False) if a.name.lower() == app_name.lower()]

    windows = []
    for item in found:
        if isinstance(item, ui.Window):
            # The app switcher maps an app's entry to exactly its windows (one MMC
            # console, one PWA), not to all windows of their process.
            candidates = [item]
        else:
            candidates = item.windows()
        windows.extend(w for w in candidates if is_candidate(w))

    if model_id:
        matching = [
            w
            for w in windows
            if str(window_model_id(w.id)).lower() == model_id.lower()
        ]
        # The default window of an app may carry no ID at all; keep everything then.
        windows = matching or windows

    unique = {w.id: w for w in windows}
    return sort_by_z_order(list(unique.values()))


def with_windows(windows: list[ui.Window], extra: list[ui.Window]) -> list[ui.Window]:
    """`windows` plus any of `extra` it lacks, in z-order."""
    ids = {w.id for w in windows}
    return sort_by_z_order(windows + [w for w in extra if w.id not in ids])
