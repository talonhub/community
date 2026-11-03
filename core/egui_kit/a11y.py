"""Accessibility (UI Automation via AccessKit) for custom-painted egui controls.

Hinting tools such as windows-hinting find controls through UIA, so every control
painted by hand needs an interactive area with a stable id and a role, name and state.
"""

import os
from collections import Counter

import egui
from talon import ui


class Ids:
    """Stable egui ids under a per-tool prefix (so two tools' ids never collide)."""

    def __init__(self, prefix: str):
        self.prefix = prefix

    def id(self, key: str) -> egui.Id:
        return egui.Id(f"{self.prefix}:{key}")

    def hit(self, ui: egui.Ui, rect: egui.Rect, key: str) -> egui.Response:
        """A clickable area with a stable id (so its accessibility node is stable across
        frames) that doesn't move the layout cursor."""
        return ui.interact(rect, self.id(key), egui.Sense.click())


def describe(resp: egui.Response, typ, label: str, enabled: bool = True, selected: bool | None = None):
    """Give a custom-painted control an accessibility node (role, name, state), so
    UI Automation clients such as windows-hinting can find and click it."""
    try:
        if selected is None:
            info = egui.WidgetInfo.labeled(typ, enabled, label)
        else:
            info = egui.WidgetInfo.selected(typ, enabled, selected, label)
        resp.widget_info(info)
    except Exception as e:  # never let accessibility break drawing
        print(f"egui_kit: widget_info failed: {e!r}")


def name_text_edit(resp: egui.Response, label: str, value: str, hint: str):
    """Text fields drawn without a frame or visible label still need a UIA name."""
    try:
        info = egui.WidgetInfo.text_edit(True, value, value, hint)
        info.label = label
        resp.widget_info(info)
    except Exception as e:
        print(f"egui_kit: naming a text field failed: {e!r}")


def dump_uia(title: str, tag: str, max_depth: int = 8, max_lines: int = 120):
    """Print a window's UI Automation tree (this process's window titled `title`), as
    hinting tools see it, to the Talon log."""
    pid = os.getpid()
    windows = [w for w in ui.windows() if w.title == title and w.app.pid == pid]
    if not windows:
        print(f"{tag}: UIA dump: window not found")
        return
    counts = Counter()
    lines = []

    def walk(el, depth):
        try:
            kind = str(el.control_type)
            name = el.name
        except Exception as e:
            lines.append("  " * depth + f"<error {e!r}>")
            return
        counts[kind] += 1
        if len(lines) < max_lines:
            lines.append("  " * depth + f"{kind} {name!r}")
        if depth >= max_depth:
            return
        try:
            for child in el.children:
                walk(child, depth + 1)
        except Exception as e:
            lines.append("  " * depth + f"<children error {e!r}>")

    walk(windows[0].element, 0)
    print(f"{tag}: UIA dump\n" + "\n".join(lines))
    print(f"{tag}: UIA counts {dict(counts)}")
