"""Keyboard shortcuts, shown as key caps: one key, a combination, a legend or a list.

A `Shortcut` is its keys and what they do. Keys are written as Talon writes them:
"+" joins a combination ("ctrl+shift+p"), a space separates alternatives ("up down"
is either arrow). Names show as on the keyboard ("escape" as Esc, "up" as an arrow,
letters upper case); anything else (a range like "a-z") shows as written.

These are painted, not controls: a legend says what the keys do and is never clicked.
Measuring takes a painter, or None for an estimate (sizing a window before it draws).
"""

import egui

from .geom import P, R
from .text import estimate_width, text_width
from .theme import font
from .widgets import Kit

CAP_HEIGHT = 20.0
CAP_PAD = 5.0  # text to the cap's sides
CAP_RADIUS = 4.0
LIP = 2.0  # the cap's darker bottom edge
JOIN_GAP = 3.0  # around a "+" or "/" between caps
LABEL_GAP = 6.0  # caps to their label
ITEM_GAP = 14.0  # one shortcut to the next, in a legend

KEY_LABELS = {
    "up": "↑",
    "down": "↓",
    "left": "←",
    "right": "→",
    "enter": "Enter",
    "return": "Enter",
    "escape": "Esc",
    "esc": "Esc",
    "backspace": "Backspace",
    "delete": "Del",
    "insert": "Ins",
    "tab": "Tab",
    "space": "Space",
    "home": "Home",
    "end": "End",
    "pageup": "PgUp",
    "pagedown": "PgDn",
    "ctrl": "Ctrl",
    "shift": "Shift",
    "alt": "Alt",
    "win": "Win",
    "super": "Win",
    "cmd": "Cmd",
}


# Arrow keys are painted: the default fonts have no arrow glyphs. (direction x, y)
ARROWS = {"↑": (0, -1), "↓": (0, 1), "←": (-1, 0), "→": (1, 0)}


class Shortcut:
    """`keys` (as Talon writes them, see the module) and what they do."""

    def __init__(self, keys: str, label: str):
        self.keys = keys
        self.label = label


def key_label(name: str) -> str:
    """How a key shows on its cap: "escape" as Esc, "a" as A, "f5" as F5."""
    lower = name.lower()
    if lower in KEY_LABELS:
        return KEY_LABELS[lower]
    if len(name) == 1 or (lower[0] == "f" and lower[1:].isdigit()):
        return name.upper()
    return name


def parse(keys: str) -> list[list[str]]:
    """The alternatives of `keys`, each a combination's caps: "ctrl+k up" ->
    [["Ctrl", "K"], ["↑"]]."""
    return [[key_label(k) for k in alt.split("+") if k] for alt in keys.split()]


def _width(painter: egui.Painter | None, text: str, size: float) -> float:
    return text_width(painter, text, font(size)) if painter is not None else estimate_width(text, size)


def cap_width(painter: egui.Painter | None, label: str, size: float = 11.5) -> float:
    """A cap's width: its text and padding, and at least square."""
    return max(CAP_HEIGHT, _width(painter, label, size) + 2 * CAP_PAD)


def keys_width(painter: egui.Painter | None, keys: str, size: float = 11.5) -> float:
    """The width of `keys` as paint_keys draws them."""
    w = 0.0
    for a, combo in enumerate(parse(keys)):
        if a:
            w += 2 * JOIN_GAP + _width(painter, "/", size)
        for c, label in enumerate(combo):
            if c:
                w += 2 * JOIN_GAP + _width(painter, "+", size)
            w += cap_width(painter, label, size)
    return w


def paint_keycap(painter: egui.Painter, kit: Kit, rect: egui.Rect, label: str, size: float = 11.5):
    """One key cap: a raised key with `label` on it."""
    t = kit.theme
    painter.rect_filled(rect, CAP_RADIUS, t.border)
    face = R(rect.min.x, rect.min.y, rect.width(), rect.height() - LIP)
    painter.rect(face, CAP_RADIUS, t.surface_alt, egui.Stroke(1.0, t.input_border), egui.StrokeKind.Inside)
    if label in ARROWS:
        paint_arrow(painter, face.center(), ARROWS[label], size * 0.4, t.text)
    else:
        painter.text(face.center(), egui.Align2.CENTER_CENTER, label, font(size), t.text)


def paint_arrow(painter: egui.Painter, center: egui.Pos2, direction: tuple, r: float, color: egui.Color32):
    """An arrow through `center`, pointing `direction` ((0, -1) is up), `r` from its
    middle to its tip."""
    dx, dy = direction
    stroke = egui.Stroke(1.4, color)
    tip = P(center.x + dx * r, center.y + dy * r)
    painter.line_segment(P(center.x - dx * r, center.y - dy * r), tip, stroke)
    h = r * 0.7  # the head's sides, back from the tip and out to either side
    for side in (1, -1):
        painter.line_segment(tip, P(tip.x - dx * h - dy * h * side, tip.y - dy * h + dx * h * side), stroke)


