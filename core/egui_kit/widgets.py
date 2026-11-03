"""Painted controls with accessibility nodes: buttons, toggles, chips, fields, lists.

Every control takes a `Kit` (its tool's id prefix and theme) and paints with the
theme's colours. Controls return what happened (clicked, flipped, removed); they never
run the caller's actions. Interactive ones get a UIA node (see a11y), so hinting tools
can find and invoke them.
"""

import egui

from .a11y import Ids, describe, name_text_edit
from .geom import P, R
from .text import elide, text_width, wrap
from .theme import THEME, Theme, font, mono


class Kit(Ids):
    """A tool's stable-id prefix and theme, passed to every control."""

    def __init__(self, prefix: str, theme: Theme = THEME):
        super().__init__(prefix)
        self.theme = theme


def text_size(painter: egui.Painter, text: str, font_id: egui.FontId) -> egui.Vec2:
    return painter.layout_no_wrap(text, font_id, THEME.white).size()


# --- layout helpers ---


def card(painter: egui.Painter, kit: Kit, rect: egui.Rect):
    t = kit.theme
    painter.rect(rect, t.radius_card, t.surface, egui.Stroke(1.0, t.border), egui.StrokeKind.Inside)


def section_label(painter: egui.Painter, kit: Kit, x: float, y: float, text: str):
    """A small upper-case label over a group of controls."""
    painter.text(P(x, y), egui.Align2.LEFT_TOP, text.upper(), font(11.5), kit.theme.text_label)


# --- buttons ---

BUTTON_KINDS = ("primary", "secondary", "outline", "pill")


def pill_size(painter: egui.Painter, label: str, size: float = 13.0, pad: float = 8.0, height: float | None = None) -> egui.Vec2:
    """The size of a "pill" button for `label`: the text plus `pad` each side; `height`
    or the text's plus 6."""
    s = text_size(painter, label, font(size))
    return egui.Vec2(s.x + 2 * pad, height if height is not None else s.y + 6)


def paint_button(
    painter: egui.Painter,
    kit: Kit,
    rect: egui.Rect,
    label: str,
    kind: str,
    hovered: bool,
    enabled: bool = True,
    active: bool = False,
    size: float | None = None,
):
    t = kit.theme
    if kind == "pill":
        # A toolbar button: surface fill and border; `active` (its dropdown is open) in
        # the chip colour.
        painter.rect_filled(rect, t.radius, t.chip_bg if active else t.surface_hover if hovered else t.surface)
        painter.rect_stroke(rect, t.radius, egui.Stroke(1.0, t.border), egui.StrokeKind.Inside)
        color = t.text if enabled else t.text_faint
        size = size or 13.0
    elif kind == "primary":
        painter.rect_filled(rect, t.radius, (t.accent_hover if hovered else t.accent) if enabled else t.accent_disabled)
        color = t.on_accent
        size = size or 14.0
    else:
        fill = t.hover if hovered and enabled else t.surface
        stroke = t.accent if kind == "outline" and enabled else t.input_border
        painter.rect(rect, t.radius, fill, egui.Stroke(1.0, stroke), egui.StrokeKind.Inside)
        color = (t.accent if kind == "outline" else t.text) if enabled else t.text_faint
        size = size or 14.0
    painter.text(rect.center(), egui.Align2.CENTER_CENTER, label, font(size), color)


def button(
    ui: egui.Ui,
    kit: Kit,
    rect: egui.Rect,
    label: str,
    kind: str = "secondary",
    *,
    enabled: bool = True,
    active: bool = False,
    key: str | None = None,
    name: str | None = None,
    tip: str | None = None,
    size: float | None = None,
) -> bool:
    """A push button; True when clicked (and enabled). `kind`: "primary", "secondary",
    "outline", or "pill" (a small toolbar button). `name` is its accessible name
    (default: the label); `key` its stable id (default: from the label)."""
    resp = kit.hit(ui, rect, key or "button:" + label)
    describe(resp, egui.WidgetType.Button, name if name is not None else label, enabled)
    if tip and resp.hovered():
        resp.on_hover_text(tip)
    paint_button(ui.painter(), kit, rect, label, kind, resp.hovered(), enabled, active, size)
    return enabled and resp.clicked()


