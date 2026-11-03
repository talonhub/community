"""The launch applications editor: its native window (via the kit's HostWindow; it
reopens after the title bar's X), showing it on one entry, launching an app. The
model (store) and the drawing (view) are mixins."""

import threading
import egui
from talon import actions, cron
from ...egui_kit import native
from ...egui_kit.host import HostWindow
from ...egui_kit.theme import THEME
from .store import StoreMixin
from .view import EditorMenu, ViewMixin


WINDOW_TITLE = "Launch applications"


class Editor(StoreMixin, ViewMixin):
    def __init__(self, path: str):
        # launch_applications.json (the Talon surface passes this machine's).
        self.path = path
        self.lock = threading.RLock()
        self.entries: list[dict] = []
        self.baseline: dict[int, tuple] = {}
        self.mtime = 0.0
        self.message = ""
        self.selected: int | None = None
        self.filter = "enabled"
        self.exe_filter: str | None = None
        self.query = egui.Mutable("")
        self.new_form = egui.Mutable("")
        self.showing = False
        # Edits save themselves a moment after they're made, and changes made to the
        # file elsewhere (app_switcher adding new apps, a text editor) load in.
        self.save_job = None
        self.saved_at: float | None = None
        # Spoken form -> unique_identifier, from app_switcher's live user.launch list
        # (which includes the forms it generates from display names).
        self.launch_map: dict[str, str] = {}
        # The same list turned around: unique_identifier (lower case) -> its forms.
        self.auto_forms: dict[str, list[str]] = {}
        self.form_notice = ""
        # The right-click menu, while open.
        self.menu: EditorMenu | None = None
        self.poll_job = cron.interval("1s", self.poll)

        # unique_identifiers (lower case), for an exact-identifier search.
        self.identifiers: set[str] = set()
        # The native window. Under a unique title until it's found (so a window a previous
        # load left behind can't be picked up); reopens after the title bar's X.
        self.host = HostWindow(
            WINDOW_TITLE,
            self.render,
            theme=THEME,
            unique_lookup=True,
            tag="launch_applications_editor",
            decorated=True,
            resizable=True,
            draggable=True,
            autosize=False,
            toplevel=False,
            focusable=True,
        )

    @property
    def window(self):
        return self.host.window

    @property
    def hwnd(self) -> int | None:
        return self.host.hwnd

    # --- file ---







    # --- showing ---

    def show(self):
        # Closed with the title bar's X: a new window.
        self.host.ensure_open()
        self.load()
        self.showing = True
        # Fit the work area (physical pixels, without the taskbar) of the monitor in use.
        left, top, right, bottom = native.foreground_work_area()
        width, height = int((right - left) * 0.92), int((bottom - top) * 0.92)
        x, y = left + ((right - left) - width) // 2, top + ((bottom - top) - height) // 2
        self.target = (x, y, x + width, y + height)
        self.host.show(focus=True)
        self.host.when_ready(self.place)

    def show_entry(self, app_id: str) -> bool:
        """Open on one entry, by its unique_identifier: selected, with the list showing
        all entries, searched by that identifier. False if there's no such entry."""
        self.show()
        with self.lock:
            index = next(
                (i for i, e in enumerate(self.entries) if (e.get("unique_identifier") or "").lower() == app_id.lower()), None
            )
            if index is None:
                return False
            self.selected = index
            self.filter = "all"
            self.exe_filter = None
            self.menu = None
            entry = self.entries[index]
            self.query.set(entry.get("unique_identifier") or entry.get("display_name") or "")
            self.new_form.set("")
            self.form_notice = ""
        self.window.refresh()
        return True

    def place(self, hwnd: int):
        """Move the native window into place, once it exists."""
        native.move_hwnd(hwnd, self.target)
        # egui only lays out again on its next frame; ask for a few after the move.
        for delay in ("0ms", "100ms", "300ms", "600ms"):
            cron.after(delay, self.window.refresh)

    def hide(self):
        self.showing = False
        self.host.hide()

    def shutdown(self):
        self.showing = False
        if getattr(self, "poll_job", None) is not None:
            cron.cancel(self.poll_job)
            self.poll_job = None
        if getattr(self, "save_job", None) is not None:
            cron.cancel(self.save_job)
            self.save_job = None
            self.save()
        self.host.close()

    # --- model (lock held) ---

    # The search, the Show filter and the executable filter combine (AND). Each side's
    # counts are what picking that row would show, given the other two.







    # --- drawing ---









    def launch(self, e: dict):
        """Launch (or focus, if it's running) the app the way "launch" commands do."""
        uid = e.get("unique_identifier")
        if not uid:
            return
        print(f"launch_applications_editor: launching {e.get('display_name')}")

        def run():
            try:
                actions.user.switcher_launch(uid)
            except Exception as ex:
                with self.lock:
                    self.message = f"Couldn't launch {e.get('display_name')}: {ex}"
                self.window.refresh()

        cron.after("0ms", run)
