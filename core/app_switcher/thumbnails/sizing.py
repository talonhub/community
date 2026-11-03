"""Sizing the switcher window for its contents: grid, app strip, list; fitting and
point/pixel conversion."""

import math
import egui
from ...egui_kit.text import estimate_width
from .config import (
    APPS_MIN_HEIGHT,
    APPS_MIN_WIDTH,
    APP_CELL,
    APP_MAX_COLUMNS,
    HEADER_HEIGHT,
    LABEL_HEIGHT,
    LIST_MAX_WIDTH_FRACTION,
    LIST_MIN_WIDTH,
    MAX_TILE_WIDTH_FRACTION,
    MIN_TILE_WIDTH,
    NUMBER_WIDTH,
    PADDING,
    ROW_GAP,
    ROW_HEIGHT,
    ROW_ICON,
    SCREEN_FILL,
    SEARCH_HEIGHT,
    TILE_ASPECT,
)


def choose_grid(count: int, work: tuple[int, int, int, int], ppp: float) -> tuple[int, int, int]:
    """Pick (columns, width, height) giving the biggest tiles that fit the screen.

    Tiles don't shrink below MIN_TILE_WIDTH; past that the grid is taller than the
    window and scrolls.
    """
    work_w = (work[2] - work[0]) * SCREEN_FILL
    work_h = (work[3] - work[1]) * SCREEN_FILL
    chrome_w = 2 * PADDING * ppp
    chrome_h = (HEADER_HEIGHT + SEARCH_HEIGHT + 2 * PADDING) * ppp
    label_h = (LABEL_HEIGHT + PADDING) * ppp
    max_tile_w = (work[2] - work[0]) * MAX_TILE_WIDTH_FRACTION
    min_tile_w = min(MIN_TILE_WIDTH * ppp, work_w - chrome_w)
    max_cols = max(int((work_w - chrome_w) // min_tile_w), 1)

    best = (0.0, 1)
    for cols in range(1, min(max(count, 1), max_cols) + 1):
        rows = math.ceil(count / cols)
        tile_w = min((work_w - chrome_w) / cols, max_tile_w)
        tile_h = tile_w / TILE_ASPECT + label_h
        if rows * tile_h > work_h - chrome_h:
            tile_h = (work_h - chrome_h) / rows
            tile_w = max(min(tile_w, (tile_h - label_h) * TILE_ASPECT), min_tile_w)
        # At the minimum size, more columns means less scrolling.
        if (tile_w, cols) > best:
            best = (tile_w, cols)

    tile_w, cols = best
    rows = math.ceil(count / cols)
    tile_h = tile_w / TILE_ASPECT + label_h
    width = int(cols * tile_w + chrome_w)
    height = int(min(rows * tile_h + chrome_h, work_h))
    return cols, width, height


def choose_apps(count: int, work: tuple[int, int, int, int], ppp: float) -> tuple[int, int, int]:
    """Pick (columns, width, height) for the apps view: a strip of icons, wrapping."""
    work_w = (work[2] - work[0]) * SCREEN_FILL
    work_h = (work[3] - work[1]) * SCREEN_FILL
    chrome_w = 2 * PADDING * ppp
    chrome_h = (HEADER_HEIGHT + SEARCH_HEIGHT + 2 * PADDING) * ppp
    cell = APP_CELL * ppp
    cols = max(1, min(count, APP_MAX_COLUMNS, int((work_w - chrome_w) // cell)))
    width = max(cols * cell + chrome_w, APPS_MIN_WIDTH * ppp)
    # Cells stretch to the width; rows are as tall as cells are wide.
    cell_w = (width - chrome_w) / cols
    rows = math.ceil(count / cols)
    height = min(max(rows * cell_w + chrome_h, APPS_MIN_HEIGHT * ppp), work_h)
    return cols, int(width), int(height)




def choose_list(entries: list["Entry"], work: tuple[int, int, int, int], ppp: float) -> tuple[int, int]:
    """Pick (width, height) for the list view: as wide as the longest row, up to a cap."""
    longest = max(
        (estimate_width(e.title, 14.0) + estimate_width(e.app_label(), 13.0) for e in entries),
        default=0.0,
    )
    row_w = 10 + NUMBER_WIDTH + ROW_ICON + 10 + longest + 24 + 10
    width = max(row_w + 3 * PADDING, LIST_MIN_WIDTH) * ppp
    width = min(width, (work[2] - work[0]) * LIST_MAX_WIDTH_FRACTION)
    height = (
        HEADER_HEIGHT + SEARCH_HEIGHT + 2 * PADDING + len(entries) * (ROW_HEIGHT + ROW_GAP)
    ) * ppp
    height = min(height, (work[3] - work[1]) * SCREEN_FILL)
    return int(width), int(height)


def fit(src_w: int, src_h: int, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Largest rectangle with the source's aspect ratio centered inside `box`."""
    left, top, right, bottom = box
    box_w, box_h = right - left, bottom - top
    if src_w <= 0 or src_h <= 0 or box_w <= 0 or box_h <= 0:
        return box
    scale = min(box_w / src_w, box_h / src_h)
    w, h = int(src_w * scale), int(src_h * scale)
    x = left + (box_w - w) // 2
    y = top + (box_h - h) // 2
    return (x, y, x + w, y + h)


def to_pixels(rect: egui.Rect, ppp: float) -> tuple[int, int, int, int]:
    """An egui rect in points as (left, top, right, bottom) physical pixels."""
    return (
        int(rect.min.x * ppp),
        int(rect.min.y * ppp),
        int(rect.max.x * ppp),
        int(rect.max.y * ppp),
    )