# --- icons ---

GLYPHS = ("close", "remove", "pin", "unpin")


def paint_glyph(painter: egui.Painter, kit: Kit, rect: egui.Rect, glyph: str, hovered: bool, color: egui.Color32 | None = None):
    """A small vector icon in `rect`: "close"/"remove" (an x), "pin", "unpin" (a crossed
    out pin). Hovered: on a red (close, remove) or chip-coloured square, in white."""
    t = kit.theme
    if hovered:
        painter.rect_filled(rect, 4, t.danger if glyph in ("close", "remove") else t.chip_bg)
    color = t.white if hovered else (color or t.text)
    stroke = egui.Stroke(1.6, color)
    c = rect.center()
    if glyph in ("close", "remove"):
        r = rect.width() * 0.22
        painter.line_segment(P(c.x - r, c.y - r), P(c.x + r, c.y + r), stroke)
        painter.line_segment(P(c.x - r, c.y + r), P(c.x + r, c.y - r), stroke)
        return
    # A pushpin: round head, a bar, and the needle.
    painter.circle_filled(P(c.x, c.y - 4), 3.2, color)
    painter.line_segment(P(c.x - 4, c.y), P(c.x + 4, c.y), stroke)
    painter.line_segment(P(c.x, c.y), P(c.x, c.y + 6), stroke)
    if glyph == "unpin":
        painter.line_segment(P(c.x - 6, c.y + 6), P(c.x + 6, c.y - 7), egui.Stroke(1.8, t.danger if not hovered else t.white))


def icon_button(ui: egui.Ui, kit: Kit, rect: egui.Rect, glyph: str, *, name: str, key: str, tip: str | None = None) -> bool:
    """A glyph button (see paint_glyph); True when clicked."""
    resp = kit.hit(ui, rect, key)
    describe(resp, egui.WidgetType.Button, name)
    if tip and resp.hovered():
        resp.on_hover_text(tip)
    paint_glyph(ui.painter(), kit, rect, glyph, resp.hovered())
    return resp.clicked()


def paint_x(painter: egui.Painter, center: egui.Pos2, radius: float, color: egui.Color32, width: float = 1.4):
    """A plain x (no background)."""
    stroke = egui.Stroke(width, color)
    painter.line_segment(P(center.x - radius, center.y - radius), P(center.x + radius, center.y + radius), stroke)
    painter.line_segment(P(center.x - radius, center.y + radius), P(center.x + radius, center.y - radius), stroke)


def paint_check(painter: egui.Painter, kit: Kit, center: egui.Pos2, radius: float = 7.0):
    """A multi-select mark: a tick on a filled circle."""
    t = kit.theme
    painter.circle_filled(center, radius, t.mark)
    stroke = egui.Stroke(1.8, t.white)
    a = P(center.x - radius * 0.5, center.y)
    b = P(center.x - radius * 0.12, center.y + radius * 0.4)
    c = P(center.x + radius * 0.5, center.y - radius * 0.38)
    painter.line_segment(a, b, stroke)
    painter.line_segment(b, c, stroke)


# --- toggles ---


def paint_toggle(painter: egui.Painter, kit: Kit, rect: egui.Rect, on: bool, enabled: bool = True):
    t = kit.theme
    track = (t.accent if on else t.track_off) if enabled else t.divider
    painter.rect_filled(rect, rect.height() / 2, track)
    r = rect.height() / 2 - 3
    cx = rect.max.x - r - 3 if on else rect.min.x + r + 3
    # Disabled: a dim knob, so it doesn't read as "off".
    painter.circle_filled(P(cx, rect.center().y), r, t.white if enabled else t.text_off)


