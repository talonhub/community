"""Tables: column layout, column headings (click to sort), and a virtualised row list.

  * `column_layout` places columns across a width: fixed ones, and flexible ones
    sharing the rest by weight.
  * `draw_header` draws the headings of a layout; sortable ones are UIA buttons
    ("Sort by <heading>") with a chevron on the sorted column. The caller paints the
    band behind them (so it can pin them above scrolled rows).
  * `draw_rows` is a scrolling list of equal-height rows that only lays out the rows
    in view; each row is a selectable UIA element, and the caller paints its cells.
"""

import egui

from .a11y import describe
from .geom import P
from .widgets import Kit


class Column:
    """A column: fixed `width`, or (width 0) a share of the rest by `weight`."""

    def __init__(self, key: str, heading: str, width: float = 0.0, weight: float = 1.0, align: str = "left", sortable: bool = False):
        self.key = key
        self.heading = heading
        self.width = width
        self.weight = weight
        self.align = align
        self.sortable = sortable


class Placed:
    """A column placed in a layout: x from the layout's start, and its width."""

    def __init__(self, column: Column, x: float, w: float):
        self.column = column
        self.key = column.key
        self.heading = column.heading
        self.x = x
        self.w = w


def column_layout(columns: list[Column], width: float, min_flex: float = 0.0) -> list[Placed]:
    """Place `columns` across `width`: fixed widths first; flexible columns share what
    is left (at least `min_flex`) by weight."""
    fixed = sum(c.width for c in columns if c.width)
    weights = sum(c.weight for c in columns if not c.width) or 1.0
    rest = max(width - fixed, min_flex)
    out, x = [], 0.0
    for c in columns:
        w = c.width or rest * c.weight / weights
        out.append(Placed(c, x, w))
        x += w
    return out


def paint_sort_chevron(painter: egui.Painter, center: egui.Pos2, descending: bool, color: egui.Color32, r: float = 3.5):
    """The sort direction as a small chevron (the font has no triangles)."""
    dy = r if descending else -r
    stroke = egui.Stroke(1.5, color)
    painter.line_segment(P(center.x - r, center.y - dy / 2), P(center.x, center.y + dy / 2), stroke)
    painter.line_segment(P(center.x, center.y + dy / 2), P(center.x + r, center.y - dy / 2), stroke)


def draw_header(
    ui: egui.Ui,
    kit: Kit,
    x: float,
    y: float,
    height: float,
    layout: list[Placed],
    *,
    sort: tuple | None = None,
    size: float = 13.0,
    color: egui.Color32 | None = None,
    pad: float = 6.0,
    key_prefix: str = "sort:",
) -> str | None:
    """Column headings in a band of `height` at (x, y). `sort` is (key, descending) of
    the sorted column. Returns the key of a sortable heading clicked this frame."""
    t = kit.theme
    painter = ui.painter()
    color = color or t.text_muted
    clicked = None
    for p in layout:
        if not p.heading:
            continue
        cell = egui.Rect.from_min_size(P(x + p.x, y), egui.Vec2(p.w, height))
        if p.column.sortable:
            response = kit.hit(ui, cell, key_prefix + p.key)
            describe(response, egui.WidgetType.Button, f"Sort by {p.heading}")
            if response.hovered():
                painter.rect_filled(cell, 4, t.surface_hover)
            if response.clicked():
                clicked = p.key
        if p.column.align == "right":
            text_rect = painter.text(P(cell.max.x - pad, cell.center().y), egui.Align2.RIGHT_CENTER, p.heading, egui.FontId.proportional(size), color)
        else:
            text_rect = painter.text(P(cell.min.x + pad, cell.center().y), egui.Align2.LEFT_CENTER, p.heading, egui.FontId.proportional(size), color)
        if sort is not None and sort[0] == p.key:
            paint_sort_chevron(painter, P(text_rect.max.x + 9, cell.center().y), sort[1], color)
    return clicked


class RowsResult:
    def __init__(self):
        # The row clicked (not on a control of its own), and one right-clicked, with
        # where: (index, egui.Pos2).
        self.clicked: int | None = None
        self.secondary: tuple | None = None


async def draw_rows(
    ui: egui.Ui,
    kit: Kit,
    rect: egui.Rect,
    count: int,
    *,
    row_h: float,
    salt: str,
    cell,
    row_name,
    selected: int | None = None,
    empty_text: str = "",
) -> RowsResult:
    """`count` rows of `row_h` in `rect`, scrolling, laid out only while in view. For
    each row in view: a selectable UIA element named `row_name(i)`, the selected or
    hovered fill and a divider, then `cell(ui, i, row_rect)` paints its content and
    returns True if a control of its own took the click."""
    t = kit.theme
    result = RowsResult()
    if not count:
        if empty_text:
            ui.painter().text(rect.center(), egui.Align2.CENTER_CENTER, empty_text, egui.FontId.proportional(14), t.text_muted)
        return result
    async with ui.allocate_new_ui(egui.UiBuilder().max_rect(rect)) as lui:
        async with lui.spacing_mut() as spacing:
            spacing.item_spacing = egui.Vec2(0, 0)
        async with egui.ScrollArea.vertical().id_salt(salt).auto_shrink(False).show_rows(row_h, count) as rows:
            rui = rows.ui
            for i in range(rows.row_start, rows.row_end):
                width = rui.available_width()
                row, resp = rui.allocate_exact_size(egui.Vec2(width, row_h), egui.Sense.click())
                describe(resp, egui.WidgetType.SelectableLabel, row_name(i), True, selected == i)
                painter = rui.painter()
                if selected == i:
                    painter.rect_filled(row, 0, t.selected_row)
                elif resp.hovered():
                    painter.rect_filled(row, 0, t.hover)
                painter.hline(row.min.x, row.max.x, row.max.y - 0.5, egui.Stroke(1.0, t.divider))
                consumed = cell(rui, i, row)
                if resp.clicked() and not consumed:
                    result.clicked = i
                if resp.secondary_clicked() and resp.interact_pointer_pos is not None:
                    result.secondary = (i, resp.interact_pointer_pos)
    return result
