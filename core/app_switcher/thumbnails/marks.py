"""Marking several windows (multi-select), and acting on the marked ones: close,
minimize, restore, lay out, move to a desktop or screen."""

from talon import app
from ..windows import virtual_desktops as vd
from .config import LAYOUTS
from .model import Entry, tile_hwnds


class MarksMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    def _set_marks(self, entries: list, on: bool | None):
        """Mark (True), unmark (False) or toggle (None) these tiles; with the lock held."""
        for entry in entries:
            hwnds = tile_hwnds(entry)
            add = on if on is not None else not all(h in self.marked for h in hwnds)
            if add:
                self.marked += [h for h in hwnds if h not in self.marked]
            else:
                self.marked = [h for h in self.marked if h not in hwnds]
            self.mark_anchor = entry.hwnd

    def mark(self, indices: list[int], on: bool | None = None):
        """Toggle the marks of the tiles with these numbers; or set them with `on`."""
        with self.lock:
            self._set_marks([self.entries[i - 1] for i in indices if 0 < i <= len(self.entries)], on)
        self.refresh()

    def mark_range(self, first: int, last: int):
        """Mark tiles `first` through `last` (numbers, either order)."""
        self.mark(list(range(min(first, last), max(first, last) + 1)), on=True)

    def mark_to(self, index: int):
        """Shift+click: mark from the last marked (or the selected) tile to tile `index`."""
        with self.lock:
            anchor = next((i + 1 for i, e in enumerate(self.entries) if e.hwnd == self.mark_anchor), self.selected + 1)
        self.mark_range(anchor, index)

    def mark_all(self):
        """Mark every tile the search shows."""
        with self.lock:
            self._set_marks(self.entries, True)
        self.refresh()

    def clear_marks(self):
        with self.lock:
            self.marked = []
            self.mark_anchor = None
        self.refresh()

    def marked_entries(self) -> list[Entry]:
        """The marked windows in the order they were marked, shown or not."""
        with self.lock:
            by_hwnd = {e.hwnd: e for e in self.pool}
            return [by_hwnd[h] for h in self.marked if h in by_hwnd]

    def _targets(self, fallback: bool) -> tuple[list[Entry], bool]:
        """The marked windows, and whether they are marked ones; with none marked and
        `fallback`, the selected tile's window(s)."""
        marked = self.marked_entries()
        if marked or not fallback:
            return marked, bool(marked)
        with self.lock:
            entry = self.entries[self.selected] if 0 <= self.selected < len(self.entries) else None
        return (list(getattr(entry, "windows", [entry])) if entry is not None else []), False

    def close_marked(self, fallback: bool = False):
        """Close the marked windows (or with `fallback` and none marked, the selected one).
        The marks go with the windows as they close; one that stays open (asking to save)
        stays marked."""
        entries, marked = self._targets(fallback)
        if entries:
            self.close_windows(entries=entries)

    def minimize_marked(self):
        entries, marked = self._targets(False)
        if entries:
            self.minimize_windows(entries=entries)

    def restore_marked(self):
        entries, marked = self._targets(False)
        if entries:
            self.restore_windows(entries=entries)

    def layout_marked(self, layout: str):
        """Snap the marked windows into `layout`'s positions, in the order they were
        marked; they stay marked (only closing and clearing unmark)."""
        entries, marked = self._targets(False)
        if entries:
            self.layout_windows([], LAYOUTS[layout], entries=entries)

    def move_marked_to_desktop(self, number: int | None = None, offset: int = 0):
        """Move the marked windows to a desktop; they stay marked."""
        entries, marked = self._targets(False)
        if entries:
            self.move_to_desktop([], number=number, offset=offset, entries=entries)

    def move_marked_to_new_desktop(self):
        try:
            desktop = vd.create_desktop()
        except OSError as e:
            app.notify("Thumbnail switcher", f"Couldn't create a desktop: {e}")
            return
        with self.lock:
            self.desktops, self.current_desktop = self._read_desktops()
        self.move_marked_to_desktop(number=desktop.number)

    def move_marked_to_screen(self, screen: int | None = None, offset: int = 0):
        """Move the marked windows to a screen; they stay marked."""
        entries, marked = self._targets(False)
        if not entries:
            return
        self._hold_focus()
        for entry in entries:
            self._move_window_to_screen(entry, screen, offset)
        self._take_focus()
        self.sync()
