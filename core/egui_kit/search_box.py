"""A painted search field for tools that take the typing themselves (keys arrive via
egui's input events, not an egui TextEdit): the query, a caret, a hint when empty,
and an optional filter chip in front that a click removes."""

import egui

from .geom import P
from .widgets import Kit


def search_box(
    ui: egui.Ui,
    kit: Kit,
    rect: egui.Rect,
    query: str,
    hint: str,
    *,
    chip_text: str | None = None,
    chip_name: str | None = None,
    name: str = "Search",
    key: str = "search",
    size: float = 15.0,
) -> bool:
    """Draw the field; True when its chip ("<chip_text>  ×") was clicked. Its UIA node
    is an edit named `name` holding the query; the chip is a button named `chip_name`."""
    t = kit.theme
    painter = ui.painter()
    # Painted, not an egui TextEdit, so it gets its accessibility node here.
    try:
        info = egui.WidgetInfo.text_edit(True, query, query, name)
        info.label = name
        kit.hit(ui, rect, key).widget_info(info)
    except Exception as e:
        print(f"egui_kit: naming the search field failed: {e!r}")
    painter.rect_filled(rect, t.radius, t.surface)
    painter.rect_stroke(rect, t.radius, egui.Stroke(1.5, t.accent), egui.StrokeKind.Inside)
    center_y = rect.center().y
    font = egui.FontId.proportional(size)
    x = rect.min.x + 8
    removed = False
    if chip_text is not None:
        galley = painter.layout_no_wrap(f"{chip_text}  ×", font, t.white)
        s = galley.size()
        pill = egui.Rect.from_min_size(P(x, center_y - s.y / 2 - 3), egui.Vec2(s.x + 16, s.y + 6))
        response = kit.hit(ui, pill, "chip")
        try:
            info = egui.WidgetInfo.labeled(egui.WidgetType.Button, True, chip_name or f"Remove {chip_text}")
            response.widget_info(info)
        except Exception as e:
            print(f"egui_kit: naming the search chip failed: {e!r}")
        painter.rect_filled(pill, pill.height() / 2, t.surface_hover if response.hovered() else t.chip_bg)
        painter.galley(P(pill.min.x + 8, pill.min.y + 3), galley, t.white)
        removed = response.clicked()
        x = pill.max.x + 8
    if query:
        text_rect = painter.text(P(x, center_y), egui.Align2.LEFT_CENTER, query, font, t.text)
        caret_x = text_rect.max.x + 2
    else:
        painter.text(P(x + 4, center_y), egui.Align2.LEFT_CENTER, hint, font, t.text_muted)
        caret_x = x + 1
    painter.vline(caret_x, center_y - 9, center_y + 9, egui.Stroke(1.5, t.text))
    return removed
