# """
# Tools for managing window size and position.
# """

# WIP - here are some quirks that need work:
#
# - 'win snap 200 percent' moves window up a bit when it should stay centered. may be a side-effect related to
# talon resize() API behavior, which will not increase height beyond 1625 for some reason...perhaps related to
# the height of the largest of my 3 screens (which is height 1600).
#
# - here's a weird one: I have vscode maximized on my left hand screen and say 'win size one thousand by one thousand',
# first it resizes, as expected, but then jumps to my primary Screen to the right.

from typing import Optional, Tuple

import queue
import logging
import time

from talon import ui, Module, Context, actions, imgui, settings, app, ctrl

# globals
from .compass_control import CompassControl, Direction, compass_direction, NonDualDirection, non_dual_direction

# # turn debug messages on and off
testing: bool = True

win_compass_control = None
compass_control = None
ctx_stop = None

# talon stuff

mod = Module()

TAG_NAME = 'window_tweak_running'
tag = mod.tag(TAG_NAME, desc="Enable stop command during continuous window move/resize.")

# context used to enable/disable window_tweak_running tag
ctx = Context()

setting_move_frequency = mod.setting(
    "win_move_frequency",
    type=str,
    default="40ms",
    desc="The update frequency used when moving a window continuously",
)
setting_resize_frequency = mod.setting(
    "win_resize_frequency",
    type=str,
    default="40ms",
    desc="The update frequency used when resizing a window continuously",
)
setting_move_rate = mod.setting(
    "win_continuous_move_rate",
    type=float,
    default=4.5,
    desc="The target speed, in cm/sec, for continuous move operations",
)
setting_resize_rate = mod.setting(
    "win_continuous_resize_rate",
    type=float,
    default=4.0,
    desc="The target speed, in cm/sec, for continuous resize operations",
)
mod.setting(
    "win_hide_move_gui",
    type=int,
    default=0,
    desc="When enabled, the 'Move/Resize Window' GUI will not be shown for continuous move operations.",
)
mod.setting(
    "win_hide_resize_gui",
    type=int,
    default=0,
    desc="When enabled, the 'Move/Resize Window' GUI will not be shown for continuous resize operations.",
)
mod.setting(
    "win_set_queue_timeout",
    type=float,
    default=0.2,
    desc="How long to wait (in seconds) for talon to signal completion of window move/resize requests.",
)
mod.setting(
    "win_set_retries",
    type=int,
    default=1,
    desc="How many times to retry a timed out talon window move/resize request.",
)
setting_verbose_warnings = mod.setting(
    "win_verbose_warnings",
    type=bool,
    default=False,
    # window move and resize requests are not guaranteed
    desc="Whether to generate warnings for anomalous events.",
)

@imgui.open(y=0)
def win_stop_gui(gui: imgui.GUI) -> None:
    gui.text(f"Say 'window stop' or click below.")
    gui.line()
    if gui.button("Stop moving/resizing"):
        actions.user.win_stop()

