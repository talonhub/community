# courtesy of https://github.com/timo/
# see https://github.com/timo/talon_scripts
import math
from typing import Union

from talon import Context, Module, actions, canvas, cron, ctrl, screen, settings, ui
from talon.skia import Paint, Rect
from talon.types.point import Point2d
from talon_plugins import eye_mouse, eye_zoom_mouse

mod = Module()
narrow_expansion = mod.setting(
    "grid_narrow_expansion",
    type=int,
    default=0,
    desc="""After narrowing, grow the new region by this many pixels in every direction, to make things immediately on edges easier to hit, and when the grid is at its smallest, it allows you to still nudge it around""",
)

mod.tag("mouse_grid_showing", desc="Tag indicates whether the mouse grid is showing")
mod.tag(
    "mouse_grid_enabled",
    desc="Deprecated: do not use.  Activates legacy m grid command",
)
ctx = Context()


class MouseSnapNine:
    def __init__(self):
        self.screen = None
        self.rect = None
        self.history = []
        self.img = None
        self.mcanvas = None
        self.active = False
        self.count = 0
        self.was_control_mouse_active = False
        self.was_zoom_mouse_active = False

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
        self.rect = rect.copy()
        self.screen = screen
        self.count = 0
        self.img = None
        if self.mcanvas is not None:
            self.mcanvas.close()
        self.mcanvas = canvas.Canvas.from_screen(screen)
        if self.active:
            self.mcanvas.register("draw", self.draw)
            self.mcanvas.freeze()

    def show(self):
        if self.active:
            return
        # noinspection PyUnresolvedReferences
        if eye_zoom_mouse.zoom_mouse.enabled:
            self.was_zoom_mouse_active = True
            eye_zoom_mouse.toggle_zoom_mouse(False)
        if eye_mouse.control_mouse.enabled:
            self.was_control_mouse_active = True
            eye_mouse.control_mouse.toggle()
        self.mcanvas.register("draw", self.draw)
        self.mcanvas.freeze()
        self.active = True
        return

    def close(self):
        if not self.active:
            return
        self.mcanvas.unregister("draw", self.draw)
        self.mcanvas.close()
        self.mcanvas = None
        self.img = None

        self.active = False
        if self.was_control_mouse_active and not eye_mouse.control_mouse.enabled:
            eye_mouse.control_mouse.toggle()
        if self.was_zoom_mouse_active and not eye_zoom_mouse.zoom_mouse.enabled:
            eye_zoom_mouse.toggle_zoom_mouse(True)

        self.was_zoom_mouse_active = False
        self.was_control_mouse_active = False

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
                    if settings["user.grids_put_one_bottom_left"]:
                        text_string = f"{(2 - row)*3+col+1}"
                    else:
                        text_string = f"{row*3+col+1}"
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

        if self.count < 2:
            paint.color = "00ff007f"
            for which in range(1, 10):
                gap = 35 - self.count * 10
                if not self.active:
                    gap = 45
                draw_crosses(*self.calc_narrow(which, self.rect))

        paint.stroke_width = grid_stroke
        if self.active:
            paint.color = "ff0000ff"
        else:
            paint.color = "000000ff"
        if self.count >= 2:
            aspect = self.rect.width / self.rect.height
            if aspect >= 1:
                w = self.screen.width / 3
                h = w / aspect
            else:
                h = self.screen.height / 3
                w = h * aspect
            x = self.screen.x + (self.screen.width - w) / 2
            y = self.screen.y + (self.screen.height - h) / 2
            self.draw_zoom(canvas, x, y, w, h)
            draw_grid(x, y, w, h)
            draw_text(x, y, w, h)
        else:
            draw_grid(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

            paint.textsize += 12 - self.count * 3
            draw_text(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def calc_narrow(self, which, rect):
        rect = rect.copy()
        bdr = narrow_expansion.get()
        row = int(which - 1) // 3
        col = int(which - 1) % 3
        if settings["user.grids_put_one_bottom_left"]:
            row = 2 - row
        rect.x += int(col * rect.width // 3) - bdr
        rect.y += int(row * rect.height // 3) - bdr
        rect.width = (rect.width // 3) + bdr * 2
        rect.height = (rect.height // 3) + bdr * 2
        return rect

    def narrow(self, which, move=True):
        if which < 1 or which > 9:
            return
        self.save_state()
        rect = self.calc_narrow(which, self.rect)
        # check count so we don't bother zooming in _too_ far
        if self.count < 5:
            self.rect = rect.copy()
            self.count += 1
        if move:
            ctrl.mouse_move(*rect.center)
        if self.count >= 2:
            self.update_screenshot()
        else:
            self.mcanvas.freeze()

    def update_screenshot(self):
        def finish_capture():
            self.img = screen.capture_rect(self.rect)
            self.mcanvas.freeze()

        self.mcanvas.hide()
        cron.after("16ms", finish_capture)

    def draw_zoom(self, canvas, x, y, w, h):
        if self.img:
            src = Rect(0, 0, self.img.width, self.img.height)
            dst = Rect(x, y, w, h)
            canvas.draw_image_rect(self.img, src, dst)

    def narrow_to_pos(self, x, y):
        col_size = int(self.width // 3)
        row_size = int(self.height // 3)
        col = math.floor((x - self.rect.x) / col_size)
        row = math.floor((y - self.rect.x) / row_size)
        self.narrow(1 + col + 3 * row, move=False)

    def save_state(self):
        self.history.append((self.count, self.rect.copy()))

    def go_back(self):
        # FIXME: need window and screen tracking
        self.count, self.rect = self.history.pop()
        self.mcanvas.freeze()


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
            actions.self.grid_narrow(int(d))

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