def paint_keys(painter: egui.Painter, kit: Kit, x: float, center_y: float, keys: str, size: float = 11.5) -> float:
    """`keys` as caps from `x`, centered on `center_y`: "+" between a combination's,
    "/" between alternatives. Returns the x after them."""
    t = kit.theme
    top = center_y - CAP_HEIGHT / 2
    for a, combo in enumerate(parse(keys)):
        if a:
            x += JOIN_GAP
            painter.text(P(x, center_y - LIP / 2), egui.Align2.LEFT_CENTER, "/", font(size), t.text_muted)
            x += _width(painter, "/", size) + JOIN_GAP
        for c, label in enumerate(combo):
            if c:
                x += JOIN_GAP
                painter.text(P(x, center_y - LIP / 2), egui.Align2.LEFT_CENTER, "+", font(size), t.text_muted)
                x += _width(painter, "+", size) + JOIN_GAP
            w = cap_width(painter, label, size)
            paint_keycap(painter, kit, R(x, top, w, CAP_HEIGHT), label, size)
            x += w
    return x


def shortcut_width(painter: egui.Painter | None, shortcut: Shortcut, size: float = 11.5, label_size: float = 12.0) -> float:
    """One shortcut of a legend: its caps, then its label."""
    return keys_width(painter, shortcut.keys, size) + LABEL_GAP + _width(painter, shortcut.label, label_size)


def legend_lines(
    painter: egui.Painter | None, shortcuts: list[Shortcut], width: float, size: float = 11.5, label_size: float = 12.0
) -> list[list[Shortcut]]:
    """`shortcuts` broken into lines of at most `width` (a shortcut wider than a line
    gets one to itself)."""
    lines, line, used = [], [], 0.0
    for s in shortcuts:
        w = shortcut_width(painter, s, size, label_size)
        if line and used + ITEM_GAP + w > width:
            lines.append(line)
            line, used = [], 0.0
        used += (ITEM_GAP if line else 0.0) + w
        line.append(s)
    if line:
        lines.append(line)
    return lines


def legend_height(
    painter: egui.Painter | None,
    shortcuts: list[Shortcut],
    width: float,
    *,
    line_height: float = 26.0,
    size: float = 11.5,
    label_size: float = 12.0,
) -> float:
    """The height legend draws `shortcuts` in, `width` wide."""
    return len(legend_lines(painter, shortcuts, width, size, label_size)) * line_height


def legend(
    painter: egui.Painter,
    kit: Kit,
    x: float,
    y: float,
    width: float,
    shortcuts: list[Shortcut],
    *,
    line_height: float = 26.0,
    size: float = 11.5,
    label_size: float = 12.0,
) -> float:
    """Shortcuts in a row from (x, y), "caps label", wrapping at `width` (as a footer
    or hint bar). Returns the y below."""
    for line in legend_lines(painter, shortcuts, width, size, label_size):
        cx, cy = x, y + line_height / 2
        for s in line:
            cx = paint_keys(painter, kit, cx, cy, s.keys, size) + LABEL_GAP
            painter.text(P(cx, cy - LIP / 2), egui.Align2.LEFT_CENTER, s.label, font(label_size), kit.theme.text_muted)
            cx += _width(painter, s.label, label_size) + ITEM_GAP
        y += line_height
    return y


def shortcut_list(
    painter: egui.Painter,
    kit: Kit,
    x: float,
    y: float,
    width: float,
    shortcuts: list[Shortcut],
    *,
    keys_column: float | None = None,
    row_height: float = 30.0,
    size: float = 11.5,
    label_size: float = 13.0,
    dividers: bool = True,
) -> float:
    """A cheat sheet: one shortcut a row, its caps in a column (`keys_column` wide;
    default, the widest's) and what it does beside them. Returns the y below."""
    t = kit.theme
    if keys_column is None:
        keys_column = max((keys_width(painter, s.keys, size) for s in shortcuts), default=0.0)
    for i, s in enumerate(shortcuts):
        cy = y + row_height / 2
        if dividers and i:
            painter.line_segment(P(x, y), P(x + width, y), egui.Stroke(1.0, t.divider))
        paint_keys(painter, kit, x, cy, s.keys, size)
        painter.text(P(x + keys_column + 2 * LABEL_GAP, cy - LIP / 2), egui.Align2.LEFT_CENTER, s.label, font(label_size), t.text)
        y += row_height
    return y
