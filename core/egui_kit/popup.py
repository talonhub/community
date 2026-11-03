"""PopupHost: a popup (a menu) in a window of its own, so it can reach past its owner's
window.

Talon's egui embeds child viewports (`embed_viewports()` is True), so egui's own popups
are clipped to the window that draws them: a switcher showing one or two windows had to
grow for every menu. WinUI has the same problem and answer: Command Palette's context
menu is a Flyout with ShouldConstrainToRootBounds=False, a popup window of its own.

The window:
  * with `focusable` (as Command Palette's flyout), takes the focus when it shows. egui
    then treats it as focused (hover, clicks, tooltips as usual) and gets the keys; the
    owner counts it as its own in any focus rules and hands the focus back to itself
    *before* hiding it (hiding the active window lets Windows activate any other).
  * without (WS_EX_NOACTIVATE), the owner keeps the keyboard; but egui treats it as
    unfocused (draw_menu's `clicked=` hit-tests by pointer), and a click still
    activates it for a moment.
  * is topmost and raised on each show, so it's over the owner and over any DWM
    thumbnails the owner shows; off the taskbar; Windows 11's rounded corners.
  * is made once and reused: placed while hidden, then shown. A new window starts at
    winit's default spot and size; its first frame comes before it's on screen and
    puts it in place.

The owner draws the content (`content(ui)`, filling the window) and decides where it
goes: `place()` works out a rect beside an anchor, flipped at the screen's edges.
"""

from . import native
from .host import HostWindow


def place(
    anchor: tuple[int, int, int, int], size: tuple[int, int], bounds: tuple[int, int, int, int]
) -> tuple[int, int, int, int]:
    """Where a popup of `size` (w, h) opens from `anchor` (left, top, right, bottom):
    below it from its left edge; above it where there's no room below, and ending at
    its right edge where there's no room to the right. Kept inside `bounds` (a work
    area), and no taller or wider. All physical pixels. A point anchor (a right-click)
    is a rect of size 0."""
    left, top, right, bottom = bounds
    w, h = min(size[0], right - left), min(size[1], bottom - top)
    x = anchor[0] if anchor[0] + w <= right else anchor[2] - w
    y = anchor[3] if anchor[3] + h <= bottom else anchor[1] - h
    x = max(left, min(x, right - w))
    y = max(top, min(y, bottom - h))
    return (x, y, x + w, y + h)


class PopupHost:
    def __init__(self, title: str, content, *, theme=None, tag: str = "egui_kit", focusable: bool = False):
        """`content` is the owner's `async def render(ui)` for the popup; `title` must
        be unique among this process's windows (the handle is found by it)."""
        self.content = content
        self.focusable = focusable
        self.tag = tag
        # Where it should be (left, top, right, bottom), and whether it's showing.
        self.rect: tuple[int, int, int, int] | None = None
        self.visible = False
        self.host = HostWindow(
            title,
            self._render,
            theme=theme,
            tag=tag,
            decorated=False,
            resizable=False,
            draggable=False,
            autosize=False,
            toplevel=True,
            focusable=focusable,
        )
        self._styled = False

    def show(self, rect: tuple[int, int, int, int]):
        """Show at `rect` (physical pixels), or move there if showing."""
        moved = rect != self.rect
        self.rect = rect
        hwnd = self.host.find_hwnd() if self._styled else None
        if hwnd is not None and (moved or not self.visible):
            native.move_hwnd(hwnd, rect)
        if not self.visible:
            self.visible = True
            self.host.show(focus=self.focusable)
            if hwnd is not None:
                # Over the owner, which may have come forward since it last showed.
                native.raise_topmost(hwnd)
        if self.focusable and hwnd is not None and not self.has_focus():
            # Showing, or reopened from the owner (a right-click there while open).
            native.set_foreground(hwnd)
        self.host.repaint()

    def has_focus(self) -> bool:
        hwnd = self.host.hwnd
        return hwnd is not None and native.foreground() == hwnd

    def hide(self):
        if self.visible:
            self.visible = False
            self.host.hide()

    def repaint(self, frames: int = 2):
        if self.visible:
            self.host.repaint(frames)

    def close(self):
        self.visible = False
        self.host.close()

    async def _render(self, ui):
        if not self._styled:
            # The first frame, before the window is on screen: style it and put it in
            # place (it exists by now, though egui hasn't shown it yet).
            hwnd = self.host.find_hwnd()
            if hwnd is not None:
                native.make_popup(hwnd)
                if self.rect is not None:
                    native.move_hwnd(hwnd, self.rect)
                native.raise_topmost(hwnd)
                if self.focusable and self.visible:
                    native.set_foreground(hwnd)
                self._styled = True
            else:
                ui.ctx().request_repaint()
        elif self.visible and self.rect is not None and self.host.hwnd is not None and native.hwnd_rect(self.host.hwnd) != self.rect:
            # winit may apply its own geometry (on creation, or a DPI change).
            native.move_hwnd(self.host.hwnd, self.rect)
        if self.visible:
            await self.content(ui)
