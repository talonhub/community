"""Guided placement: filling a layout's slots one window at a time, the slot overlay and
the numbered grid overlay, and their stacking."""

import sys
import egui
from talon import ui
from talon.egui import Window
from ...egui_kit import native
from . import dwm_thumbnails as dwm
from ..windows import virtual_desktops as vd
from .config import GRID_OVERLAY_TITLE, LAYOUTS, OVERLAY_THICKNESS, OVERLAY_TITLE, SELECTED
from .model import Entry


class Placement:
    """Filling a layout's slots one window at a time."""

    def __init__(self, layout: str, slots: list[str], screen: ui.Screen):
        self.layout = layout
        self.slots = slots
        self.screen = screen
        self.index = 0
        # Window handle -> the slot it was put in.
        self.placed: dict[int, str] = {}

    @property
    def slot(self) -> str:
        return self.slots[self.index]


def slot_label(slot: str) -> str:
    return slot.lower().replace("_", " ")


def slot_fractions(slot: str):
    """(left, top, right, bottom) of a snap position, from community's window_snap.py."""
    snap = sys.modules.get("user.community.core.windows_and_tabs.window_snap")
    pos = snap._snap_positions[slot]
    return pos.left, pos.top, pos.right, pos.bottom


def slot_rect(screen: ui.Screen, slot: str) -> ui.Rect:
    left, top, right, bottom = slot_fractions(slot)
    r = screen.visible_rect
    return ui.Rect(
        round(r.x + r.width * left),
        round(r.y + r.height * top),
        round(r.width * (right - left)),
        round(r.height * (bottom - top)),
    )


class SlotOverlay:
    """A frame on screen around the slot the next window goes to.

    A separate, never-focused egui window shaped to just the frame, so the switcher
    keeps the keyboard and the inside stays visible and clickable.
    """

    def __init__(self):
        self.rect: tuple[int, int, int, int] | None = None
        self.hwnd: int | None = None
        self.showing = False
        self.window = Window()
        self.window.title = OVERLAY_TITLE
        self.window.decorated = False
        self.window.resizable = False
        self.window.draggable = False
        self.window.autosize = False
        self.window.toplevel = True
        self.window.focusable = False
        self.window.set_content(self.render)

    def show(self, rect: ui.Rect):
        self.rect = (int(rect.x), int(rect.y), int(rect.x + rect.width), int(rect.y + rect.height))
        self.showing = True
        self.window.show()
        self.place()

    def place(self):
        """Fit the native window to the slot; called again from the switcher's tick."""
        if not self.showing or self.rect is None:
            return
        if self.hwnd is None or not native.is_window(self.hwnd):
            self.hwnd = native.find_own_hwnd(OVERLAY_TITLE)
            if self.hwnd is None:
                return
        if native.hwnd_rect(self.hwnd) != self.rect:
            native.move_hwnd(self.hwnd, self.rect)
            left, top, right, bottom = self.rect
            dwm.make_overlay(self.hwnd, right - left, bottom - top, OVERLAY_THICKNESS)

    def hide(self):
        self.showing = False
        self.window.hide()

    async def render(self, ui: egui.Ui) -> None:
        ui.painter().rect_filled(ui.clip_rect(), 0, SELECTED)

    def close(self):
        self.hide()
        self.window.close()


