"""Scrolling grids of selectable cells (tiles, list rows, details rows), and an A-Z
index strip.

  * `grid_layout` places cells in columns; each section starts a new row under its
    heading.
  * `Grid` is one frame's geometry: where each cell is at a scroll offset, how far
    the content scrolls, scrolling a cell into view or to the top, section headings and
    the scrollbar.
  * `cell_interact` is a cell's interaction: a selectable UIA element (and an optional
    close button of its own) and hover; `paint_cell` its fill and outline for selected,
    marked (multi-select) and hovered cells. The tool paints the content.
  * `index_strip` is a column of letters to jump by.
"""

import egui

from .a11y import describe
from .geom import P
from .widgets import Kit


def grid_layout(count: int, cols: int, sections: list) -> list[tuple[int, int, int]]:
    """Each cell's (column, row, section headings above it). `sections` are (first
    cell, heading); each starts on a new row; without sections, cells simply wrap."""
    starts = {first: n for n, (first, _heading) in enumerate(sections)}
    layout, row, col, section = [], 0, 0, -1
    for i in range(count):
        if i in starts:
            if col > 0:
                row += 1
            col, section = 0, starts[i]
        elif col == cols:
            row, col = row + 1, 0
        layout.append((col, row, section + 1))
        col += 1
    return layout


