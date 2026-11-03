"""Measuring, eliding and wrapping text."""

import egui

from .geom import P

# Any colour does for measuring.
_MEASURE = egui.Color32.from_rgb(255, 255, 255)


def text_width(painter: egui.Painter, text: str, font_id: egui.FontId) -> float:
    return painter.layout_no_wrap(text, font_id, _MEASURE).size().x


def elide(painter: egui.Painter, text: str, font_id: egui.FontId, width: float) -> str:
    """`text`, cut short with "…" to fit `width` points (measured)."""
    if width <= 0:
        return ""
    if text_width(painter, text, font_id) <= width:
        return text
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if text_width(painter, text[:mid] + "…", font_id) <= width:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + "…"


def wrap(painter: egui.Painter, x: float, y: float, width: float, text: str, font_id: egui.FontId, color: egui.Color32) -> float:
    """Paint `text` wrapped to `width` at (x, y); returns the y below it."""
    galley = painter.layout(text, font_id, color, width)
    painter.galley(P(x, y), galley, color)
    return y + galley.size().y


def estimate_width(text: str, font_size: float) -> float:
    """Rough width of `text` in points, for sizing before there is a painter."""
    return len(text) * 0.55 * font_size


def elide_estimate(text: str, width_points: float, font_size: float) -> str:
    """`text` cut short with "…" by the estimate (no painter needed)."""
    max_chars = max(int(width_points / (0.55 * font_size)), 4)
    return text if len(text) <= max_chars else text[: max_chars - 1] + "…"