def toggle(
    ui: egui.Ui, kit: Kit, rect: egui.Rect, on: bool, *, name: str, key: str, hit_rect: egui.Rect | None = None, enabled: bool = True
) -> bool:
    """An on/off switch (a UIA checkbox); True when clicked, i.e. to be flipped.
    `hit_rect` (default `rect`) is the clickable area."""
    resp = kit.hit(ui, hit_rect or rect, key)
    describe(resp, egui.WidgetType.Checkbox, name, enabled, on)
    paint_toggle(ui.painter(), kit, rect, on, enabled)
    return enabled and resp.clicked()


def setting_row(ui: egui.Ui, kit: Kit, x: float, y: float, w: float, title: str, description: str, on: bool, *, key: str, name: str | None = None) -> bool:
    """A titled, described on/off setting, the switch at the right; True when clicked.
    Takes 56 points."""
    t = kit.theme
    painter = ui.painter()
    painter.text(P(x, y), egui.Align2.LEFT_TOP, title, font(14), t.text)
    painter.text(P(x, y + 22), egui.Align2.LEFT_TOP, description, font(13), t.text_muted)
    rect = R(x + w - 40 - 4, y + 8, 40 + 4, 22 + 4)
    return toggle(ui, kit, rect, on, name=name or title, key=key)


# --- chips ---

CHIP_VARIANTS = ("accent", "auto", "warn")


def _chip_colors(kit: Kit, variant: str):
    """(fill, text, border or None, remove-hover fill)."""
    t = kit.theme
    if variant == "auto":
        return t.auto_chip_bg, t.text_muted, t.auto_chip_border, t.hover
    if variant == "warn":
        return t.warn_bg, t.warn_text, None, t.warn_hover
    return t.chip_bg, t.chip_text, None, t.chip_hover


def paint_chip(painter: egui.Painter, kit: Kit, rect: egui.Rect, text: str, variant: str = "accent", size: float = 12.5, radius: float | None = None):
    """A chip with its text centered: "accent" (a value), "auto" (a generated one,
    outlined), "warn" (a clash)."""
    fill, color, border, _ = _chip_colors(kit, variant)
    radius = kit.theme.radius if radius is None else radius
    if border is not None:
        painter.rect(rect, radius, fill, egui.Stroke(1.0, border), egui.StrokeKind.Inside)
    else:
        painter.rect_filled(rect, radius, fill)
    painter.text(rect.center(), egui.Align2.CENTER_CENTER, text, font(size), color)


def removable_chip(
    ui: egui.Ui,
    kit: Kit,
    rect: egui.Rect,
    text: str,
    *,
    key: str,
    variant: str = "accent",
    size: float = 13.5,
    radius: float | None = None,
    pad: float = 12,
    remove_w: float = 28,
    name: str | None = None,
) -> bool:
    """A chip with an x at its right end; True when the x is clicked."""
    fill, color, border, hover = _chip_colors(kit, variant)
    radius = kit.theme.radius if radius is None else radius
    painter = ui.painter()
    close = R(rect.max.x - remove_w, rect.min.y, remove_w, rect.height())
    resp = kit.hit(ui, close, key)
    describe(resp, egui.WidgetType.Button, name or f"Remove {text}")
    if border is not None:
        painter.rect(rect, radius, fill, egui.Stroke(1.0, border), egui.StrokeKind.Inside)
    else:
        painter.rect_filled(rect, radius, fill)
    if resp.hovered():
        painter.rect_filled(close, radius, hover)
    painter.text(P(rect.min.x + pad, rect.center().y), egui.Align2.LEFT_CENTER, text, font(size), color)
    paint_x(painter, close.center(), 4.0, color)
    return resp.clicked()


class Chip:
    """One chip of a chip_flow: its text, variant, and (removable) its stable key."""

    def __init__(self, text: str, variant: str = "accent", remove_key: str | None = None):
        self.text = text
        self.variant = variant
        self.remove_key = remove_key


