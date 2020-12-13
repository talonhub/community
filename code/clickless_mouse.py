# prototype of a clickless mouse mode using Talon. This does not coexist with the zoom, control mouse or mouse grid
# l = left click
# lh = left hold
# lr = left release. when left is down, all options become lr
# ld = left double click
# su = scroll up
# sd = scroll down
# r = right click
# rh = right click old, DISABLED, doesn't work yet.
# ka = keep alive for e.g. leaving the thing up for easy scroll down/up on webpages. no action

from talon import Module, Context, app, canvas, screen, ui, ctrl, cron, actions

import math, time

mod = Module()
ctx = Context()

STATE_MOUSE_IDLE = 0
STATE_MOUSE_MOVING = 1
STATE_MOUSE_STOPPED = 2
STATE_DISPLAYING_OPTIONS = 3

dwell_time = mod.setting(
    "clickless_mouse_dwell_time",
    type=float,
    default=0.250,
    desc="The required dwell time before triggering the action",
)

auto_hide = mod.setting(
    "clickless_mouse_auto_hide_time",
    type=float,
    default=0.8,
    desc="The time before the clickless mouse is auto-hidden",
)

mouse_idle = mod.setting(
    "clickless_mouse_idle_time_before_display",
    type=float,
    default=0.35,
    desc="The time the mouse must be idle before the clickless mouse options are displayed",
)

radius = mod.setting(
    "clickless_mouse_radius",
    type=int,
    default=15 if app.platform == "mac" else 20,
    desc="The size of the options in the clickless mouse",
)


class dwell_button:
    def __init__(self, x, y, action="l"):
        self.x = x
        self.y = y
        self.hit = False
        self.action = action
        self.last_hit_time = None
        self.scroll_progress = 0

    def hit_check(self, hit):
        if hit:
            if not self.last_hit_time:
                self.last_hit_time = time.time()
        else:
            hit = False
            self.last_hit_time = None

        self.hit = hit