class GridOverlay:
    """Placing windows into a layout: the screen dimmed a little, with every slot of
    the layout outlined and the current one filled in. A click-through layer under
    the switcher and the slot's frame (which are topmost), and under the windows
    already placed, so they show at full brightness landing in their slots; not
    topmost itself, so placed windows can go above it."""

    # How much the layer covers what's below, of 255: about 40%, so windows behind
    # show through at about 60% brightness. Lines and numbers are drawn bright to
    # stay readable through it.
    ALPHA = 105

    def __init__(self):
        self.rect: tuple[int, int, int, int] | None = None
        self.cells: list[tuple[int, int, int, int]] = []
        self.current = 0
        self.repaints = 0
        self.hwnd: int | None = None
        self.showing = False
        self.window = Window()
        self.window.title = GRID_OVERLAY_TITLE
        self.window.decorated = False
        self.window.resizable = False
        self.window.draggable = False
        self.window.autosize = False
        self.window.toplevel = False
        self.window.focusable = False
        self.window.set_content(self.render)

    def show(self, screen_rect: ui.Rect, cells: list[ui.Rect], current: int):
        """`screen_rect` and `cells` in physical pixels; `current` is the slot to fill."""
        self.rect = (int(screen_rect.x), int(screen_rect.y), int(screen_rect.x + screen_rect.width), int(screen_rect.y + screen_rect.height))
        self.cells = [(int(c.x), int(c.y), int(c.x + c.width), int(c.y + c.height)) for c in cells]
        self.current = current
        self.showing = True
        self.window.show()
        self.place()
        # The window shows a frame late (see Switcher.refresh): without the extra
        # frame, a new layout would appear with the previous one's cells.
        self.repaints = 2
        self.window.refresh()

    def place(self, above: int | None = None):
        """Fit the native window to the screen and keep it right below `above` (a
        placed window), or at the top of the ordinary windows."""
        if not self.showing or self.rect is None:
            return
        if self.hwnd is None or not native.is_window(self.hwnd):
            self.hwnd = native.find_own_hwnd(GRID_OVERLAY_TITLE)
            if self.hwnd is None:
                return
        if not dwm.is_layered(self.hwnd):
            # Talon/winit can reset the extended styles (on show); without them the
            # layer is opaque.
            dwm.make_scrim(self.hwnd, self.ALPHA)
        if native.hwnd_rect(self.hwnd) != self.rect:
            native.move_hwnd(self.hwnd, self.rect)
        if above is not None:
            dwm.place_below(self.hwnd, above)
        else:
            dwm.raise_quietly(self.hwnd, topmost=False)

    def hide(self):
        self.showing = False
        self.window.hide()

    async def render(self, ui: egui.Ui) -> None:
        if self.repaints > 0:
            self.repaints -= 1
            if self.repaints:
                ui.ctx().request_repaint()
        painter = ui.painter()
        painter.rect_filled(ui.clip_rect(), 0, egui.Color32.from_rgb(0, 0, 0))
        if self.rect is None or self.hwnd is None:
            return
        ppp = (dwm.user32.GetDpiForWindow(self.hwnd) or 96) / 96
        left, top = self.rect[0], self.rect[1]
        for i, (l, t, r, b) in enumerate(self.cells):
            cell = egui.Rect.from_min_max(
                egui.Pos2((l - left) / ppp + 4, (t - top) / ppp + 4), egui.Pos2((r - left) / ppp - 4, (b - top) / ppp - 4)
            )
            if i == self.current:
                painter.rect_filled(cell, 10, egui.Color32.from_rgb(60, 140, 255))
                painter.rect_stroke(cell, 10, egui.Stroke(8.0, egui.Color32.from_rgb(120, 190, 255)), egui.StrokeKind.Inside)
            else:
                painter.rect_stroke(cell, 10, egui.Stroke(5.0, egui.Color32.from_rgb(255, 255, 255)), egui.StrokeKind.Inside)
            painter.text(cell.center(), egui.Align2.CENTER_CENTER, str(i + 1), egui.FontId.proportional(80.0), egui.Color32.from_rgb(255, 255, 255))

    def close(self):
        self.hide()
        self.window.close()


class PlacementMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    def start_placement(self, layout: str):
        """Fill `layout`'s slots on the switcher's screen; numbers now pick windows."""
        if not self.showing:
            return
        placement = Placement(layout, LAYOUTS[layout], self._screen())
        with self.lock:
            self.placement = placement
        self._show_slot()
        self.refresh()
        # Marked windows fill the first slots, in the order they were marked.
        marked = self.marked_entries()
        if marked:
            for entry in marked[: len(placement.slots)]:
                self._place(entry)

    def place(self, index: int):
        """Put the window on tile `index` into the current slot and move on."""
        entries = self.entries_at([index])
        if entries:
            self._place(entries[0])

    def _place(self, entry: Entry):
        with self.lock:
            placement = self.placement
        if placement is None:
            return
        self._hold_focus()
        try:
            if entry.away and self.current_desktop is not None:
                vd.move_window(entry.hwnd, next(d.guid for d in self.desktops if d.guid.key() == self.current_desktop))
            dwm.make_normal(entry.hwnd)
            entry.window.rect = slot_rect(placement.screen, placement.slot)
            # In front of the other windows (under the switcher and its overlays, which
            # stay on top), so it can be seen landing in its slot.
            dwm.raise_quietly(entry.hwnd)
        except Exception as e:
            print(f"thumbnail_switcher: placing {entry.title!r} failed: {e!r}")
        with self.lock:
            placement.placed[entry.hwnd] = placement.slot
        self.skip_slot()
        self._take_focus()
        self.sync()

    def skip_slot(self):
        """Move on to the next slot; after the last one, placement is done."""
        with self.lock:
            placement = self.placement
            if placement is None:
                return
            placement.index += 1
            done = placement.index >= len(placement.slots)
        if done:
            with self.lock:
                placed = [e for h in placement.placed for e in self.pool if e.hwnd == h]
            self.end_placement()
            if placed:
                # The layout is complete: show it, the last window placed focused.
                self._finish_layout(placed)
        else:
            self._show_slot()
        self.refresh()

    def end_placement(self):
        with self.lock:
            self.placement = None
        self.overlay.hide()
        self.grid_overlay.hide()
        self.refresh()

    def _show_slot(self):
        with self.lock:
            placement = self.placement
        if placement is not None:
            # Showing the grid layer (an ordinary, not topmost window) can take the
            # focus for a moment; the switcher takes it back rather than closing.
            self._hold_focus()
            try:
                self.grid_overlay.show(
                    placement.screen.visible_rect, [slot_rect(placement.screen, slot) for slot in placement.slots], placement.index
                )
                self.overlay.show(slot_rect(placement.screen, placement.slot))
                self._stack_overlays()
            except Exception as e:
                print(f"thumbnail_switcher: showing the slot outline failed: {e!r}")

    def _stack_overlays(self):
        """The switcher on top, then the slot's frame (both topmost), then the windows
        placed so far, then the dimmed grid over everything else."""
        if self.hwnd is None:
            return
        self.overlay.place()
        if self.overlay.hwnd is not None:
            dwm.place_below(self.overlay.hwnd, self.hwnd)
        with self.lock:
            placement = self.placement
            placed = [h for h in placement.placed if native.is_window(h)] if placement else []
        if placed and self.grid_overlay.hwnd is not None:
            # Keep every placed window above the grid, whatever reordered them since
            # (another app's window, or the app itself, coming forward), and the grid
            # right below the lowest of them.
            z = dwm.z_order()
            lowest_z = max(z.get(h, 0) for h in placed)
            ours = {self.hwnd, self.overlay.hwnd, self.grid_overlay.hwnd}
            # An ordinary window in between: raise the placed ones again, in order.
            if any(
                pos < lowest_z
                and h not in ours
                and h not in placed
                and dwm.user32.IsWindowVisible(h)
                and not dwm.is_topmost(h)
                and not dwm.is_cloaked(h)
                and not dwm.is_minimized(h)
                for h, pos in z.items()
            ):
                for h in placed:
                    dwm.raise_quietly(h)
                z = dwm.z_order()
            lowest = max(placed, key=lambda h: z.get(h, -1))
            self.grid_overlay.place(above=lowest)
        else:
            self.grid_overlay.place(above=None)

    def _screen(self) -> ui.Screen:
        """The screen the switcher is on."""
        if self.target is not None:
            x = (self.target[0] + self.target[2]) / 2
            y = (self.target[1] + self.target[3]) / 2
            for screen in ui.screens():
                r = screen.rect
                if r.x <= x < r.x + r.width and r.y <= y < r.y + r.height:
                    return screen
        return ui.main_screen()
