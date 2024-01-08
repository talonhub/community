from talon import Module, app, registry, scope, skia, ui, settings
from talon.canvas import Canvas
from talon.screen import Screen
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia.imagefilter import ImageFilter
from talon.ui import Rect

canvas: Canvas = None
current_mode = ""
mod = Module()

setting_show = mod.setting(
    "mode_indicator_show",
    bool,
    desc="If true the mode indicator is shown",
    default=False,
)
setting_size = mod.setting(
    "mode_indicator_size",
    float,
    desc="Mode indicator diameter in pixels",
)
setting_x = mod.setting(
    "mode_indicator_x",
    float,
    desc="Mode indicator center X-position in percentages(0-1). 0=left, 1=right",
)
setting_y = mod.setting(
    "mode_indicator_y",
    float,
    desc="Mode indicator center Y-position in percentages(0-1). 0=top, 1=bottom",
)
setting_color_alpha = mod.setting(
    "mode_indicator_color_alpha",
    float,
    desc="Mode indicator alpha/opacity in percentages(0-1). 0=fully transparent, 1=fully opaque",
)
setting_color_gradient = mod.setting(
    "mode_indicator_color_gradient",
    float,
    desc="Mode indicator gradient brightness in percentages(0-1). 0=darkest, 1=brightest",
)
setting_color_sleep = mod.setting("mode_indicator_color_sleep", str)
setting_color_dictation = mod.setting("mode_indicator_color_dictation", str)
setting_color_mixed = mod.setting("mode_indicator_color_mixed", str)
setting_color_command = mod.setting("mode_indicator_color_command", str)
setting_color_other = mod.setting("mode_indicator_color_other", str)

setting_paths = {
    s.path
    for s in [
        setting_show,
        setting_size,
        setting_x,
        setting_y,
        setting_color_alpha,
        setting_color_gradient,
        setting_color_sleep,
        setting_color_dictation,
        setting_color_mixed,
        setting_color_command,
        setting_color_other,
    ]
}


def get_mode_color() -> str:
    if current_mode == "sleep":
        return settings.get("user.mode_indicator_color_sleep")
    elif current_mode == "dictation":
        return settings.get("user.mode_indicator_color_dictation")
    elif current_mode == "mixed":
        return settings.get("user.mode_indicator_color_mixed")
    elif current_mode == "command":
        return settings.get("user.mode_indicator_color_command")
    else:
        return settings.get("user.mode_indicator_color_other")


def get_alpha_color() -> str:
    alpha = settings.get("user.mode_indicator_color_alpha")
    return f"{int( * 255):02x}"


def get_gradient_color(color: str) -> str:
    factor = settings.get("user.mode_indicator_color_gradient")
    # hex -> rgb
    (r, g, b) = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
    # Darken rgb
    r, g, b = int(r * factor), int(g * factor), int(b * factor)
    # rgb -> hex
    return f"{r:02x}{g:02x}{b:02x}"


def get_colors():
    color_mode = get_mode_color()
    color_gradient = get_gradient_color(color_mode)
    color_alpha = get_alpha_color()
    return f"{color_mode}{color_alpha}", f"{color_gradient}"


def on_draw(c: SkiaCanvas):
    color_mode, color_gradient = get_colors()
    x, y = c.rect.center.x, c.rect.center.y
    radius = c.rect.height / 2 - 2

    c.paint.shader = skia.Shader.radial_gradient(
        (x, y), radius, [color_mode, color_gradient]
    )

    c.paint.imagefilter = ImageFilter.drop_shadow(1, 1, 1, 1, color_gradient)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = color_mode
    c.draw_circle(x, y, radius)


def move_indicator():
    screen: Screen = ui.main_screen()
    rect = screen.rect
    scale = screen.scale if app.platform != "mac" else 1
    radius = settings.get("user.mode_indicator_size") * scale / 2

    x = rect.left + min(
        max(settings.get("user.mode_indicator_x") * rect.width - radius, 0),
        rect.width - 2 * radius,
    )

    y = rect.top + min(
        max(settings.get("user.mode_indicator_y") * rect.height - radius, 0),
        rect.height - 2 * radius,
    )

    side = 2 * radius
    canvas.resize(side, side)
    canvas.move(x, y)


def show_indicator():
    global canvas
    canvas = Canvas.from_rect(Rect(0, 0, 0, 0))
    canvas.register("draw", on_draw)


def hide_indicator():
    global canvas
    canvas.unregister("draw", on_draw)
    canvas.close()
    canvas = None


def update_indicator():
    if settings.get("user.mode_indicator_show"):
        if not canvas:
            show_indicator()
        move_indicator()
        canvas.freeze()
    elif canvas:
        hide_indicator()


def on_update_contexts():
    global current_mode
    modes = scope.get("mode")
    if "sleep" in modes:
        mode = "sleep"
    elif "dictation" in modes:
        if "command" in modes:
            mode = "mixed"
        else:
            mode = "dictation"
    elif "command" in modes:
        mode = "command"
    else:
        mode = "other"

    if current_mode != mode:
        current_mode = mode
        update_indicator()


def on_update_settings(updated_settings: set[str]):
    if setting_paths & updated_settings:
        update_indicator()


def on_ready():
    registry.register("update_contexts", on_update_contexts)
    registry.register("update_settings", on_update_settings)
    ui.register("screen_change", lambda _: update_indicator)


app.register("ready", on_ready)