class Grid:
    """One frame's geometry of a grid of `len(layout)` cells in `viewport`."""

    def __init__(
        self, viewport: egui.Rect, cols: int, cell_w: float, cell_h: float, gap: float, layout: list, *, padding: float = 8.0, section_h: float = 28.0
    ):
        self.viewport = viewport
        self.cols = cols
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.gap = gap
        self.layout = layout
        self.padding = padding
        self.section_h = section_h
        n = len(layout)
        self.content_h = padding + (self.top(n - 1) + cell_h if n else 0)
        self.max_scroll = max(self.content_h - viewport.height(), 0.0)
        # Rows a page (PageUp/PageDown) moves.
        self.page_rows = max(1, int(viewport.height() // max(cell_h, 1)) - 1)

    def top(self, i: int) -> float:
        """Cell `i`'s top within the scrolled content."""
        _col, row, headings = self.layout[i]
        return row * self.cell_h + headings * self.section_h

    def rect(self, i: int, scroll: float) -> egui.Rect:
        col = self.layout[i][0]
        vp = self.viewport
        return egui.Rect.from_min_size(
            P(vp.min.x + self.padding + col * self.cell_w, vp.min.y + self.padding + self.top(i) - scroll),
            egui.Vec2(self.cell_w - self.padding, self.cell_h - self.gap),
        )

    def scroll(self, scroll: float, wheel: float = 0.0, *, jump_to: int | None = None, reveal: int | None = None) -> float:
        """The next scroll offset: moved by the wheel; with `jump_to`, that cell's row at
        the top; with `reveal`, just enough to show that cell (with its heading)."""
        n = len(self.layout)
        scroll = scroll - wheel
        if jump_to is not None and 0 <= jump_to < n:
            scroll = self.top(jump_to) - self.padding / 2
        elif reveal is not None and 0 <= reveal < n:
            top = self.top(reveal) - (self.section_h if self.layout[reveal][2] else 0)
            bottom = top + self.cell_h + self.padding
            if top < scroll:
                scroll = top
            elif bottom > scroll + self.viewport.height():
                scroll = bottom - self.viewport.height()
        return max(0.0, min(scroll, self.max_scroll))

    def section_headings(self, painter: egui.Painter, kit: Kit, sections: list, scroll: float, size: float = 15.0):
        vp = self.viewport
        for first, label in sections:
            y = vp.min.y + self.padding + self.top(first) - self.section_h / 2 - scroll
            if vp.min.y - self.section_h < y < vp.max.y:
                painter.text(P(vp.min.x + self.padding + 4, y), egui.Align2.LEFT_CENTER, label, egui.FontId.proportional(size), kit.theme.text_muted)

    def scrollbar(self, painter: egui.Painter, kit: Kit, scroll: float, width: float = 4.0):
        """A thin scroll position bar along the right edge, when the content scrolls."""
        if self.max_scroll <= 0:
            return
        vp = self.viewport
        track = egui.Rect.from_min_max(
            P(vp.max.x - self.padding / 2 - width / 2, vp.min.y + self.padding),
            P(vp.max.x - self.padding / 2 + width / 2, vp.max.y - self.padding),
        )
        bar_h = max(track.height() * vp.height() / self.content_h, 20.0)
        bar_top = track.min.y + (track.height() - bar_h) * scroll / self.max_scroll
        painter.rect_filled(egui.Rect.from_min_size(P(track.min.x, bar_top), egui.Vec2(width, bar_h)), 2, kit.theme.border)


class CellResult:
    def __init__(self, response, hovered: bool, close_hovered: bool, close_response):
        # The cell's egui response (clicks, secondary clicks, tooltips).
        self.response = response
        # Over the cell but not its close button; over the close button.
        self.hovered = hovered
        self.close_hovered = close_hovered
        self.close_response = close_response

    def close_clicked(self) -> bool:
        return (self.close_hovered and self.response.clicked()) or (self.close_response is not None and self.close_response.clicked())


def cell_interact(
    ui: egui.Ui,
    kit: Kit,
    rect: egui.Rect,
    viewport: egui.Rect,
    *,
    key: str,
    name: str,
    selected: bool,
    close_rect: egui.Rect | None = None,
    close_name: str | None = None,
    pointer=None,
) -> CellResult:
    """A cell's UIA element ("tile:<key>", named `name`, selected or not), clipped to
    the viewport. With `close_rect`, a close button of its own ("tile-close:<key>")
    comes first, so it's its own UIA element while the pointer decides between them
    for the mouse. Then paint the frame (paint_cell), the content, and the close glyph
    (widgets.paint_glyph)."""
    close_response = None
    if close_rect is not None:
        close_response = kit.hit(ui, close_rect, f"tile-close:{key}")
        describe(close_response, egui.WidgetType.Button, close_name or "Close")
    response = kit.hit(ui, rect.intersect(viewport), f"tile:{key}")
    describe(response, egui.WidgetType.SelectableLabel, name, True, selected)
    close_hovered = close_rect is not None and response.hovered() and pointer is not None and close_rect.contains(pointer)
    hovered = response.hovered() and not close_hovered
    return CellResult(response, hovered, close_hovered, close_response)


def paint_cell(
    painter: egui.Painter, kit: Kit, rect: egui.Rect, *, selected: bool, marked: bool = False, hovered: bool = False, radius: float | None = None, selected_width: float = 3.0
):
    """A cell's fill and outline: marked (multi-select), hovered or plain; outlined when
    selected, marked, or else thinly."""
    t = kit.theme
    radius = t.radius if radius is None else radius
    painter.rect_filled(rect, radius, t.mark_fill if marked else t.surface_hover if hovered else t.surface)
    if selected:
        painter.rect_stroke(rect, radius, egui.Stroke(selected_width, t.accent), egui.StrokeKind.Inside)
    elif marked:
        painter.rect_stroke(rect, radius, egui.Stroke(2.0, t.mark), egui.StrokeKind.Inside)
    else:
        painter.rect_stroke(rect, radius, egui.Stroke(1.0, t.border), egui.StrokeKind.Inside)


def index_strip(
    ui: egui.Ui,
    kit: Kit,
    x: float,
    top: float,
    height: float,
    letters: str,
    available: set,
    current: str | None = None,
    *,
    width: float = 22.0,
    max_row: float = 22.0,
    size: float = 12.0,
) -> str | None:
    """A column of `letters` centered on `x`, from `top` within `height`: the
    `available` ones are buttons ("Jump to <letter>"), `current` highlighted.
    Returns a letter clicked this frame."""
    t = kit.theme
    painter = ui.painter()
    row = min(max_row, height / len(letters))
    clicked = None
    font = egui.FontId.proportional(size)
    for n, letter in enumerate(letters):
        rect = egui.Rect.from_center_size(P(x, top + (n + 0.5) * row), egui.Vec2(width, row))
        if letter in available:
            response = kit.hit(ui, rect, "letter:" + letter)
            describe(response, egui.WidgetType.Button, f"Jump to {letter}")
            if response.hovered():
                painter.rect_filled(rect, 4, t.surface_hover)
            if response.clicked():
                clicked = letter
            color = t.accent if letter == current else t.text
        else:
            color = t.text_off
        painter.text(rect.center(), egui.Align2.CENTER_CENTER, letter, font, color)
    return clicked
