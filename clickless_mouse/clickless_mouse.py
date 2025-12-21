# prototype of a clickless mouse mode using Talon. This does not coexist with the zoom, control mouse or mouse grid
# todo:
#  (1) smoother, accelerated scrolling
#  (2) horizontal scrolling
#  (3) detect non-clickless mouse events to dismiss
#  (4) better handling of mixed resolutions - 4k + non-4k etc
#  (5) Clicking some contexts menus (e.g. run as admin) in the start menu requires a double click???
from talon import Module, Context, app, canvas, screen, ui, ctrl, cron, actions, settings

import math, time

# l = left click
# lh = left hold
# lr = left release. when left is down, all options become lr
# ld = left double click
# su = scroll up
# sd = scroll down
# r = right click
# rh = right click old, DISABLED, doesn't work yet.
# ka = keep alive for e.g. leaving the thing up for easy scroll down/up on webpages. no action
# x = force an exit when auto hide is disabled
horizontal_button_order_auto_hide_enabled = [
    "l",
    "ld",
    "lt",
    "lh",
    "r",
    "su",
    "sd",
    "ka",
]
horizontal_button_order_auto_hide_disabled = [
    "l",
    "ld",
    "lt",
    "lh",
    "r",
    "su",
    "sd",
    "x",
]
left_mouse_button_index = 0
right_mouse_button_index = 1


mod = Module()
ctx = Context()
mod.tag("clickless_mouse_enabled", desc="Indicates the clickless mouse is enabled")

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
    "clickless_mouse_auto_hide",
    type=int,
    default=1,
    desc="toggles the functionality to auto hide within the bounds",
)

