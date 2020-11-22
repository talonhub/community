# prototype of a clickless mouse mode using Talon. This does not coexist with the zoom or control mouse modes
# l = left click
# lh = left hold
# ld = left double click
# su = scroll up
# sd = scroll down
# r = right click
# rh = right click old
# ka = keep alive for e.g. leaving the thing up for easy scroll down/up on webpages. no action

from talon import Module, Context, app, canvas, screen, ui, ctrl, cron, actions

import math, time

mod = Module()
ctx = Context()

STATE_MOUSE_IDLE = 0
STATE_MOUSE_MOVING = 1
STATE_MOUSE_STOPPED = 2
STATE_DISPLAYING_OPTIONS = 3


class dwell_button:
    def __init__(self, x, y, action="l"):
        self.x = x
        self.y = y
        self.hit = False
        self.action = action
        self.last_hit_time = None

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
        self.mcanvas = canvas.Canvas.from_screen(self.screen)
        # self.mcanvas.register("draw", self.draw)
        self.x, self.y = ctrl.mouse_pos()
        self._dwell_x, self._dwell_y = ctrl.mouse_pos()
        self.state = STATE_MOUSE_IDLE
        self.last_time = 0
        self.enabled = False
        self.auto_hide_time = 0.8
        self.mouse_idle_time = 0.150
        self.item_selection_time = 0.200
        self.radius = 20

    def enable(self, enable):
        self.enabled = enable

        if self.enabled:
            self.mcanvas.register("draw", self.draw)
        else:
            self.mcanvas.unregister("draw", self.draw)

    def set_button_positions(self):
        self.button_positions = []
        self.x, self.y = ctrl.mouse_pos()
        self._dwell_x, self._dwell_y = self.x, self.y
        x = self.x
        y = self.y

        # to best handle menus and such, we're going to prefer to draw things
        # downward by default wherever possible
        if x <= 70 and y <= 65:
            # print("x <= 70 and y <= 65")
            self.button_positions.append(dwell_button(x, y + 65, "l"))
            self.button_positions.append(dwell_button(x + 70, y, "r"))
        elif x + 70 >= self.width and y <= 65:
            self.button_positions.append(dwell_button(x - 70, y, "l"))
            self.button_positions.append(dwell_button(x, y + 65, "r"))
        elif x <= 70 and y + 65 >= self.height:
            # print("x <= 70 and y + 65 >= self.height")

            self.button_positions.append(dwell_button(x + 70, y, "r"))
            self.button_positions.append(dwell_button(x, y - 65, "l"))
        elif x + 70 >= self.width and y + 65 >= self.height:
            # print("x + 70 >= self.width and y + 65 >= self.height")
            self.button_positions.append(dwell_button(x - 70, y, "l"))
            self.button_positions.append(dwell_button(x, y - 65, "r"))
        elif y + 65 >= self.height:
            # print("y + 65 >= self.height")
            self.button_positions.append(dwell_button(x - 70, y, "lh"))
            self.button_positions.append(dwell_button(x - 45, y - 40, "l"))
            self.button_positions.append(dwell_button(x, y - 65, "ld"))
            self.button_positions.append(dwell_button(x + 45, y - 40, "r"))
            self.button_positions.append(dwell_button(x + 70, y, "rh"))
        elif x <= 70:
            # print("x<= 70")
            self.button_positions.append(dwell_button(x, y + 65, "ld"))
            self.button_positions.append(dwell_button(x + 45, y + 40, "r"))
            self.button_positions.append(dwell_button(x + 70, y, "rh"))
            self.button_positions.append(dwell_button(x + 45, y - 40, "lh"))
            self.button_positions.append(dwell_button(x, y - 65, "l"))
        elif x + 70 >= self.width:
            self.button_positions.append(dwell_button(x, y + 65, "ld"))
            self.button_positions.append(dwell_button(x - 45, y + 40, "r"))
            self.button_positions.append(dwell_button(x - 70, y, "rh"))
            self.button_positions.append(dwell_button(x - 45, y - 40, "lh"))
            self.button_positions.append(dwell_button(x, y - 65, "l"))
        elif y + 65 <= self.height and x + 70 <= self.width:
            # print("y + 65 < self.height and x + 70 < self.width")
            self.button_positions.append(dwell_button(x - 45, y - 40, "su"))
            self.button_positions.append(dwell_button(x + 45, y - 40, "sd"))
            self.button_positions.append(dwell_button(x, y - 65, "ka"))

            self.button_positions.append(dwell_button(x - 70, y, "lh"))
            self.button_positions.append(dwell_button(x - 45, y + 40, "l"))
            self.button_positions.append(dwell_button(x, y + 65, "ld"))
            self.button_positions.append(dwell_button(x + 45, y + 40, "r"))
            self.button_positions.append(dwell_button(x + 70, y, "rh"))

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
                if time.time() - self.last_time >= self.mouse_idle_time:
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
                if (x <= b.x + self.radius and b.x - self.radius <= x) and (
                    y <= b.y + self.radius and b.y - self.radius <= y
                ):
                    # print("hit")
                    b.hit_check(True)
                    self.last_time = time.time()
                    item_hit = b
                else:
                    b.hit_check(False)

            if (
                not item_hit
                and time.time() - self.last_time >= self.auto_hide_time
                and (self._dwell_x == x or self._dwell_y == y)
            ):
                self.state = STATE_MOUSE_IDLE
            elif (
                item_hit
                and time.time() - item_hit.last_hit_time >= self.item_selection_time
            ):
                draw_options = False

                # print("performing action...")
                action = item_hit.action
                if action != "su" and action != "sd" and action != "ka":
                    ctrl.mouse_move(self.x, self.y)

                if item_hit.action == "lh":
                    # print("left hold")
                    print(str(ctrl.mouse_buttons_down()))
                    index = 0
                    if app.platform == "windows":
                        index = 1
                    if 1 not in ctrl.mouse_buttons_down():
                        print("pressing button 0 down")
                        ctrl.mouse_click(button=0, down=True)
                    else:
                        print("pressing button 0 up")
                        actions.sleep("50ms")
                        ctrl.mouse_click(button=0, up=True)

                elif item_hit.action == "l":
                    ctrl.mouse_click(button=0, hold=16000)

                elif item_hit.action == "ld":
                    ctrl.mouse_click(button=0, hold=16000)
                    ctrl.mouse_click(button=0, hold=16000)

                elif item_hit.action == "r":
                    ctrl.mouse_click(button=1, hold=16000)

                elif item_hit.action == "rh":
                    print(str(ctrl.mouse_buttons_down()))
                    index = 1
                    if app.platform == "windows":
                        index = 2
                    if index not in ctrl.mouse_buttons_down():
                        ctrl.mouse_click(button=1, down=True)
                    else:
                        actions.sleep("50ms")
                        ctrl.mouse_click(button=1, up=True)
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

            elif (
                abs(x - self.x) >= self.radius * 4 or abs(y - self.y) >= self.radius * 4
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
            paint.color = "ff0000"
            paint.style = paint.Style.STROKE
            canvas.draw_circle(b.x, b.y, self.radius + 1)

            if b.hit:
                paint.color = "00FF00"
                paint.style = paint.Style.FILL
            else:
                paint.color = "000000"
                paint.style = paint.Style.STROKE

            paint.style = paint.Style.FILL
            canvas.draw_circle(b.x, b.y, self.radius)

            canvas.paint.text_align = canvas.paint.TextAlign.CENTER
            text_string = b.action
            paint.textsize = 20
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