@imgui.open(x=2100, y=40)
# @imgui.open(x=4000,y=244)
def _win_show_gui(gui: imgui.GUI) -> None:
    w = ui.active_window()

    gui.text(f"== Window ==")

    gui.text(f"Id: {w.id}")
    gui.spacer()

    x = w.rect.x
    y = w.rect.y
    width = w.rect.width
    height = w.rect.height

    gui.text(f"Top Left: {x, y}")
    gui.text(f"Top Right: {x + width, y}")
    gui.text(f"Bottom Left: {x, y + height}")
    gui.text(f"Bottom Right: {x + width, y + height}")
    gui.text(f"Center: {round(w.rect.center.x), round(w.rect.center.y)}")
    gui.spacer()

    gui.text(f"Width: {round(width)}")
    gui.text(f"Height: {round(height)}")

    gui.line()

    gui.text(f"== Mouse ==")

    gui.text(f"Position: {ctrl.mouse_pos()}")

    gui.line()

    screen = w.screen
    gui.text(f"== Screen ==")
    gui.spacer()

    #gui.text(f"Name: {screen.name}")
    # gui.text(f"DPI: {screen.dpi}")
    # gui.text(f"DPI_x: {screen.dpi_x}")
    # gui.text(f"DPI_y: {screen.dpi_y}")
    #gui.text(f"Scale: {screen.scale}")
    #gui.spacer()

    x = screen.visible_rect.x
    y = screen.visible_rect.y
    width = screen.visible_rect.width
    height = screen.visible_rect.height

    gui.text(f"__Visible Rectangle__")
    gui.text(f"Top Left: {round(x), round(y)}")
    gui.text(f"Top Right: {round(x + width), round(y)}")
    gui.text(f"Bottom Left: {round(x), round(y + height)}")
    gui.text(f"Bottom Right: {round(x + width), round(y + height)}")
    gui.text(f"Center: {round(screen.visible_rect.center.x), round(screen.visible_rect.center.y)}")
    gui.spacer()

    gui.text(f"Width: {round(width)}")
    gui.text(f"Height: {round(height)}")

    gui.spacer()

    x = screen.rect.x
    y = screen.rect.y
    width = screen.rect.width
    height = screen.rect.height

    gui.text(f"__Physical Rectangle__")
    gui.text(f"Top Left: {round(x), round(y)}")
    gui.text(f"Top Right: {round(x + width), round(y)}")
    gui.text(f"Bottom Left: {round(x), round(y + height)}")
    gui.text(f"Bottom Right: {round(x + width), round(y + height)}")
    gui.text(f"Center: {round(screen.rect.center.x), round(screen.rect.center.y)}")
    gui.spacer()

    gui.text(f"Width: {round(width)}")
    gui.text(f"Height: {round(height)}")

    gui.line()

    gui.text(f"Say 'window traits hide' to close this window.")

    gui.line()

    if gui.button("Close"):
        _win_show_gui.hide()

class WinCompassControl:
    @classmethod
    def win_set_rect(cls, old_rect: ui.Rect, rect_id: int, rect_in: ui.Rect) -> Tuple[bool, ui.Rect]:
        """Callback invoked by CompassControl engine for updating the window rect using talon API"""
        start_time = time.time_ns()
        if not rect_in:
            raise ValueError('rect_in is None')

        max_retries = retries = settings.get('user.win_set_retries')
        queue_timeout = settings.get('user.win_set_queue_timeout')

        # rect update code adapted from https://talonvoice.slack.com/archives/C9MHQ4AGP/p1635971780355900
        q = queue.Queue()
        def on_move(event_win: ui.Window) -> None:
            if event_win == w and w.rect != old_rect:
                q.put(1)
                if testing:
                    print(f'_win_set_rect: win position changed')
        #
        def on_resize(event_win: ui.Window) -> None:
            if event_win == w and w.rect != old_rect:
                q.put(1)
                if testing:
                    print(f'_win_set_rect: win size changed')

        # get window handle
        windows = ui.windows()
        for w in windows:
            if w.id == rect_id:
                break
        else:
            if settings.get('user.win_verbose_warnings') != 0:
                logging.warning(f'_win_set_rect: invalid window id "{rect_id}"')
            return False, w.rect

        if testing:
            print(f'_win_set_rect: starting...{old_rect=}, {rect_in=}, {w.rect=}')

        result = False, old_rect

        while retries >= 0:
            event_count = 0
            if (rect_in.x, rect_in.y) != (w.rect.x, w.rect.y):
                # print(f'_win_set_rect: register win_move')
                ui.register('win_move', on_move)
                event_count += 1
            if (rect_in.width, rect_in.height) != (w.rect.width, w.rect.height):
                # print(f'_win_set_rect: register win_resize')
                ui.register('win_resize', on_resize)
                event_count += 1
            if event_count == 0:
                # sometimes the queue get below times out, yet by the time we loop around here
                # for a retry, the set operation has completed successfully. then, the checks above
                # fall through to this block. so, the result we return is based on whether this is
                # our first time through the loop or not.
                success = retries < max_retries

                # no real work to do
                result = success, rect_in

                if testing:
                    print('_win_set_rect: nothing to do, window already matches given rect.')

                break

            # do it to it
            start_time_rect = time.time_ns()
            w.rect = rect_in.copy()
            try:
                # for testing
                #raise queue.Empty()
                #raise Exception('just testing')

                q.get(timeout=queue_timeout)
                if event_count == 2:
                    q.get(timeout=queue_timeout)

            except queue.Empty:
                if testing:
                    print('_win_set_rect: timed out waiting for window update.')

                if retries > 0:
                    if testing:
                        print('_win_set_rect: retrying after time out...')
                    retries -= 1
                    continue
                else:
                    if testing:
                        print('_win_set_rect: no more retries, failed')

                    # no more retries
                    break
            else:
                if testing:
                    print(f'_win_set_rect: before: {old_rect}')
                    print(f'_win_set_rect: requested: {rect_in}')
                    print(f'_win_set_rect: after: {w.rect}')

                position_matches_request = (rect_in.x, rect_in.y) == (w.rect.x, w.rect.y)
                size_matches_request = (rect_in.width, rect_in.height) == (w.rect.width, w.rect.height)
                if not position_matches_request or not size_matches_request:
                    if False and app.platform == 'linux':
                        if testing:
                            print('_win_set_rect: linux - timed out waiting for window update.')

                        if retries > 0:
                            if testing:
                                print('_win_set_rect: linux - retrying after time out...')
                            retries -= 1
                            continue
                        else:
                            if testing:
                                print('_win_set_rect: linux - no more retries, failed')

                            # no more retries
                            break
                    else:
                        # need to pass rect_id and old_rect here so they can be saved for 'win revert' usage
                        raise compass_control.RectUpdateError(rect_id=rect_id, initial=old_rect, requested=rect_in, actual=w.rect)

                else:
                    result = True, w.rect

                    # done with retry loop
                    break
            finally:
                ui.unregister('win_move',   on_move)
                ui.unregister('win_resize', on_resize)

        elapsed_time_ms = (time.time_ns() - start_time) / 1e6
        if testing:
            print(f'_win_set_rect: done ({elapsed_time_ms} ms)')

        return result

    def win_stop(self) -> None:
        """Callback invoked by CompassControl engine after stopping a continuous operation"""
        win_stop_gui.hide()