def chip_flow(
    ui: egui.Ui,
    kit: Kit,
    x: float,
    y: float,
    right: float,
    chips: list[Chip],
    *,
    height: float = 22,
    size: float = 12.5,
    radius: float | None = None,
    pad: float = 8,
    gap: float = 6,
    wrap_lines: bool = True,
    line_gap: float = 6,
) -> tuple[int | None, float]:
    """Chips left to right from (x, y), each `height` tall. With `wrap_lines`, onto new
    lines below at `right`; without, an "…" where they no longer fit (the chips then
    centered on y). Returns (the index of a chip whose x was clicked, or None; the top
    of the last line)."""
    painter = ui.painter()
    removed = None
    cx = x
    top = y if wrap_lines else y - height / 2
    for i, c in enumerate(chips):
        tw = text_width(painter, c.text, font(size))
        w = pad + tw + 28 if c.remove_key else tw + 2 * pad
        if not wrap_lines and cx + w > right:
            painter.text(P(cx, y), egui.Align2.LEFT_CENTER, "…", font(13), kit.theme.text_muted)
            break
        if wrap_lines and cx + w > right and cx > x:
            cx = x
            top += height + line_gap
        rect = R(cx, top, w, height)
        if c.remove_key:
            if removable_chip(ui, kit, rect, c.text, key=c.remove_key, variant=c.variant, size=size, radius=radius, pad=pad) and removed is None:
                removed = i
        else:
            paint_chip(painter, kit, rect, c.text, c.variant, size, radius)
        cx += w + gap
    return removed, top


# --- text fields and choices ---


async def text_field(
    ui: egui.Ui, kit: Kit, rect: egui.Rect, value: "egui.Mutable", *, hint: str, name: str, size: float = 14, pad: egui.Vec2 | None = None
):
    """A framed single-line text field bound to `value` (an egui.Mutable made once and
    kept). Returns egui's TextEditOutput (`.response` for focus, changes, Enter)."""
    t = kit.theme
    painter = ui.painter()
    pad = pad or egui.Vec2(10, 8)
    painter.rect(rect, t.radius, t.surface, egui.Stroke(1.0, t.input_border), egui.StrokeKind.Inside)
    async with ui.allocate_new_ui(egui.UiBuilder().max_rect(rect.shrink2(pad))) as fui:
        out = (
            egui.TextEdit.singleline(value)
            .hint_text(hint)
            .frame(egui.Frame.none())
            .desired_width(rect.width() - 2 * pad.x)
            .font_id(font(size))
            .text_color(t.text)
            .show(fui)
        )
    name_text_edit(out.response, name, value.get(), hint)
    return out


NO_CHANGE = object()


async def combo(
    ui: egui.Ui,
    kit: Kit,
    rect: egui.Rect,
    *,
    salt: str,
    name: str,
    selected_text: str,
    options: list[tuple],
    selected,
    size: float = 14,
    popup_height: float = 480,
):
    """A drop-down choice. `options` are (key, text); returns the key picked this frame,
    or NO_CHANGE. Its UIA name is "<name>: <selected text>"."""
    picked = NO_CHANGE
    w = rect.width()
    async with ui.allocate_new_ui(egui.UiBuilder().max_rect(rect)) as cui:
        async with cui.spacing_mut() as spacing:
            spacing.interact_size = egui.Vec2(w, rect.height() - 4)
        async with (
            egui.ComboBox.from_id_salt(salt).selected_text(egui.RichText(selected_text).size(size)).width(w).height(popup_height).show()
        ) as box:
            if box.shown:
                pui = box.ui
                for key, text in options:
                    if pui.selectable_label(selected == key, egui.RichText(text).size(size)).clicked():
                        picked = key
        try:
            resp = box.response() if callable(box.response) else box.response
            describe(resp, egui.WidgetType.ComboBox, f"{name}: {selected_text}")
        except Exception as e:
            print(f"egui_kit: naming a combo box failed: {e!r}")
    return picked


