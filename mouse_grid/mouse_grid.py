# courtesy of https://github.com/timo/
# see https://github.com/timo/talon_scripts
from talon import Module, Context, app, canvas, screen, settings, ui, ctrl, cron
from talon.skia import Shader, Color, Paint, Rect
from talon.types.point import Point2d
from talon_plugins import eye_mouse, eye_zoom_mouse
from typing import Union

import math, time

import typing

mod = Module()
shimmer_effect_enabled = mod.setting(
    "grid_shimmer_effect_enabled",
    type=bool,
    default=False,
    desc="""Enable the "shimmer effect" that regularly displays a faint hint of the first two layers of the 3x3 grid.""",
)
shimmer_effect_duration = mod.setting(
    "grid_shimmer_effect_duration",
    type=float,
    default=10,
    desc="""How long should the shimmer effect take to pass across the screen.""",
)
shimmer_effect_pause = mod.setting(
    "grid_shimmer_effect_pause",
    type=float,
    default=420,
    desc="""How long should it take for the shimmer effect to come back.""",
)
shimmer_effect_width = mod.setting(
    "grid_shimmer_effect_stroke_width",
    type=float,
    default=1,
    desc="""How thick should the grid lines be that show up during the shimmer effect.""",
)

narrow_expansion = mod.setting(
    "grid_narrow_expansion",
    type=int,
    default=0,
    desc="""After narrowing, grow the new region by this many pixels in every direction, to make things immediately on edges easier to hit, and when the grid is at its smallest, it allows you to still nudge it around""",
)

mod.tag("mouse_grid_showing", desc="Tag indicates whether the mouse grid is showing")
mod.tag("mouse_grid_enabled", desc="Tag enables the mouse grid commands.")
ctx = Context()