def on_ready():
    """Callback invoked by Talon, where we populate our global objects"""
    global win_compass_control, compass_control, ctx_stop

    # if testing:
    #     print(f"on_ready: {settings.get('user.win_continuous_move_rate')=}")

    win_compass_control= WinCompassControl()

    compass_control_settings = {
        '_continuous_move_frequency_str':   setting_move_frequency,
        '_continuous_resize_frequency_str': setting_resize_frequency,
        '_continuous_move_rate':            setting_move_rate,
        '_continuous_resize_rate':          setting_resize_rate,
        '_verbose_warnings':                setting_verbose_warnings
    }
    compass_control= CompassControl(
        TAG_NAME,
        win_compass_control.win_set_rect,
        win_compass_control.win_stop,
        compass_control_settings,
        testing
    )

    # context containing the stop command, enabled only when a continuous move/resize is running
    ctx_stop = Context()
    ctx_stop.matches = fr"""
    tag: user.{TAG_NAME}
    """
    @ctx_stop.action_class("user")
    class WindowTweakActions:
        """
        # Commands for controlling continuous window move/resize operations
        """
        def win_stop() -> None:
            "Stops current window move/resize operation"
            compass_control.continuous_stop()

app.register("ready", on_ready)

@mod.action_class
class Actions:
    def win_show() -> None:
        "Shows information about current window position and size"
        _win_show_gui.show()

    def win_hide() -> None:
        "Hides the window information window"
        _win_show_gui.hide()

    def win_stop() -> None:
        "Module action declaration for stopping current window move/resize operation"
        compass_control.continuous_stop()

    def win_move(direction: Optional[Direction] = None) -> None:
        "Move window in small increments in the given direction, until stopped"

        if not direction:
            direction = compass_direction(['center'])

        w = ui.active_window()

        compass_control.mover.continuous_init(w.rect, w.id, w.screen.visible_rect, w.screen.dpi_x, w.screen.dpi_y, direction)

        if settings.get('user.win_hide_move_gui') == 0:
            win_stop_gui.show()

    def win_move_absolute(x: float, y: float, region: Optional[Direction] = None) -> None:
        "Move window to given absolute position, centered on the point indicated by the given region"

        w = ui.active_window()

        compass_control.mover.move_absolute(w.rect, w.id, x, y, region)

    def win_move_to_pointer(region: Optional[NonDualDirection] = non_dual_direction(['north', 'west'])):
        "Move window to pointer position, centered on the point indicated by the given region"

        w = ui.active_window()

        compass_control.mover.resize_to_pointer(w.rect, w.id, w.screen.visible_rect, region)

    def win_stretch(direction: Optional[Direction] = None) -> None:
        "Stretch window in small increments until stopped, optionally in the given direction"

        if not direction:
            direction = compass_direction(['center'])

        w = ui.active_window()
        compass_control.sizer.continuous_init(w.rect, w.id, w.screen.visible_rect, 1, w.screen.dpi_x, w.screen.dpi_y, direction)

        if settings.get('user.win_hide_resize_gui') == 0:
            win_stop_gui.show()

    def win_shrink(direction: Optional[Direction] = None) -> None:
        "Shrink window in small increments until stopped, optionally in the given direction"
        w = ui.active_window()

        if not direction:
            direction = compass_direction(['center'])

        compass_control.sizer.continuous_init(w.rect, w.id, w.screen.visible_rect, -1, w.screen.dpi_x, w.screen.dpi_y, direction)

        if settings.get('user.win_hide_resize_gui') == 0:
            win_stop_gui.show()

    def win_resize_absolute(target_width: float, target_height: float, region: Optional[Direction] = None) -> None:
        "Size window to given absolute dimensions, optionally by stretching/shrinking in the direction indicated by the given region"

        if not region:
            region = compass_direction(['center'])

        w = ui.active_window()

        compass_control.sizer.resize_absolute(w.rect, w.id, target_width, target_height, region)

    def win_resize_to_pointer(nd_direction: NonDualDirection) -> None:
        "Stretch or shrink window to pointer position, centered on the point indicated by the given region"

        w = ui.active_window()

        compass_control.sizer.resize_to_pointer(w.rect, w.id, w.screen.visible_rect, nd_direction)

    def win_move_pixels(distance: int, direction: Optional[Direction] = None) -> None:
        "Move window some number of pixels"

        if not direction:
            direction = compass_direction(['center'])

        w = ui.active_window()

        delta_width, delta_height = compass_control.get_component_dimensions(w.rect, w.id, w.screen.visible_rect, distance, direction, 'move')

        return compass_control.mover.move_pixels_relative(w.rect, w.id, w.screen.visible_rect, delta_width, delta_height, direction)

    def win_move_percent(percent: float, direction: Optional[Direction] = None) -> None:
        "Move window some percentage of the current size"

        if not direction:
            direction = compass_direction(['center'])

        w = ui.active_window()

        delta_width, delta_height = compass_control.get_component_dimensions_by_percent(w.rect, w.id, w.screen.visible_rect, percent, direction, 'move')

        return compass_control.mover.move_pixels_relative(w.rect, w.id, w.screen.visible_rect, delta_width, delta_height, direction)

    def win_resize_pixels(distance: int, direction: Optional[Direction] = None) -> None:
        "Change window size by pixels"
        w = ui.active_window()

        if not direction:
            direction = compass_direction(['center'])

        delta_width, delta_height = compass_control.get_component_dimensions(w.rect, w.id, w.screen.visible_rect, distance, direction, 'resize')

        if testing:
            print(f'win_resize_pixels: {delta_width=}, {delta_height=}')

        compass_control.sizer.resize_pixels_relative(w.rect, w.id, w.screen.visible_rect, delta_width, delta_height, direction)

    def win_resize_percent(percent: float, direction: Optional[Direction] = None) -> None:
        "Change window size by a percentage of current size"

        if not direction:
            direction = compass_direction(['center'])

        w = ui.active_window()

        delta_width, delta_height = compass_control.get_component_dimensions_by_percent(w.rect, w.id, w.screen.visible_rect, percent, direction, 'resize')

        if testing:
            print(f'win_resize_percent: {delta_width=}, {delta_height=}')

        compass_control.sizer.resize_pixels_relative(w.rect, w.id, w.screen.visible_rect, delta_width, delta_height, direction)

    def win_snap_percent(percent: int) -> None:
        "Center window and change size to given percentage of parent screen (in each direction)"

        direction = compass_direction(['center'])

        w = ui.active_window()

        compass_control.snap(w.rect, w.id, w.screen.visible_rect, percent, direction)

    def win_revert() -> None:
        "Restore current window's last remembered size and position"

        w = ui.active_window()
        compass_control.revert(w.rect, w.id)

    def win_test_bresenham(num: int) -> None:
        "Test modified bresenham algo"

        if num == 1:
            compass_control.mover.test_bresenham()
