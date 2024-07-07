from typing import Any, Callable, Optional, Sequence, Type

from talon import Module, app, cron, ctrl, settings, ui
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia.imagefilter import ImageFilter
from talon.types import Rect

mod = Module()


def setting(
    name: str, type: Type, desc: str, *, default: Optional[Any] = None
) -> Callable[[], type]:
    mod.setting(f"subtitles_{name}", type, default=default, desc=f"Subtitles: {desc}")
    return lambda: settings.get(f"user.subtitles_{name}")


setting_show = setting(
    "show",
    bool,
    "If true show (custom) subtitles",
    default=False,
)
setting_screens = setting(
    "screens",
    str,
    "Show on which screens: 'all', 'main', 'cursor', 'focus'",
)
setting_size = setting(
    "size",
    int,
    "Subtitle size in pixels",
)
setting_color = setting(
    "color",
    str,
    "Subtitle color",
)
setting_color_outline = setting(
    "color_outline",
    str,
    "Subtitle outline color",
)
setting_timeout_per_char = setting(
    "timeout_per_char",
    int,
    "For each character in the subtitle extend the timeout by this amount in ms",
)
setting_timeout_min = setting(
    "timeout_min",
    int,
    "Minimum time for a subtitle to show in ms",
)
setting_timeout_max = setting(
    "timeout_max",
    int,
    "Maximum time for a subtitle to show in ms",
)
setting_y = setting(
    "y",
    float,
    "Percentage of screen hight to show subtitle at. 0=top, 1=bottom",
)

mod = Module()
canvases: list[Canvas] = []


def show_subtitle(text: str):
    """Show subtitle"""
    if not setting_show():
        return
    clear_canvases()
    screens = get_screens()
    for screen in screens:
        canvas = show_text_on_screen(screen, text)
        canvases.append(canvas)


def get_screens() -> Sequence[ui.Screen]:
    screen = setting_screens()
    match screen:
        case "main":
            return [ui.main_screen()]
        case "all":
            return ui.screens()
        case "cursor":
            x, y = ctrl.mouse_pos()
            return [ui.screen_containing(x, y)]
        case "focus":
            return [ui.active_window().screen]
        case _:
            raise ValueError(f"Unknown screen setting: {screen}")


def show_text_on_screen(screen: ui.Screen, text: str):
    timeout = calculate_timeout(text)
    canvas = Canvas.from_screen(screen)
    canvas.register("draw", lambda c: on_draw(c, screen, text))
    canvas.freeze()
    cron.after(f"{timeout}ms", canvas.close)
    return canvas


def on_draw(c: SkiaCanvas, screen: ui.Screen, text: str):
    scale = screen.scale if app.platform != "mac" else 1
    size = setting_size() * scale
    rect = set_text_size_and_get_rect(c, size, text)
    x = c.rect.center.x - rect.center.x
    # Clamp coordinate to make sure entire text is visible
    y = max(
        min(
            c.rect.y + setting_y() * c.rect.height + c.paint.textsize / 2,
            c.rect.bot - rect.bot,
        ),
        c.rect.top - rect.top,
    )

    c.paint.imagefilter = ImageFilter.drop_shadow(2, 2, 1, 1, "000000")
    c.paint.style = c.paint.Style.FILL
    c.paint.color = setting_color()
    c.draw_text(text, x, y)

    # Outline
    c.paint.imagefilter = None
    c.paint.style = c.paint.Style.STROKE
    c.paint.color = setting_color_outline()
    c.draw_text(text, x, y)


def calculate_timeout(text: str) -> int:
    ms_per_char = setting_timeout_per_char()
    ms_min = setting_timeout_min()
    ms_max = setting_timeout_max()
    return min(ms_max, max(ms_min, len(text) * ms_per_char))


def set_text_size_and_get_rect(c: SkiaCanvas, size: int, text: str) -> Rect:
    while True:
        c.paint.textsize = size
        rect = c.paint.measure_text(text)[1]
        if rect.width < c.width * 0.8:
            return rect
        size *= 0.9


def clear_canvases():
    for canvas in canvases:
        canvas.close()
    canvases.clear()