class MouseSnapNine:
    def __init__(self):
        self.states = []
        # self.screen_index = 0
        self.screen = ui.screens()[0]
        self.offset_x = self.screen.x
        self.offset_y = self.screen.y
        self.width = self.screen.width
        self.height = self.screen.height
        self.states.append((self.offset_x, self.offset_y, self.width, self.height))
        self.mcanvas = canvas.Canvas.from_screen(self.screen)
        self.img = None
        self.wants_capture = 0
        self.active = False
        self.moving = False
        self.count = 0
        self.was_control_mouse_active = False
        self.was_zoom_mouse_active = False

    #     tap.register(tap.MMOVE, self.on_move)
    #
    # def on_move(self, typ, e):
    #     if typ != tap.MMOVE or not self.active:
    #         return
    #     x, y = self.pos()
    #     last_pos = self.states[-1]
    #     x2, y2 = last_pos[0] + last_pos[2]//2, last_pos[1] + last_pos[3]//2
    #     # print("moved ", e, x, y)
    #     if (e.x, e.y) != (x, y) and (e.x, e.y) != (x2, y2):
    #         self.stop(None)

    def start(self, *_):
        if self.active:
            print("already active - won't start")
            return
        # noinspection PyUnresolvedReferences
        if eye_zoom_mouse.zoom_mouse.enabled:
            self.was_zoom_mouse_active = True
            eye_zoom_mouse.toggle_zoom_mouse(False)
        if eye_mouse.control_mouse.enabled:
            self.was_control_mouse_active = True
            eye_mouse.control_mouse.toggle()
        if self.mcanvas is not None:
            print("unregistering a canvas")
            self.mcanvas.unregister("draw", self.draw)
        self.mcanvas.register("draw", self.draw)
        print("grid activating")
        self.active = True
        return True

    def stop(self, *_):
        if not shimmer_effect_enabled.get():
            self.mcanvas.unregister("draw", self.draw)
        self.active = False
        if self.was_control_mouse_active and not eye_mouse.control_mouse.enabled:
            eye_mouse.control_mouse.toggle()
        if self.was_zoom_mouse_active and not eye_zoom_mouse.zoom_mouse.enabled:
            eye_zoom_mouse.toggle_zoom_mouse(True)

        self.was_zoom_mouse_active = False
        self.was_control_mouse_active = False

    def draw(self, canvas):
        if self.wants_capture == 1:
            self.wants_capture = 2
            self.mcanvas.freeze()
            return
        elif self.wants_capture == 2:

            def finish_capture():
                print("capture finished")
                self.mcanvas.allows_capture = True
                self.wants_capture = 0
                self.mcanvas.register("paint", self.draw)
                self.mcanvas.freeze()

            def do_capture():
                print(
                    "capturing area",
                    self.offset_x,
                    self.offset_y,
                    self.width,
                    self.height,
                )
                self.img = screen.capture(
                    self.offset_x, self.offset_y, self.width, self.height
                )
                cron.after("5ms", finish_capture)

            self.mcanvas.allows_capture = False
            cron.after("5ms", do_capture)
            self.wants_capture = 3
            self.mcanvas.freeze()
            self.mcanvas.unregister("paint", self.draw)
        elif self.wants_capture == 3:
            return

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

        # def draw_grid(offset_x, offset_y, width, height, dxp = 0, dyp = 0):
        # dx = (dxp / 100) * width
        # dy = (dyp / 100) * height
        # canvas.draw_line(
        # offset_x + width // 3,
        # offset_y + dy,
        # offset_x + width // 3,
        # offset_y + height - dy,
        # )
        # canvas.draw_line(
        # offset_x + 2 * width // 3,
        # offset_y + dy,
        # offset_x + 2 * width // 3,
        # offset_y + height - dy,
        # )

        # canvas.draw_line(
        # offset_x + dx,
        # offset_y + height // 3,
        # offset_x + width - dx,
        # offset_y + height // 3,
        # )
        # canvas.draw_line(
        # offset_x + dx,
        # offset_y + 2 * height // 3,
        # offset_x + width - dx,
        # offset_y + 2 * height // 3,
        # )

        grid_stroke = 1

        if not self.active and shimmer_effect_enabled.get():
            remainder_time = time.time() % (
                shimmer_effect_duration.get() + shimmer_effect_pause.get()
            )
            if remainder_time < shimmer_effect_duration.get():
                alpha = "60"
                animpos = remainder_time / shimmer_effect_duration.get()
                # fromcnt = (animpos - 0.5) * 2
                stops = [
                    animpos - 0.1,
                    animpos - 0.05,
                    animpos,
                    animpos + 0.05,
                    animpos + 0.1,
                ]
                stops = list(map(lambda c: min(max(c, 0), 1), stops))
                paint.shader = Shader.linear_gradient(
                    0,
                    self.height / 9,
                    self.width,
                    8 * self.height / 9,
                    [
                        "00000000",
                        "ff0000" + alpha,
                        "0000ff" + alpha,
                        "00ff00" + alpha,
                        "00000000",
                    ],
                    stops,
                    Shader.TileMode.CLAMP,
                )
                grid_stroke = shimmer_effect_width.get()
                paint.stroke_width = 1
            else:
                return

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
                            offset_y + height / 6 + row * height / 3)
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
                draw_crosses(
                    *self.calc_narrow(
                        which, self.offset_x, self.offset_y, self.width, self.height
                    )
                )

        paint.stroke_width = grid_stroke
        if self.active:
            paint.color = "ff0000ff"
        else:
            paint.color = "000000ff"
        if self.count >= 2:
            aspect = self.width / self.height
            if aspect >= 1:
                w = self.screen.width / 3
                h = w / aspect
            else:
                h = self.screen.height / 3
                w = h * aspect
            x = (self.screen.width - w) / 2
            y = (self.screen.height - h) / 2
            self.draw_zoom(canvas, x, y, w, h)
            draw_grid(x, y, w, h)
            draw_text(x, y, w, h)
        else:
            draw_grid(self.offset_x, self.offset_y, self.width, self.height)

            paint.textsize += 12 - self.count * 3
            draw_text(self.offset_x, self.offset_y, self.width, self.height)

    def calc_narrow(self, which, offset_x, offset_y, width, height):
        bdr = narrow_expansion.get()
        row = int(which - 1) // 3
        col = int(which - 1) % 3
        if settings["user.grids_put_one_bottom_left"]:
            row = 2 - row
        offset_x += int(col * width // 3) - bdr
        offset_y += int(row * height // 3) - bdr
        width //= 3
        height //= 3
        width += bdr * 2
        height += bdr * 2
        return [offset_x, offset_y, width, height]

    def narrow(self, which, move=True):
        if which < 1 or which > 9:
            return
        self.save_state()
        self.offset_x, self.offset_y, self.width, self.height = self.calc_narrow(
            which, self.offset_x, self.offset_y, self.width, self.height
        )
        if move:
            ctrl.mouse_move(*self.pos())
        self.count += 1
        self.mcanvas.freeze()
        if self.count >= 2:
            self.wants_capture = 1
        # if self.count >= 4:
        # self.reset(None)
        self.mcanvas.freeze()

    def draw_zoom(self, c, x, y, w, h):
        if self.img:
            src = Rect(0, 0, self.img.width, self.img.height)
            dst = Rect(x, y, w, h)
            c.draw_image_rect(self.img, src, dst)

    def pos(self):
        return self.offset_x + self.width // 2, self.offset_y + self.height // 2

    def reset(self, pos=-1):
        def _reset(m):
            self.save_state()
            self.count = 0
            x, y = ctrl.mouse_pos()

            if pos >= 0:
                self.screen = ui.screens()[pos]
            else:
                self.screen = ui.screen_containing(x, y)

            # print(screens)
            # self.screen = screens[self.screen_index]
            self.offset_x = self.screen.x
            self.offset_y = self.screen.y
            self.width = self.screen.width
            self.height = self.screen.height
            if self.mcanvas is not None:
                self.mcanvas.unregister("draw", self.draw)
            self.mcanvas = canvas.Canvas.from_screen(self.screen)
            # self.mcanvas.register("draw", self.draw)
            if eye_mouse.control_mouse.enabled:
                self.was_control_mouse_active = True
                eye_mouse.control_mouse.toggle()
            if self.was_control_mouse_active and self.screen == ui.screens()[0]:
                # if self.screen == ui.screens()[0]:
                self.narrow_to_pos(x, y)
                self.narrow_to_pos(x, y)
                # self.narrow_to_pos(x, y)
            # print(self.offset_x, self.offset_y, self.width, self.height)
            # print(*self.pos())
            self.mcanvas.freeze()

        return _reset

    def reset_to_current_window(self):
        win = ui.active_window()
        rect = win.rect

        self.offset_x = rect.x
        self.offset_y = rect.y
        self.width = rect.width
        self.height = rect.height

        self.count = 0

    def narrow_to_pos(self, x, y):
        col_size = int(self.width // 3)
        row_size = int(self.height // 3)
        col = math.floor((x - self.offset_x) / col_size)
        row = math.floor((y - self.offset_y) / row_size)
        # print(f"Narrow to {row} {col} {1 + col + 3 * row}")
        self.narrow(1 + col + 3 * row, move=False)

    def save_state(self):
        self.states.append((self.offset_x, self.offset_y, self.width, self.height))

    def go_back(self):
        last_state = self.states.pop()
        self.offset_x, self.offset_y, self.width, self.height = last_state
        self.count -= 1


mg = MouseSnapNine()


@mod.action_class
class GridActions:
    def grid_activate():
        """Brings up a/the grid (mouse grid or otherwise)"""
        if mg.start():
            ctx.tags = ["user.mouse_grid_showing"]

    def grid_place_window():
        """Places the grid on the currently active window"""
        mg.reset_to_current_window()

    def grid_reset():
        """Resets the grid to fill the whole screen again"""
        mg.reset()(None)

    def grid_select_screen(screen: int):
        """Brings up a/the grid (mouse grid or otherwise)"""
        mg.reset(screen - 1)(None)
        mg.start()

    def grid_narrow_list(digit_list: typing.List[str]):
        """Choose fields multiple times in a row"""
        # print("narrow many", repr(digit))
        # print(str(digit_list))
        for d in digit_list:
            GridActions.grid_narrow(int(d))

    def grid_narrow(digit: Union[int, str]):
        """Choose a field of the grid and narrow the selection down"""
        # print("narrow one", repr(digit))
        mg.narrow(int(digit))

    def grid_go_back():
        """Sets the grid state back to what it was before the last command"""
        mg.go_back()

    def grid_close():
        """Close the active grid"""
        if len(ctx.tags) > 0 or mg.active:
            ctx.tags = []
            mg.reset()(None)
            mg.stop()


def check_shimmer_setting_at_startup():
    if shimmer_effect_enabled.get():
        mg.start()
        mg.reset()
        mg.stop()


app.register("launch", check_shimmer_setting_at_startup)