class clickless_mouse:
    def __init__(self):
        self.button_positions = []
        # self.screen_index = 0
        self.screen = ui.screens()[0]
        self.offset_x = self.screen.x
        self.offset_y = self.screen.y
        self.width = self.screen.width
        self.height = self.screen.height
        # self.mcanvas.register("draw", self.draw)
        self.mcanvas = None
        self.x, self.y = ctrl.mouse_pos()
        self._dwell_x, self._dwell_y = ctrl.mouse_pos()
        self.state = STATE_MOUSE_IDLE
        self.last_time = 0
        self.enabled = False

    def __del__(self):
        self.mcanvas = None

    def is_left_down(self):
        left_index = 0

        if app.platform == "windows":
            left_index = 1
        return left_index in ctrl.mouse_buttons_down()

    def enable(self, enable):
        self.enabled = enable

        if self.enabled:
            self.mcanvas = canvas.Canvas.from_screen(self.screen)
            self.mcanvas.register("draw", self.draw)
        else:
            self.mcanvas.unregister("draw", self.draw)
            self.mcanvas = None

    def set_button_positions(self):
        self.button_positions = []
        self.scroll_progress = 0
        self.x, self.y = ctrl.mouse_pos()
        self._dwell_x, self._dwell_y = self.x, self.y
        x = self.x
        y = self.y

        if self.is_left_down():
            # print("case 8")
            # print("y + 65 < self.height and x + 70 < self.width")
            self.button_positions.append(
                dwell_button(
                    x - math.ceil(radius.get() * 2.25),
                    y - math.ceil(radius.get() * 2),
                    "lr",
                )
            )
            self.button_positions.append(
                dwell_button(
                    x + math.ceil(radius.get() * 2.25),
                    y - math.ceil(radius.get() * 2),
                    "lr",
                )
            )
            self.button_positions.append(
                dwell_button(x, y - math.ceil(radius.get() * 3.25), "lr")
            )

            self.button_positions.append(
                dwell_button(x - math.ceil(radius.get() * 3.5), y, "lr")
            )
            self.button_positions.append(
                dwell_button(
                    x - math.ceil(radius.get() * 2.25),
                    y + math.ceil(radius.get() * 2),
                    "lr",
                )
            )
            self.button_positions.append(
                dwell_button(x, y + math.ceil(radius.get() * 3.25), "lr")
            )
            self.button_positions.append(
                dwell_button(
                    x + math.ceil(radius.get() * 2.25),
                    y + math.ceil(radius.get() * 2),
                    "lr",
                )
            )
            self.button_positions.append(
                dwell_button(x + math.ceil(radius.get() * 3.5), y, "lr")
            )

        # to best handle menus and such, we're going to prefer to draw things
        # downward by default wherever possible
        elif x <= radius.get() * 3.5 and y <= radius.get() * 3.25:
            # print("case 1")
            # print("x <= 70 and y <= 65")
            self.button_positions.append(
                dwell_button(x, y + math.ceil(radius.get() * 3.5), "l")
            )
            self.button_positions.append(
                dwell_button(x + math.ceil(radius.get() * 3.25), y, "r")
            )
        elif x + radius.get() * 3.5 >= self.width and y <= radius.get() * 3.25:
            # print("case 2")
            self.button_positions.append(
                dwell_button(x - math.ceil(radius.get() * 3.5), y, "l")
            )
            self.button_positions.append(
                dwell_button(x, y + math.ceil(radius.get() * 3.25), "r")
            )
        elif x <= radius.get() * 3.5 and y + radius.get() * 3.25 >= self.height:
            # print("x <= 70 and y + 65 >= self.height")
            # print("case 3")
            self.button_positions.append(
                dwell_button(x + math.ceil(radius.get() * 3.5), y, "r")
            )
            self.button_positions.append(
                dwell_button(x, y - math.ceil(radius.get() * 3.25), "l")
            )
        elif (
            x + radius.get() * 3.5 >= self.width
            and y + math.ceil(radius.get() * 3.25) >= self.height
        ):
            # print("case 4")
            # print("x + 70 >= self.width and y + 65 >= self.height")
            self.button_positions.append(
                dwell_button(x - math.ceil(radius.get() * 3.5), y, "l")
            )
            self.button_positions.append(
                dwell_button(x, y - math.ceil(radius.get() * 3.25), "r")
            )
        elif y + math.ceil(radius.get() * 3.25) >= self.height:
            # print("case 5")
            # print("y + 65 >= self.height")
            self.button_positions.append(
                dwell_button(x - math.ceil(radius.get() * 3.5), y, "lh")
            )
            self.button_positions.append(
                dwell_button(
                    x - math.ceil(radius.get() * 2.25),
                    y - math.ceil(radius.get() * 2),
                    "l",
                )
            )
            self.button_positions.append(
                dwell_button(x, y - math.ceil(radius.get() * 3.25), "ld")
            )
            self.button_positions.append(
                dwell_button(
                    x + math.ceil(radius.get() * 2.25),
                    y - math.ceil(radius.get() * 2),
                    "r",
                )
            )
            # self.button_positions.append(dwell_button(x + 70, y, "rh"))
        elif x <= radius.get() * 3.5:
            # print("case 6")
            # print("x<= 70")
            self.button_positions.append(
                dwell_button(x, y + math.ceil(radius.get() * 3.25), "ld")
            )
            self.button_positions.append(
                dwell_button(
                    x + math.ceil(radius.get() * 2.25),
                    y + math.ceil(radius.get() * 2),
                    "r",
                )
            )
            # self.button_positions.append(dwell_button(x + 70, y, "rh"))
            self.button_positions.append(
                dwell_button(
                    x + math.ceil(radius.get() * 2.25),
                    y - math.ceil(radius.get() * 2),
                    "lh",
                )
            )
            self.button_positions.append(
                dwell_button(x, y - math.ceil(radius.get() * 3.25), "l")
            )
        elif x + radius.get() * 2 >= self.width:
            # print("case 7")
            self.button_positions.append(
                dwell_button(x, y + math.ceil(radius.get() * 3.25), "ld")
            )
            self.button_positions.append(
                dwell_button(
                    x - math.ceil(radius.get() * 2.25),
                    y + math.ceil(radius.get() * 2),
                    "r",
                )
            )
            # self.button_positions.append(dwell_button(x - 70, y, "rh"))
            self.button_positions.append(
                dwell_button(
                    x - math.ceil(radius.get() * 2.25),
                    y - math.ceil(radius.get() * 2),
                    "lh",
                )
            )
            self.button_positions.append(
                dwell_button(x, y - math.ceil(radius.get() * 3.25), "l")
            )
        elif (
            y + math.ceil(radius.get() * 3.25) <= self.height
            and x + radius.get() * 3.5 <= self.width
        ):
            # print("case 8")
            # print("y + 65 < self.height and x + 70 < self.width")
            self.button_positions.append(
                dwell_button(
                    x - math.ceil(radius.get() * 2.25),
                    y - math.ceil(radius.get() * 2),
                    "su",
                )
            )
            self.button_positions.append(
                dwell_button(
                    x + math.ceil(radius.get() * 2.25),
                    y - math.ceil(radius.get() * 2),
                    "sd",
                )
            )
            self.button_positions.append(
                dwell_button(x, y - math.ceil(radius.get() * 3.25), "lt")
            )

            self.button_positions.append(
                dwell_button(x - math.ceil(radius.get() * 3.5), y, "lh")
            )
            self.button_positions.append(
                dwell_button(
                    x - math.ceil(radius.get() * 2.25),
                    y + math.ceil(radius.get() * 2),
                    "ld",
                )
            )
            self.button_positions.append(
                dwell_button(x, y + math.ceil(radius.get() * 3.25), "l")
            )
            self.button_positions.append(
                dwell_button(
                    x + math.ceil(radius.get() * 2.25),
                    y + math.ceil(radius.get() * 2),
                    "r",
                )
            )
            self.button_positions.append(
                dwell_button(x + math.ceil(radius.get() * 3.5), y, "ka")
            )

    def draw(self, canvas):
        x, y = ctrl.mouse_pos()
        # print("({},{})".format(x,y))
        if self.state == STATE_MOUSE_IDLE:
            # print("idle")

            if x != self.x and y != self.y:
                self.x, self.y = ctrl.mouse_pos()
                self.state = STATE_MOUSE_MOVING

        elif self.state == STATE_MOUSE_MOVING:
            # print("moving")

            if x == self.x and y == self.y:
                self.x, self.y = ctrl.mouse_pos()
                self.last_time = time.time()
                self.state = STATE_MOUSE_STOPPED
            else:
                self.x, self.y = ctrl.mouse_pos()

        elif self.state == STATE_MOUSE_STOPPED:
            # print("stopped")

            if x == self.x and y == self.y:
                if time.time() - self.last_time >= mouse_idle.get():
                    self.last_time = time.time()
                    self.set_button_positions()
                    self.state = STATE_DISPLAYING_OPTIONS
            else:
                self.x, self.y = ctrl.mouse_pos()
                self.state = STATE_MOUSE_MOVING
                self.button_positions = []
        elif self.state == STATE_DISPLAYING_OPTIONS:
            # print("display")
            item_hit = None
            draw_options = True

            for b in self.button_positions:
                if (x <= b.x + radius.get() and b.x - radius.get() <= x) and (
                    y <= b.y + radius.get() and b.y - radius.get() <= y
                ):
                    # print("hit")
                    b.hit_check(True)
                    self.last_time = time.time()
                    item_hit = b
                else:
                    b.hit_check(False)

            if (
                not item_hit
                and time.time() - self.last_time >= auto_hide.get()
                and (self._dwell_x == x or self._dwell_y == y)
            ):
                self.state = STATE_MOUSE_IDLE
            elif item_hit and time.time() - item_hit.last_hit_time >= dwell_time.get():
                draw_options = False

                # print("performing action...")
                action = item_hit.action
                if action != "su" and action != "sd" and action != "ka":
                    ctrl.mouse_move(self.x, self.y)

                if item_hit.action == "lh":
                    # print("left hold")
                    if not self.is_left_down():
                        # print("pressing button 0 down")
                        ctrl.mouse_click(button=0, down=True)
                    else:
                        # print("pressing button 0 up")
                        actions.sleep("50ms")
                        ctrl.mouse_click(button=0, up=True)

                    # print(str(ctrl.mouse_buttons_down()))
                elif item_hit.action == "lr":
                    if self.is_left_down():
                        actions.sleep("50ms")
                        ctrl.mouse_click(button=0, up=True)

                elif item_hit.action == "l":
                    ctrl.mouse_click(button=0, hold=16000)

                elif item_hit.action == "ld":
                    ctrl.mouse_click(button=0, hold=16000)
                    ctrl.mouse_click(button=0, hold=16000)

                elif item_hit.action == "lt":
                    ctrl.mouse_click(button=0, hold=16000)
                    ctrl.mouse_click(button=0, hold=16000)
                    ctrl.mouse_click(button=0, hold=16000)

                elif item_hit.action == "r":
                    ctrl.mouse_click(button=1, hold=16000)

                elif item_hit.action == "rh":
                    index = 1
                    if app.platform == "windows":
                        index = 2
                    if index not in ctrl.mouse_buttons_down():
                        ctrl.mouse_click(button=1, down=True)
                    else:
                        actions.sleep("50ms")
                        ctrl.mouse_click(button=1, up=True)
                        # print(str(ctrl.mouse_buttons_down()))
                elif item_hit.action == "su":
                    actions.mouse_scroll(y=-10)
                    draw_options = True

                elif item_hit.action == "sd":
                    actions.mouse_scroll(y=10)
                    draw_options = True
                elif item_hit.action == "ka":
                    draw_options = True

                if action != "su" and action != "sd" and action != "ka":
                    self.x, self.y = ctrl.mouse_pos()
                    self.state = STATE_MOUSE_IDLE
                    self.scroll_progress = 0

            elif (
                abs(x - self.x) >= radius.get() * 7
                or abs(y - self.y) >= radius.get() * 7
            ):
                draw_options = False
                self.state = STATE_MOUSE_IDLE

            if draw_options:
                if self._dwell_x != x or self._dwell_y != y:
                    self.last_time = time.time()

                self._dwell_x, self._dwell_y = ctrl.mouse_pos()
                self.draw_options(canvas)

    def draw_options(self, canvas):
        paint = canvas.paint

        for b in self.button_positions:
            # draw outer circle
            paint.color = "ffffff"
            paint.style = paint.Style.STROKE
            canvas.draw_circle(b.x, b.y, radius.get() + 1)

            # draw inner circle
            paint.color = "000000"
            paint.style = paint.Style.STROKE
            paint.style = paint.Style.FILL
            canvas.draw_circle(b.x, b.y, radius.get())

            # draw hit circle
            if b.last_hit_time:
                paint.color = "00FF00"
                paint.style = paint.Style.FILL

                _radius = min(
                    math.ceil(
                        radius.get()
                        * (time.time() - b.last_hit_time)
                        / dwell_time.get()
                    ),
                    radius.get(),
                )
                canvas.draw_circle(b.x, b.y, _radius)

            canvas.paint.text_align = canvas.paint.TextAlign.CENTER
            text_string = b.action
            paint.textsize = radius.get()
            paint.color = "ffffff"

            # text_rect = canvas.paint.measure_text(text_string)[1]
            canvas.draw_text(text_string, b.x, b.y)


cm = clickless_mouse()

# uncomment to enable by default/for quick testing
# cm.enable(True)


def toggle_clickless_mouse(state):
    cm.enable(state)


menu = app.menu.submenu("knausj_talon", weight=999, disabled=False)
menu.toggle("Clickless mouse", weight=2, cb=toggle_clickless_mouse)

app.menu.sep(weight=998)
