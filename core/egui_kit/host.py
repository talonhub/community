"""HostWindow: the lifecycle of a talon.egui window, and surviving hot reloads.

What every tool needs and egui's Window doesn't give:
  * a first-frame setup (theme visuals, AccessKit for UI Automation)
  * extra frames after a change: the window shows a frame late, so what one repaint
    draws only appears with the next (`repaint(frames=2)`)
  * the native handle, found by title once egui has created the window (optionally
    under a unique title, so a window a previous load left behind can't be picked up)
  * reopening after the title bar's X: a closed Window never shows again
  * `replace()`: Talon reloads a module but the old instance's Window, cron jobs and
    render callback live on; shut the old instance down and stash the new one
"""

import sys

from talon import cron
from talon.egui import Window

from . import native

WINDOW_PROPERTIES = ("decorated", "resizable", "draggable", "autosize", "toplevel", "focusable")


class HostWindow:
    def __init__(self, title: str, content, *, theme=None, unique_lookup: bool = False, tag: str = "egui_kit", **properties):
        """`content` is the tool's `async def render(ui)`. `properties` are Window
        properties (decorated, resizable, draggable, autosize, toplevel, focusable).
        With `unique_lookup`, the window carries a unique title until its handle is
        found. `theme` (a theme.Theme) sets egui's visuals on the first frame."""
        unknown = set(properties) - set(WINDOW_PROPERTIES)
        if unknown:
            raise TypeError(f"unknown window properties: {sorted(unknown)}")
        self.title = title
        self.content = content
        self.theme = theme
        self.tag = tag
        self.properties = properties
        self.lookup_title = f"{title} [{id(self):x}]" if unique_lookup else title
        self.hwnd: int | None = None
        self._prepared = False
        self._repaints = 0
        self._ready_job = None
        self.window = self._make_window()

    def _make_window(self) -> Window:
        window = Window()
        window.title = self.title
        for name in WINDOW_PROPERTIES:
            if name in self.properties:
                setattr(window, name, self.properties[name])
        window.set_content(self._render)
        return window

    async def _render(self, ui):
        ctx = ui.ctx()
        if not self._prepared:
            if self.theme is not None:
                try:
                    self.theme.apply(ctx)
                except Exception as e:
                    print(f"{self.tag}: applying the theme failed: {e!r}")
            try:
                ctx.enable_accesskit()
            except Exception as e:
                print(f"{self.tag}: enable_accesskit failed: {e!r}")
            self._prepared = True
        if self._repaints > 0:
            self._repaints -= 1
            if self._repaints:
                ctx.request_repaint()
        await self.content(ui)

    # --- showing ---

    def ensure_open(self) -> bool:
        """After the title bar's X destroyed the native window, make a new Window (a
        closed one never shows again). True if it did."""
        if self.hwnd is None or native.is_window(self.hwnd):
            return False
        try:
            self.window.close()
        except Exception:
            pass
        self.window = self._make_window()
        self.hwnd = None
        self._prepared = False
        return True

    def show(self, focus: bool = False):
        if self.hwnd is None and self.lookup_title != self.title:
            self.window.title = self.lookup_title
        self.window.show()
        if focus:
            self.window.focus()

    def hide(self):
        self.window.hide()

    def focus(self):
        self.window.focus()

    def refresh(self):
        self.window.refresh()

    def repaint(self, frames: int = 2):
        """Redraw after a change, `frames` frames in a row (see the module docstring)."""
        self._repaints = frames
        self.window.refresh()

    # --- the native window ---

    def find_hwnd(self) -> int | None:
        """The native handle, once egui has created the window; None before that."""
        if self.hwnd is not None and native.is_window(self.hwnd):
            return self.hwnd
        hwnd = native.find_own_hwnd(self.lookup_title)
        if hwnd is not None:
            self.hwnd = hwnd
            if self.lookup_title != self.title:
                self.window.title = self.title
        return hwnd

    def when_ready(self, callback, tries: int = 40, every: str = "50ms"):
        """Call `callback(hwnd)` once the native window exists (it only does after
        egui's first frame), polling `tries` times."""
        if self._ready_job is not None:
            cron.cancel(self._ready_job)
            self._ready_job = None

        def poll(left: int):
            self._ready_job = None
            hwnd = self.find_hwnd()
            if hwnd is not None:
                callback(hwnd)
            elif left > 1:
                self._ready_job = cron.after(every, lambda: poll(left - 1))
            else:
                print(f"{self.tag}: couldn't find the window")
                self.window.title = self.title

        self._ready_job = cron.after(every, lambda: poll(tries))

    def move(self, rect: tuple[int, int, int, int]):
        if self.hwnd is not None:
            native.move_hwnd(self.hwnd, rect)

    def close(self):
        if self._ready_job is not None:
            cron.cancel(self._ready_job)
            self._ready_job = None
        self.window.close()

    # --- hot reload ---

    @staticmethod
    def replace(stash_key: str, factory, *, legacy_keys=(), before_create=None, tag: str = "egui_kit"):
        """Shut down the instance a previous load stashed on `sys` under `stash_key`
        (or under any of `legacy_keys`, which may hold a list), then make, stash and
        return a new one with `factory()`. Instances need a `shutdown()`."""
        previous = []
        for key in (stash_key, *legacy_keys):
            value = getattr(sys, key, None)
            for instance in value if isinstance(value, list) else [value]:
                if instance is not None and all(instance is not p for p in previous):
                    previous.append(instance)
        for instance in previous:
            try:
                instance.shutdown()
            except Exception as e:
                print(f"{tag}: shutting down a previous instance failed: {e!r}")
        for key in legacy_keys:
            setattr(sys, key, None)
        if before_create is not None:
            try:
                before_create()
            except Exception as e:
                print(f"{tag}: cleaning up before a new instance failed: {e!r}")
        instance = factory()
        setattr(sys, stash_key, instance)
        return instance