def nav_list(
    ui: egui.Ui, kit: Kit, x: float, y: float, w: float, items: list[tuple], selected, *, row_h: float = 36, gap: float = 2
) -> tuple:
    """A list of choices with counts, one selected (a sidebar filter). `items` are
    (key, label, count). Returns (the key clicked, or None; the y below the list)."""
    t = kit.theme
    painter = ui.painter()
    clicked = None
    for key, label, count in items:
        rect = R(x, y, w, row_h)
        on = selected == key
        resp = kit.hit(ui, rect, "filter:" + label)
        describe(resp, egui.WidgetType.SelectableLabel, f"{label} ({count})", True, on)
        if on:
            painter.rect_filled(rect, t.radius, t.selected_nav)
        elif resp.hovered():
            painter.rect_filled(rect, t.radius, t.hover)
        width = rect.width() - 24 - 40
        painter.text(P(rect.min.x + 12, rect.center().y), egui.Align2.LEFT_CENTER, elide(painter, label, font(14), width), font(14), t.text)
        painter.text(P(rect.max.x - 12, rect.center().y), egui.Align2.RIGHT_CENTER, str(count), font(13), t.text_muted)
        if resp.clicked():
            clicked = key
        y += row_h + gap
    return clicked, y


def key_values(
    painter: egui.Painter, kit: Kit, x: float, y: float, w: float, rows: list[tuple], *, label_w: float = 88, gap: float = 10, mono_values: bool = True
) -> float:
    """Label/value lines, values wrapped (monospace by default); returns the y below."""
    t = kit.theme
    for label, value in rows:
        painter.text(P(x, y), egui.Align2.LEFT_TOP, label, font(12.5), t.text_muted)
        y = wrap(painter, x + label_w, y, w - label_w, str(value), mono(12) if mono_values else font(12.5), t.text)
        y += gap
    return y


# --- badges ---


def badges(painter: egui.Painter, kit: Kit, items: list[tuple], right: float, center_y: float, size: float = 12.0) -> float:
    """Small rounded labels, each (text, fill colour), laid right to left ending at
    `right`, in white text. Returns where they start."""
    font_id = font(size)
    for text, color in items:
        galley = painter.layout_no_wrap(text, font_id, kit.theme.white)
        s = galley.size()
        pill = egui.Rect.from_min_size(P(right - s.x - 12, center_y - s.y / 2 - 2), egui.Vec2(s.x + 12, s.y + 4))
        painter.rect_filled(pill, pill.height() / 2, color)
        painter.galley(P(pill.min.x + 6, pill.min.y + 2), galley, kit.theme.white)
        right = pill.min.x - 6
    return right


# --- a row of pill buttons (toolbars, header bars) ---


class Pill:
    """One button of a pill_row: its stable `key`, `label`, accessible `name` (default:
    the label), hover `tip`, and `active` (its dropdown is open)."""

    def __init__(self, key: str, label: str, name: str | None = None, tip: str | None = None, active: bool = False):
        self.key = key
        self.label = label
        self.name = name
        self.tip = tip
        self.active = active


def pill_row(
    ui: egui.Ui,
    kit: Kit,
    x: float,
    center_y: float,
    pills: list[Pill],
    *,
    align: str = "left",
    limit: float | None = None,
    height: float | None = None,
    size: float = 13.0,
    gap: float = 6.0,
) -> tuple:
    """Pill buttons in a row centered on `center_y`: from `x` rightwards (align
    "left"; stopping before one would pass `limit`), or from `x` leftwards (align
    "right", the first pill rightmost). Returns (the key clicked this frame or None;
    {key: rect} of the pills drawn; the x after the last one, past its gap)."""
    painter = ui.painter()
    clicked, rects = None, {}
    for p in pills:
        s = pill_size(painter, p.label, size, height=height)
        left = x if align == "left" else x - s.x
        rect = egui.Rect.from_min_size(P(left, center_y - s.y / 2), s)
        if align == "left" and limit is not None and rect.max.x > limit:
            break
        rects[p.key] = rect
        if button(ui, kit, rect, p.label, "pill", key=p.key, name=p.name, tip=p.tip, active=p.active, size=size):
            clicked = p.key
        x = rect.max.x + gap if align == "left" else rect.min.x - gap
    return clicked, rects, x
