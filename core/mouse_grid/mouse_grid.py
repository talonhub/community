# courtesy of https://github.com/timo/
# see https://github.com/timo/talon_scripts
import math
from typing import Union

from talon import Context, Module, actions, canvas, cron, ctrl, screen, settings, ui
from talon.skia import Paint, Rect
from talon.types.point import Point2d

mod = Module()
mod.setting(
    "grid_narrow_expansion",
    type=int,
    default=0,
    desc="""After narrowing, grow the new region by this many pixels in every direction, to make things immediately on edges easier to hit, and when the grid is at its smallest, it allows you to still nudge it around""",
)
mod.setting(
    "grids_put_one_bottom_left",
    type=bool,
    default=False,
    desc="""Allows you to switch mouse grid and friends between a computer numpad and a phone numpad (the number one goes on the bottom left or the top left)""",
)
mod.setting(
    "grid_show_zoomed",
    type=bool,
    default=True,
    desc="If true, show a zoomed in version of the mouse grid when it becomes sufficiently small",
)

mod.tag("mouse_grid_showing", desc="Tag indicates whether the mouse grid is showing")
ctx = Context()


class MouseSnapNine:
    def __init__(self):
        user.screen = None
        user.rect = None
        user.history = []
        user.img = None
        user.mcanvas = None
        user.active = False
        user.count = 0
        user.was_zoom_mouse_active = False
        user.was_control_mouse_active = False
        user.was_control1_mouse_active = False

    def setup(self, *, rect: Rect = None, screen_num: int = None):
        screens = ui.screens()
        # each if block here might set the rect to None to indicate failure
        if rect is not None:
            try:
                screen = ui.screen_containing(*rect.center)
            except Exception:
                rect = None
        if rect is None and screen_num is not None:
            screen = screens[screen_num % len(screens)]
            rect = screen.rect
        if rect is None:
            screen = screens[0]
            rect = screen.rect
        user.rect = rect.copy()
        user.screen = screen
        user.count = 0
        user.img = None
        if user.mcanvas is not None:
            user.mcanvas.close()
        user.mcanvas = canvas.Canvas.from_screen(screen)
        if user.active:
            user.mcanvas.register("draw", user.draw)
            user.mcanvas.freeze()

    def show(self):
        if user.active:
            return
        # noinspection PyUnresolvedReferences
        if actions.tracking.control_zoom_enabled():
            user.was_zoom_mouse_active = True
            actions.tracking.control_zoom_toggle(False)
        if actions.tracking.control_enabled():
            user.was_control_mouse_active = True
            actions.tracking.control_toggle(False)
        if actions.tracking.control1_enabled():
            user.was_control1_mouse_active = True
            actions.tracking.control1_toggle(False)
        user.mcanvas.register("draw", user.draw)
        user.mcanvas.freeze()
        user.active = True
        return

    def close(self):
        if not user.active:
            return
        user.mcanvas.unregister("draw", user.draw)
        user.mcanvas.close()
        user.mcanvas = None
        user.img = None

        user.active = False

        if user.was_control_mouse_active and not actions.tracking.control_enabled():
            actions.tracking.control_toggle(True)
        if user.was_control1_mouse_active and not actions.tracking.control1_enabled():
            actions.tracking.control1_toggle(True)
        if user.was_zoom_mouse_active and not actions.tracking.control_zoom_enabled():
            actions.tracking.control_zoom_toggle(True)

        user.was_zoom_mouse_active = False
        user.was_control_mouse_active = False
        user.was_control1_mouse_active = False

    def draw(self, canvas):
        paint = canvas.paint

        def draw_grid(offset_x, offset_y, width, height):
            canvas.draw_line(
                offset_x + width // 3,
                offset_y,
                offset_x + width // 3,
                offset_y + height,
            )
            canvas.draw_line(
                offset_x + 2 * width // 3,
                offset_y,
                offset_x + 2 * width // 3,
                offset_y + height,
            )

            canvas.draw_line(
                offset_x,
                offset_y + height // 3,
                offset_x + width,
                offset_y + height // 3,
            )
            canvas.draw_line(
                offset_x,
                offset_y + 2 * height // 3,
                offset_x + width,
                offset_y + 2 * height // 3,
            )

        def draw_crosses(offset_x, offset_y, width, height):
            for row in range(0, 2):
                for col in range(0, 2):
                    cx = offset_x + width / 6 + (col + 0.5) * width / 3
                    cy = offset_y + height / 6 + (row + 0.5) * height / 3

                    canvas.draw_line(cx - 10, cy, cx + 10, cy)
                    canvas.draw_line(cx, cy - 10, cx, cy + 10)

        grid_stroke = 1

        def draw_text(offset_x, offset_y, width, height):
            canvas.paint.text_align = canvas.paint.TextAlign.CENTER
            for row in range(3):
                for col in range(3):
                    text_string = ""
                    if settings.get("user.grids_put_one_bottom_left"):
                        text_string = f"{(2 - row) * 3 + col + 1}"
                    else:
                        text_string = f"{row * 3 + col + 1}"
                    text_rect = canvas.paint.measure_text(text_string)[1]
                    background_rect = text_rect.copy()
                    background_rect.center = Point2d(
                        offset_x + width / 6 + col * width / 3,
                        offset_y + height / 6 + row * height / 3,
                    )
                    background_rect = background_rect.inset(-4)
                    paint.color = "9999995f"
                    paint.style = Paint.Style.FILL
                    canvas.draw_rect(background_rect)
                    paint.color = "00ff00ff"
                    canvas.draw_text(
                        text_string,
                        offset_x + width / 6 + col * width / 3,
                        offset_y + height / 6 + row * height / 3 + text_rect.height / 2,
                    )

        should_show_zoomed_in = user.should_show_zoomed_in()
        if not should_show_zoomed_in:
            paint.color = "00ff007f"
            for which in range(1, 10):
                draw_crosses(*user.calc_narrow(which, user.rect))

        paint.stroke_width = grid_stroke
        if user.active:
            paint.color = "ff0000ff"
        else:
            paint.color = "000000ff"
        if should_show_zoomed_in:
            aspect = user.rect.width / user.rect.height
            if aspect >= 1:
                w = user.screen.width / 3
                h = w / aspect
            else:
                h = user.screen.height / 3
                w = h * aspect
            x = user.screen.x + (user.screen.width - w) / 2
            y = user.screen.y + (user.screen.height - h) / 2
            user.draw_zoom(canvas, x, y, w, h)
            draw_grid(x, y, w, h)
            draw_text(x, y, w, h)
        else:
            draw_grid(user.rect.x, user.rect.y, user.rect.width, user.rect.height)

            paint.textsize += 12 - user.count * 3
            draw_text(user.rect.x, user.rect.y, user.rect.width, user.rect.height)

    def should_show_zoomed_in(self):
        """Determines if the display of the grid should be zoomed in"""
        return settings.get("user.grid_show_zoomed") and user.count >= 2

    def calc_narrow(self, which, rect):
        rect = rect.copy()
        bdr = settings.get("user.grid_narrow_expansion")
        row = int(which - 1) // 3
        col = int(which - 1) % 3
        if settings.get("user.grids_put_one_bottom_left"):
            row = 2 - row
        rect.x += int(col * rect.width // 3) - bdr
        rect.y += int(row * rect.height // 3) - bdr
        rect.width = (rect.width // 3) + bdr * 2
        rect.height = (rect.height // 3) + bdr * 2
        return rect

    def narrow(self, which, move=True):
        if which < 1 or which > 9:
            return
        user.save_state()
        rect = user.calc_narrow(which, user.rect)
        # check count so we don't bother zooming in _too_ far
        if user.count < 5:
            user.rect = rect.copy()
            user.count += 1
        if move:
            ctrl.mouse_move(*rect.center)
        if user.should_show_zoomed_in():
            user.update_screenshot()
        else:
            user.mcanvas.freeze()

    def update_screenshot(self):
        def finish_capture():
            user.img = screen.capture_rect(user.rect)
            user.mcanvas.freeze()

        user.mcanvas.hide()
        cron.after("16ms", finish_capture)

    def draw_zoom(self, canvas, x, y, w, h):
        if user.img:
            src = Rect(0, 0, user.img.width, user.img.height)
            dst = Rect(x, y, w, h)
            canvas.draw_image_rect(user.img, src, dst)

    def narrow_to_pos(self, x, y):
        col_size = int(user.width // 3)
        row_size = int(user.height // 3)
        col = math.floor((x - user.rect.x) / col_size)
        row = math.floor((y - user.rect.x) / row_size)
        user.narrow(1 + col + 3 * row, move=False)

    def save_state(self):
        user.history.append((user.count, user.rect.copy()))

    def go_back(self):
        # FIXME: need window and screen tracking
        user.count, user.rect = user.history.pop()
        user.mcanvas.freeze()


mg = MouseSnapNine()


@mod.action_class
class GridActions:
    def grid_activate():
        """Show mouse grid"""
        if not mg.mcanvas:
            mg.setup()
        mg.show()
        ctx.tags = ["user.mouse_grid_showing"]

    def grid_place_window():
        """Places the grid on the currently active window"""
        mg.setup(rect=ui.active_window().rect)

    def grid_reset():
        """Resets the grid to fill the whole screen again"""
        if mg.active:
            mg.setup()

    def grid_select_screen(screen: int):
        """Brings up mouse grid"""
        mg.setup(screen_num=screen - 1)
        mg.show()

    def grid_narrow_list(digit_list: list[str]):
        """Choose fields multiple times in a row"""
        for d in digit_list:
            actions.user.grid_narrow(int(d))

    def grid_narrow(digit: Union[int, str]):
        """Choose a field of the grid and narrow the selection down"""
        mg.narrow(int(digit))

    def grid_go_back():
        """Sets the grid state back to what it was before the last command"""
        mg.go_back()

    def grid_close():
        """Close the active grid"""
        ctx.tags = []
        mg.close()

    def grid_is_active():
        """check if grid is already active"""
        return mg.active