auto_hide_time = mod.setting(
    "clickless_mouse_auto_hide_time",
    type=float,
    default=1.25,
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

release_button_delay = mod.setting(
    "clickless_mouse_release_delay",
    type=int,
    default=50,
    desc="The delay (ms) before releasing the held mouse button",
)


prevent_redisplay_for_minor_motions = mod.setting(
    "clickless_mouse_prevent_redisplay_for_minor_motions",
    type=int,
    default=0,
    desc="A value of 1 or more prevents re-display for minor motions",
)

vertical_offset = mod.setting(
    "clickless_mouse_vertical_offset",
    type=float,
    default=2.25,
    desc="when drawing the options horizontally, this determines the vertical distance from the mouse. The total distance is the value times the radius.",
)

horizontal_offset = mod.setting(
    "clickless_mouse_horizontal_offset",
    type=float,
    default=2.25,
    desc="when drawing the options horizontally, this determines the distance between the options. The total distance is the value times the radius.",
)

stroke_width = mod.setting(
    "clickless_mouse_stroke_width",
    type=int,
    default=3,
    desc="The width the stroke for the cursor position.",
)

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
                self.last_hit_time = time.perf_counter()
        else:
            hit = False
            self.last_hit_time = None

        self.hit = hit


class clickless_mouse:
    def __init__(self):
        self.button_positions = []
        self.screen = None
        self.mcanvas = None
        self.x, self.y = ctrl.mouse_pos()
        self._dwell_x, self._dwell_y = ctrl.mouse_pos()
        self.state = STATE_MOUSE_IDLE
        self.last_time = 0
        self.enabled = False
        self.update_cron = None
        self.draw_registered = False

        # after moving the mouse to perform an action,
        # avoid a state change in the first update.
        # this prevents an unnecessary re-display
        self.suppress_next_update = False

        # the bounds around the displayed options. if you go outside, options
        # are hidden
        self.y_min = self.y_max = self.x_min = self.x_max = 0

    def is_left_down(self):
        return left_mouse_button_index in ctrl.mouse_buttons_down()

    def enable(self, _enable):
        if _enable == self.enabled:
            return

        self.enabled = _enable

        if self.enabled:
            ctx.tags = ["user.clickless_mouse_enabled"]
        else:
            ctx.tags = []

        if self.enabled:
            self.x, self.y = ctrl.mouse_pos()
            self.update_cron = cron.interval("16ms", self.update)
        elif self.update_cron:
            cron.cancel(self.update_cron)
            self.update_cron = None
            self.state = STATE_MOUSE_IDLE
            if self.draw_registered:
                self.mcanvas.unregister("draw", self.draw)
                self.mcanvas.close()
                self.mcanvas = None
                self.draw_registered = False

    def toggle(self):
        self.enable(not self.enabled)

    def get_max_horizontal_distance(self):
        return 2 * settings.get("user.clickless_mouse_radius") * (len(self.get_horizontal_button_order()) + 1.5)

    def get_horizontal_button_order(self):
        if settings.get("user.clickless_mouse_auto_hide") >= 1:
            return horizontal_button_order_auto_hide_enabled
        else:
            return horizontal_button_order_auto_hide_disabled

    def set_horizontal_button_positions_and_bounds(self, x, y, draw_right, draw_above):
        x_pos = None

        if draw_above:
            y_pos = y - math.ceil(settings.get("user.clickless_mouse_radius") * settings.get("user.clickless_mouse_vertical_offset"))  
            self.y_min = y - math.ceil(settings.get("user.clickless_mouse_radius") * 5)
            self.y_max = y + math.ceil(settings.get("user.clickless_mouse_radius") * 2)      
        else:
            y_pos = y + math.ceil(settings.get("user.clickless_mouse_radius") * settings.get("user.clickless_mouse_vertical_offset"))
            self.y_min = y - math.ceil(settings.get("user.clickless_mouse_radius") * 2)
            self.y_max = y + math.ceil(settings.get("user.clickless_mouse_radius") * 5) 

        if draw_right:
            self.x_min = x - math.ceil(settings.get("user.clickless_mouse_radius") * 2.25) 
            self.x_max = x + self.get_max_horizontal_distance()          
        else:
            self.x_min = x - self.get_max_horizontal_distance()
            self.x_max = x + math.ceil(settings.get("user.clickless_mouse_radius") * 2.25)

        for index, button_label in enumerate(
            self.get_horizontal_button_order()
        ):
            if draw_right:
                x_pos = x + math.ceil(settings.get("user.clickless_mouse_radius") * (2.5 + settings.get("user.clickless_mouse_horizontal_offset") * (index - 1)))
            else:
                x_pos = x - math.ceil(settings.get("user.clickless_mouse_radius") * (2.5 + settings.get("user.clickless_mouse_horizontal_offset") * (index - 1)))
            
            self.button_positions.append(
                dwell_button(
                    x_pos,
                    y_pos,
                    button_label if not self.is_left_down() else "lr",
                )
            )

    def set_button_positions(self):
        self.button_positions = []
        self.x, self.y = ctrl.mouse_pos()

        self._dwell_x, self._dwell_y = self.x, self.y

        # alias the cursor position for convenience
        x = self.x
        y = self.y

        # calculate the screen coordinates
        x_screen = self.x - self.screen.x
        y_screen = self.y - self.screen.y

        # top left corner
        if x_screen <= settings.get("user.clickless_mouse_radius") * 3.5 and y_screen <= settings.get("user.clickless_mouse_radius") * 3.25:
            # print("case 1")
            self.set_horizontal_button_positions_and_bounds(x, y, True, False)

        # top right corner
        elif (
            x_screen + settings.get("user.clickless_mouse_radius") * 3.5 >= self.screen.width
            and y_screen <= settings.get("user.clickless_mouse_radius") * 3.25
        ):
            # print("case 2")
            self.set_horizontal_button_positions_and_bounds(x, y, False, False)

        # bottom left corner
        elif (
            x_screen <= settings.get("user.clickless_mouse_radius") * 3.5
            and y_screen + settings.get("user.clickless_mouse_radius") * 3.25 >= self.screen.height
        ):
            # print("case 3")
            self.set_horizontal_button_positions_and_bounds(x, y, True, True)

        # bottom right corner
        elif (
            x_screen + settings.get("user.clickless_mouse_radius") * 3.5 >= self.screen.width
            and y_screen + math.ceil(settings.get("user.clickless_mouse_radius") * 3.25) >= self.screen.height
        ):
            # print("case 4")
            self.set_horizontal_button_positions_and_bounds(x, y, False, True)

        # bottom edge, sufficient space to draw to the right
        elif (
            y_screen + math.ceil(settings.get("user.clickless_mouse_radius") * 3.25) >= self.screen.height
            and x_screen
            + math.ceil(settings.get("user.clickless_mouse_radius") * len(self.get_horizontal_button_order()) * 2)
            <= self.screen.width
        ):
            # print("case 5")
            self.set_horizontal_button_positions_and_bounds(x, y, True, True)

        # bottom edge, insufficient space to draw to the right
        elif (
            y_screen + math.ceil(settings.get("user.clickless_mouse_radius") * 3.25) >= self.screen.height
            and x_screen
            + math.ceil(settings.get("user.clickless_mouse_radius") * len(self.get_horizontal_button_order()) * 2)
            >= self.screen.width
        ):
            # print("case 6")
            self.set_horizontal_button_positions_and_bounds(x, y, False, True)

        # left edge, not in corner
        elif x_screen <= settings.get("user.clickless_mouse_radius") * 3.5:
            # print("case 7")
            self.set_horizontal_button_positions_and_bounds(x, y, True, False)

        # right edge, not in corner
        elif x_screen + settings.get("user.clickless_mouse_radius") * 3.5 >= self.screen.width:
            # print("case 8")
            self.set_horizontal_button_positions_and_bounds(x, y, False, False)

        # not along edges and not in corner
        # draw all around cursor
        elif (
            not y_screen <= settings.get("user.clickless_mouse_radius") * 3.25
            and x_screen + settings.get("user.clickless_mouse_radius") * 3.5 <= self.screen.width
        ):
            # print("case 9")
            self.button_positions.append(
                dwell_button(
                    x - math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    y - math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    "su" if not self.is_left_down() else "lr",
                )
            )
            self.button_positions.append(
                dwell_button(
                    x + math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    y - math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    "sd" if not self.is_left_down() else "lr",
                )
            )
            self.button_positions.append(
                dwell_button(
                    x,
                    y - math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    "lt" if not self.is_left_down() else "lr",
                )
            )

            self.button_positions.append(
                dwell_button(
                    x - math.ceil(settings.get("user.clickless_mouse_radius") * 3.5),
                    y,
                    "lh" if not self.is_left_down() else "lr",
                )
            )
            self.button_positions.append(
                dwell_button(
                    x - math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    y + math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    "ld" if not self.is_left_down() else "lr",
                )
            )

            self.button_positions.append(
                dwell_button(
                    x,
                    y + math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    "l" if not self.is_left_down() else "lr",
                )
            )

            self.button_positions.append(
                dwell_button(
                    x + math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    y + math.ceil(settings.get("user.clickless_mouse_radius") * 2.25),
                    "r" if not self.is_left_down() else "lr",
                )
            )

            action = "ka" if settings.get("user.clickless_mouse_auto_hide") >= 1 else "x"
            self.button_positions.append(
                dwell_button(x + math.ceil(settings.get("user.clickless_mouse_radius") * 3.5), y, action)
            )

            self.y_min = y - math.ceil(settings.get("user.clickless_mouse_radius") * 5)
            self.y_max = y + math.ceil(settings.get("user.clickless_mouse_radius") * 5)
            self.x_min = x - math.ceil(settings.get("user.clickless_mouse_radius") * 5)
            self.x_max = x + math.ceil(settings.get("user.clickless_mouse_radius") * 5)

        # top edge, sufficient space to the right
        elif (
            y_screen <= settings.get("user.clickless_mouse_radius") * 3.25
            and x_screen + settings.get("user.clickless_mouse_radius") * 3.5 <= self.screen.width
            and x_screen
            + math.ceil(settings.get("user.clickless_mouse_radius") * len(self.get_horizontal_button_order()) * 2)
            <= self.screen.width
        ):
            # print("case 10")
            self.set_horizontal_button_positions_and_bounds(x, y, True, False)

        # top edge, insufficient space to the right
        elif (
            x_screen + settings.get("user.clickless_mouse_radius") * 3.5 <= self.screen.width
            and (
                x_screen
                + math.ceil(
                    settings.get("user.clickless_mouse_radius") * len(self.get_horizontal_button_order()) * 2
                )
                >= self.screen.width
            )
            and y_screen <= settings.get("user.clickless_mouse_radius") * 3.25
        ):
            # print("case 11")
            self.set_horizontal_button_positions_and_bounds(x, y, False, False)

        else:
            print("not handled: {},{}".format(x, y))

        # print(self.button_positions)

    def update(self):
        # print("update")
        x, y = ctrl.mouse_pos()
        now = time.perf_counter()
        # print("({},{})".format(x, y))
        if self.state == STATE_MOUSE_IDLE:
            # print("idle")
            if self.suppress_next_update:
                self.suppress_next_update = False
                self.x, self.y = ctrl.mouse_pos()
                return
            elif math.fabs(self.x - x) > 1 or math.fabs(self.y - y) > 1:
                self.x, self.y = ctrl.mouse_pos()
                self.state = STATE_MOUSE_MOVING

        elif self.state == STATE_MOUSE_MOVING:
            # print("moving")

            if x == self.x and y == self.y:
                self.x, self.y = ctrl.mouse_pos()
                self.last_time = now
                self.state = STATE_MOUSE_STOPPED
            else:
                self.x, self.y = ctrl.mouse_pos()

        elif self.state == STATE_MOUSE_STOPPED:
            # print("stopped")

            if x == self.x and y == self.y:
                if now - self.last_time >= settings.get("user.clickless_mouse_auto_hide_time"):
                    self.last_time = now
                    self._dwell_x, self._dwell_y = ctrl.mouse_pos()
                    screen = ui.screen_containing(self.x, self.y)

                    # if the screen is cached, it won't always appear over
                    # certain windows
                    if True:  # screen != self.screen:
                        self.screen = screen
                        if self.mcanvas:
                            self.mcanvas.close()
                            self.mcanvas = None
                        self.mcanvas = canvas.Canvas.from_screen(self.screen)
                    self.x, self.y = ctrl.mouse_pos()
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
                if (x <= b.x + settings.get("user.clickless_mouse_radius") and b.x - settings.get("user.clickless_mouse_radius") <= x) and (
                    y <= b.y + settings.get("user.clickless_mouse_radius") and b.y - settings.get("user.clickless_mouse_radius") <= y
                ):
                    b.hit_check(True)
                    self.last_time = now
                    item_hit = b
                else:
                    b.hit_check(False)

            if (
                settings.get("user.clickless_mouse_auto_hide") >= 1
                and not item_hit
                and now - self.last_time >= settings.get("user.clickless_mouse_auto_hide_time")
                and (self._dwell_x == x or self._dwell_y == y)
            ):
                # update the position to prevent re-display for minor moves within the bounds
                # this may not be preferred.
                if settings.get("user.clickless_mouse_prevent_redisplay_for_minor_motions") >= 1:
                    self.x, self.y = ctrl.mouse_pos()

                self.state = STATE_MOUSE_IDLE

                draw_options = False

            elif item_hit and now - item_hit.last_hit_time >= settings.get("user.clickless_mouse_dwell_time"):
                draw_options = False

                # print("performing action...")
                action = item_hit.action
                if (
                    action != "su"
                    and action != "sd"
                    and action != "ka"
                    and action != "x"
                ):
                    self.suppress_next_update = True
                    ctrl.mouse_move(self.x, self.y)

                if item_hit.action == "lh":
                    # print("left hold")
                    if not self.is_left_down():
                        # print("pressing button 0 down")
                        ctrl.mouse_click(button=left_mouse_button_index, down=True)
                    else:
                        # print("pressing button 0 up")
                        actions.sleep("{}ms".format(settings.get("user.clickless_mouse_release_delay")))
                        ctrl.mouse_click(button=left_mouse_button_index, up=True)

                    # print(str(ctrl.mouse_buttons_down()))
                elif item_hit.action == "lr":
                    if self.is_left_down():
                        actions.sleep("{}ms".format(settings.get("user.clickless_mouse_release_delay")))
                        ctrl.mouse_click(button=left_mouse_button_index, up=True)

                elif item_hit.action == "l":
                    ctrl.mouse_click(button=left_mouse_button_index)

                elif item_hit.action == "ld":
                    ctrl.mouse_click(button=left_mouse_button_index)
                    ctrl.mouse_click(button=left_mouse_button_index)

                elif item_hit.action == "lt":
                    ctrl.mouse_click(button=left_mouse_button_index)
                    ctrl.mouse_click(button=left_mouse_button_index)
                    ctrl.mouse_click(button=left_mouse_button_index)

                elif item_hit.action == "r":
                    ctrl.mouse_click(button=right_mouse_button_index)

                elif item_hit.action == "rh":
                    if right_mouse_button_index not in ctrl.mouse_buttons_down():
                        ctrl.mouse_click(button=right_mouse_button_index, down=True)
                    else:
                        actions.sleep("{}ms".format(settings.get("user.clickless_mouse_release_delay")))
                        ctrl.mouse_click(button=right_mouse_button_index, up=True)
                elif item_hit.action == "su":
                    actions.mouse_scroll(y=-10)
                    draw_options = True

                elif item_hit.action == "sd":
                    actions.mouse_scroll(y=10)
                    draw_options = True
                elif item_hit.action == "ka":
                    draw_options = True
                elif item_hit.action == "x":
                    draw_options = False
                    self.x, self.y = ctrl.mouse_pos()
                    self.state = STATE_MOUSE_IDLE

                if action != "su" and action != "sd" and action != "ka":
                    # print("({},{})".format(self.x, self.y))
                    self.x, self.y = ctrl.mouse_pos()
                    # print("({},{})".format(self.x, self.y))
                    self.state = STATE_MOUSE_IDLE

            elif x > self.x_max or x < self.x_min or y > self.y_max or y < self.y_min:
                draw_options = False
                self.state = STATE_MOUSE_IDLE

            if draw_options:
                if self._dwell_x != x or self._dwell_y != y:
                    self.last_time = now
                    self._dwell_x, self._dwell_y = ctrl.mouse_pos()

                if not self.draw_registered:
                    self.mcanvas.register("draw", self.draw)
                    self.draw_registered = True
            elif self.draw_registered:
                self.mcanvas.unregister("draw", self.draw)
                self.draw_registered = False

    def draw(self, canvas):
        self.draw_options(canvas)

    def draw_options(self, canvas):
        x = self.x
        y = self.y
        paint = canvas.paint
        paint.color = "ff0000dd"
        paint.style = paint.Style.FILL
        # print("{},{}".format(self.x, self.y))
        # print(canvas.rect)
        paint.stroke_width = settings.get("user.clickless_mouse_stroke_width")
        canvas.draw_line(x - settings.get("user.clickless_mouse_radius"), y, x + settings.get("user.clickless_mouse_radius"), y)
        canvas.draw_line(x, y - settings.get("user.clickless_mouse_radius"), x, y + settings.get("user.clickless_mouse_radius"))

        for b in self.button_positions:
            # draw outer circle
            paint.color = "ffffffaa"
            paint.style = paint.Style.STROKE
            canvas.draw_circle(b.x, b.y, settings.get("user.clickless_mouse_radius") + 1)

            # draw inner circle
            paint.color = "000000AA"
            paint.style = paint.Style.FILL
            canvas.draw_circle(b.x, b.y, settings.get("user.clickless_mouse_radius"))

            # draw hit circle
            if b.last_hit_time:
                paint.color = "00FF00"
                paint.style = paint.Style.FILL

                _radius = min(
                    math.ceil(
                        settings.get("user.clickless_mouse_radius")
                        * (time.perf_counter() - b.last_hit_time)
                        / settings.get("user.clickless_mouse_dwell_time")
                    ),
                    settings.get("user.clickless_mouse_radius"),
                )
                canvas.draw_circle(b.x, b.y, _radius)

            canvas.paint.text_align = canvas.paint.TextAlign.CENTER
            text_string = b.action
            paint.textsize = settings.get("user.clickless_mouse_radius")
            paint.color = "ffffffff"

            canvas.draw_text(text_string, b.x, b.y)


cm = clickless_mouse()


@mod.action_class
class Actions:
    def clickless_mouse_toggle():
        """Toggles the click less mouse"""
        cm.toggle()

    def clickless_mouse_enable():
        """Toggles the click less mouse"""
        cm.enable(True)

    def clickless_mouse_disable():
        """Toggles the click less mouse"""
        cm.enable(False)
    
    def clickless_mouse_is_enabled():
        """Returns whether or not the click less mouse is enabled"""
        return cm.enabled
        


# uncomment the following for quick testing
# def on_ready():
#     cm.enable(True)


# app.register("ready", on_ready)
