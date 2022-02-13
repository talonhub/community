# """
# Tools for managing the size and position of rectangles using cardinal and ordinal directions, e.g. North, Southwest, etc.
#
# See window_tweak.talon and window_tweak.py for example of usage.
#
# Ideas:
# - Windows on a screen (window_tweak.py)
# - Pieces on a game board
# - Elements of a diagram
# - Moving 3D objects within a 2D view frame.
# - Tiles in a visual programming environment (e.g. Grasshopper 3D)
# - Panes of an IDE window
#
# Continuous move/resize machinery adapted from mouse.py.
# """

# TODO
# -perhaps we shouldn't be using 'win move in'/'win move out' because, for 3D, it would
# be most natural to use in and out for the z axis...
# 'win park'/'win fly'
# 'win seek'/'win flee'
# 'win suck'/'win blow'
# 'win here'/'win there'
# 'win move central'/'win move distal'
# 'win move near'/'win move far'
#
# - could implement actions to mirror window's position about some axis


# WIP - here are some quirks that need work:
#
# - continuous operations are sometimes choppy and randomly stop, due to API delay and timeouts.
# increasing the queue time out doesn't seem to help (this may be more noticeable when debug logging
# is enabled). see https://github.com/talonvoice/talon/issues/470
#
# - timeout issues with 'win shrink' automatic stop mechanisms. both mechanisms I've implemented are hindered
# by the API timeouts that happen when the window hits a minimum size. the 'change checking' approach also
# fails because rect assignment will sometimes partially fail even before the window has reached its
# minimum size. can repro with 'win shrink' command. see use_resize_history_for_shrink and
# use_change_check_for_shrink.
#
# - on my Kubuntu 20.10 system, diagonal continuous stretch stops when the first diminension is clipped rather
# then continuing along the second diminesion until that limit is reached. this is because the visible rect size
# is the same as the physical rect size even though they are not really the same. this feature started working as
# expected after I enabled auto-hide for the 'taskbar'.
#
# Kubuntu 20.10: 'win stretch' stops at first limit and at other times, because set_rect()
# result does not match request. seems to happen randomly...maybe not, it just happened
# again at about the same place.
#
# Kubuntu 20.10: move in/out is noticeably slower than other operations
#
# - 'win shrink west' fails when the window is on my left-most screen and is off the left edge of the
# screen, at the end it of the shrink it jumps to the left edge of the screen to the right. same thing
# swapping west for east, left for right, etc.
#
#
# - behavior while stretching or shrinking a rectangle which is not fully contained by the parent
# rectangle is a bit funky...not terrible, I guess...but could be improved.
#
# - is this a bug, the fact that the settings below seem to be constantly changing? see 'settings register' below
# and code.py.
# 2021-12-08 22:59:37    IO CompassControl.refresh_settings: arg='user.code_public_function_formatter'
# 2021-12-08 22:59:37    IO CompassControl.refresh_settings: arg=<talon.scripting.types.SettingDecl.NoValueType object at 0x0000000005B7C160>
# 2021-12-08 22:59:37    IO CompassControl.Mover.refresh_settings: args=('user.code_public_function_formatter', <talon.scripting.types.SettingDecl.NoValueType object at 0x0000000005B7C160>)
# 2021-12-08 22:59:37    IO refresh_settings: self.settings_map={'continuous_move_frequency_str': 'user.win_move_frequency', 'continuous_resize_frequency_str': 'user.win_resize_frequency', 'continuous_move_rate': 'user.win_continuous_move_rate', 'continuous_resize_rate': 'user.win_continuous_resize_rate', 'verbose_warnings': 'user.win_verbose_warnings'}
# 2021-12-08 22:59:37    IO refresh_settings: args: args=('user.code_public_variable_formatter', <talon.scripting.types.SettingDecl.NoValueType object at 0x0000000005B7C160>)
# 2021-12-08 22:59:37    IO CompassControl.refresh_settings: arg='user.code_public_variable_formatter'
# 2021-12-08 22:59:37    IO CompassControl.refresh_settings: arg=<talon.scripting.types.SettingDecl.NoValueType object at 0x0000000005B7C160>
# 2021-12-08 22:59:37    IO CompassControl.Mover.refresh_settings: args=('user.code_public_variable_formatter', <talon.scripting.types.SettingDecl.NoValueType object at 0x0000000005B7C160>)
# 2021-12-08 22:59:37    IO CompassControl.Sizer.refresh_settings: args=('user.code_public_variable_formatter', <talon.scripting.types.SettingDecl.NoValueType object at 0x0000000005B7C160>)
# 2021-12-08 22:59:37    IO refresh_settings: self.settings_map={'continuous_move_frequency_str': 'user.win_move_frequency', 'continuous_resize_frequency_str': 'user.win_resize_frequency', 'continuous_move_rate': 'user.win_continuous_move_rate', 'continuous_resize_rate': 'user.win_continuous_resize_rate', 'verbose_warnings': 'user.win_verbose_warnings'}
# 2021-12-08 22:59:37    IO refresh_settings: args: args=('user.code_protected_function_formatter', <talon.scripting.types.SettingDecl.NoValueType object at 0x0000000005B7C160>)

from typing import Any, Callable, Dict, List, Tuple, Optional, Iterator

import math
import logging
import threading
import time

from talon import ui, Module, ctrl, cron, Context, settings
from talon.types.point import Point2d

## talon stuff

mod = Module()

# # context used to enable/disable the tag for controlling whether the 'stop' command is active
ctx = Context()

# taken from https: //talon.wiki/unofficial_talon_docs/#captures
#
# a type for representing compass directions
Direction = Dict[str, bool]
#
@mod.capture(rule="in | out | center | ((north | south) [(east | west)] | east | west)")
def compass_direction(m: List) -> Direction:
    """
    Matches on a basic compass direction to return which keys should
    be pressed.
    """
    result = {}

    if "in" in m or "center" in m:
        result["up"] = result["down"] = result["right"] = result["left"] = False
    elif "out" in m:
        result["up"] = result["down"] = result["right"] = result["left"] = True
    else:
        result = {
            "up": "north" in m,
            "down": "south" in m,
            "right": "east" in m,
            "left": "west" in m
        }

    return result

# a type for representing "non-dual" directions
NonDualDirection = Dict[str, bool]

# mod.list("non_dual_direction", desc="Horizontal, vertical or diagonal")
# ctx.lists["user.non_dual_direction"] = [ 'horizontal', 'flat', 'vertical', 'sharp', 'diagonal', 'slant' ]
@mod.capture(rule="horizontal | flat | vertical | sharp | diagonal | slant")
def non_dual_direction(m: List) -> NonDualDirection:
    """
    Matches on a basic compass direction to return which keys should
    be pressed.
    """
    result = {
        "horizontal": "horizontal" in m or "flat" in m,
        "vertical": "vertical" in m or "sharp" in m,
        "diagonal": "diagonal" in m or "slant" in m,
    }

    return result

class CompassControl:

    def __init__(self, continuous_tag_name: str, set_method: Callable, stop_method: Callable, settings_map: Dict, testing: bool):

        # turn debug messages on and off
        self.testing = testing

        # the method to call to actually set the new size and position of the given rectangle
        self.set_method = set_method

        # remember the last rectangle so we can always revert back to it later
        self.last_rect: Dict = dict()

        # tag used to enable/disable commands used to manage continuous move/resize operations, e.g. 'stop'
        self.continuous_tag_name: str = continuous_tag_name
        self.continuous_tag_name_qualified: str = 'user.' + self.continuous_tag_name

        # the method to call when stopping a continuous move/resize operation, so the caller can do any additional tasks, as required
        self.continuous_stop_method = stop_method

        self.continuous_mutex: threading.RLock = threading.RLock()

        # variables for managing continuous move/resize operations
        self.continuous_iteration: int = 0
        self.continuous_direction: Direction = None
        self.continuous_old_rect: ui.Rect = None
        self.continuous_rect: ui.Rect = None
        self.continuous_rect_id: int = None
        self.continuous_parent_rect: ui.Rect = None

        # talon settings
        self._verbose_warnings: int = None

        # the control uses a mover instance and a sizer instance
        self.mover: CompassControl.Mover = CompassControl.Mover(self, settings_map, testing)
        self.sizer: CompassControl.Sizer = CompassControl.Sizer(self, settings_map, testing)

        self.settings_map = settings_map
        self.refresh_map =  {
                talon_setting.path: local_name
                            for local_name, talon_setting in settings_map.items()
                                                                if hasattr(self, local_name) }
        self.refresh_settings()
        # catch updates
        settings.register("", self.refresh_settings)

        # print(f'CompassControl.__init__: {move_rate=}')

    @property
    def verbose_warnings(self):
        if self._verbose_warnings is None:
            self._verbose_warnings = self.settings_map['_verbose_warnings'].get()
        return self._verbose_warnings

    def refresh_settings(self, *args):
        # if self.testing:
        #     # print(f'refresh_settings: {self.settings_map=}')
        #     print(f'CompassControl.refresh_settings: args: {args=}')

        caller_id = 'CompassControl'
        if args:
            CompassControl._update_setting(self, caller_id, args)
        else:
            CompassControl._update_all_settings(self, caller_id)

        self.mover.refresh_settings(args)
        self.sizer.refresh_settings(args)

    @classmethod
    def _update_all_settings(cls, caller, caller_id: str) -> None:
        # fetch all our settings
        for local_name, talon_setting in caller.settings_map.items():
            if hasattr(caller, local_name):
                caller.__setattr__(local_name, talon_setting.get())

                print(f'{caller_id}._update_all_settings: received updated value for {talon_setting.path}: {getattr(caller, local_name, None)}')

    @classmethod
    def _update_setting(cls, caller, caller_id: str, args):
        # fetch updated settings
        talon_name = args[0]
        try:
            local_name = caller.refresh_map[talon_name]
        except KeyError:
            # not one of our settings
            pass
        else:
            caller.__setattr__(local_name, args[1])

            print(f'{caller_id}._update_setting: received updated value for {talon_name}: {getattr(caller, local_name, None)}')

    # error thrown when a move or resize request is not completely successful
    class RectUpdateError(Exception):
        def __init__(self, rect_id, initial,  requested, actual):
            # along with error reporting, these values are used to update last_rect in support of revert functionality
            self.rect_id = rect_id
            self.initial = initial
            self.requested = requested
            self.actual = actual

    def _handle_rect_update_error(self, e: RectUpdateError) -> None:
        if self.verbose_warnings:
            position_matches_request = (e.requested.x, e.requested.y) == (e.actual.x, e.actual.y)
            size_matches_request = (e.requested.width, e.requested.height) == (e.actual.width, e.actual.height)

            if not position_matches_request:
                logging.warning(f'after update, rectangle position does not exactly match request: {e.requested.x, e.requested.y} -> {e.actual.x, e.actual.y}')

            if not size_matches_request:
                logging.warning(f'after update, rectangle size does not exactly match request: {e.requested.width, e.requested.height} -> {e.actual.width, e.actual.height}')

        self._save_last_rect(e.rect_id, e.initial)

    class Mover:
        def __init__(self, compass_control, settings_map: Dict, testing: bool):
            # ref to parent
            self.compass_control: CompassControl = compass_control

            # turn debug messages on and off
            self.testing = testing

            # variables used during continuous move/resize operations
            self.continuous_width_increment: int = 0
            self.continuous_height_increment: int = 0
            self.continuous_job: Any = None

            self.continuous_target_x: float = None
            self.continuous_target_y: float = None

            # bresenham generator used for 'move to center' operations
            self.continuous_bres: Iterator[(int, int)] = None

            # talon settings
            self._verbose_warnings: int = None
            self._continuous_move_frequency_str: str = ""
            self._continuous_move_frequency: float = 0
            self._continuous_move_rate: float = 0

            self.settings_map = settings_map
            self.refresh_map =  {
                talon_setting.path: local_name
                            for local_name, talon_setting in settings_map.items()
                                                                if hasattr(self, local_name) }

            # if self.testing:
            #     print(f'Mover.__init__: {rate=}')

        @property
        def verbose_warnings(self):
            if self._verbose_warnings is None:
                self._verbose_warnings = self.settings_map['_verbose_warnings'].get()
            return self._verbose_warnings

        @property
        def continuous_move_frequency_str(self):
            if self._continuous_move_frequency_str is None:
                self._continuous_move_frequency_str = self.settings_map['_continuous_move_frequency_str'].get()
            return self._continuous_move_frequency_str

        @property
        def continuous_move_frequency(self):
            if self._continuous_move_frequency is None:
                self._continuous_move_frequency = float((self.continuous_move_frequency_str)[:-2])
            return self._continuous_move_frequency

        @property
        def continuous_move_rate(self):
            if not self._continuous_move_rate is None:
                self._continuous_move_rate = self.settings_map['_continuous_move_rate'].get()
            return self._continuous_move_rate

        # update settings for managing continuous move/resize operations
        def refresh_settings(self, args):
            # if self.testing:
            #     print(f'CompassControl.Mover.refresh_settings: {args=}')

            caller_id = 'CompassControl.Mover'
            if args:
                self.compass_control._update_setting(self, caller_id, args)
            else:
                self.compass_control._update_all_settings(self, caller_id)

            # force a refresh for this value
            self._continuous_move_frequency = None

        def continuous_init(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect,
                                                dpi_x: float, dpi_y: float, direction: Direction) -> None:
            """Initialize continuous operation"""
            with self.compass_control.continuous_mutex:
                if self.continuous_job:
                    if self.testing:
                        print(f'init_continuous: {self.continuous_job=}')
                    logging.warning('cannot start a move job when one is already running')
                    return

                self.compass_control._continuous_reset()

                self.compass_control.continuous_old_rect = rect.copy()
                self.compass_control.continuous_rect = rect
                self.compass_control.continuous_rect_id = rect_id
                self.compass_control.continuous_parent_rect = parent_rect
                self.compass_control.continuous_direction = direction

                # print(f'init_continuous: {self.continuous_frequency_str=}')
                self.continuous_width_increment, self.continuous_height_increment = self.compass_control._get_continuous_parameters(
                                    rect, rect_id, parent_rect, self.continuous_move_rate, self.continuous_move_frequency,
                                        dpi_x, dpi_y, direction, 'move'
                            )

                if self.testing:
                    print(f'init_continuous: {self.continuous_width_increment=}, {self.continuous_height_increment=}')

                direction_count = sum(self.compass_control.continuous_direction.values())
                if direction_count == 0 or direction_count == 4:    # move in/out (special case)
                    # follow path from rectangle center to the target point

                    x0 = rect.x
                    y0 = rect.y

                    x1, y1 = self.compass_control.get_target_point(rect, rect_id, parent_rect, direction)

                    if self.testing:
                        print(f'init_continuous: bresenham line - {x0, y0} -> {x1, y1}')

                    self.continuous_target_x = x1
                    self.continuous_target_y = y1

                    # note that this is based on the line from rectangle center to the target point, resulting
                    # coordinates will have to be translated to top left to set rectangle position, etc.
                    self.continuous_bres = self.compass_control.bresenham(x0, y0, x1, y1)

                    # discard initial point (we're already there)
                    next(self.continuous_bres)

                    # if we're already there, zero the increment
                    if x0 == x1:
                        self.continuous_width_increment = 0
                    if y0 == y1:
                        self.continuous_height_increment = 0

                self._continuous_start()

        def _continuous_start(self) -> None:
            """Commence continuous operation"""
            with self.compass_control.continuous_mutex:
                ctx.tags = [self.compass_control.continuous_tag_name_qualified]
                self.continuous_job = cron.interval(self.continuous_move_frequency_str, self._continuous_helper)
                if self.testing:
                    print(f'_start_continuous: {self.continuous_job=}')

        def _continuous_helper(self) -> None:
            """This is the engine that handles each continuous iteration"""
            def _move_it(rect: ui.Rect, rect_id: int, parent_rect: ui.Rect,
                            delta_x: float, delta_y: float, direction: Direction) -> Tuple[bool, ui.Rect]:
                result, rect, horizontal_limit_reached, vertical_limit_reached = self.move_pixels_relative(
                                        rect, rect_id, parent_rect, delta_x, delta_y, self.compass_control.continuous_direction)
                if not result:
                    if self.testing:
                        print(f'continuous_helper: rectangle move failed. {result=}, {rect=}, {horizontal_limit_reached=}, {vertical_limit_reached=}')
                elif (horizontal_limit_reached and vertical_limit_reached): # both limits reached, we are done
                    if self.testing:
                        print(f'continuous_helper: rectangle move is complete. {result=}, {rect=}, {horizontal_limit_reached=}, {vertical_limit_reached=}')
                    self.continuous_width_increment = self.continuous_height_increment = 0
                    result = True
                else: # check whether one of the limits has been reached
                    if horizontal_limit_reached:
                        self.continuous_width_increment = 0
                    elif vertical_limit_reached:
                        self.continuous_height_increment = 0

                    result = True

                return result, rect

            def _continuous_move_in_out(self, _move_it: Callable, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect):
                initial_x = rect.x
                initial_y = rect.y
                cumulative_delta_x = cumulative_delta_y = 0
                # we break out of this loop for three reasons:
                # 1. if we reach the target coordinates (exhaust bresenham iterator)
                # 2. if we fail to actually move to the intended coordinates for some reason
                # 3. if we move past the current maximum distance (horizontally or vertically) for one iteration
                direction_count = sum(self.compass_control.continuous_direction.values())
                while (
                        # for move in, we only stop after hitting both limits
                        (direction_count == 0 and (self.continuous_width_increment or self.continuous_height_increment)) or
                        # for move out, we stop after hitting the first limit
                        (direction_count == 4 and self.continuous_width_increment and self.continuous_height_increment)
                    ):

                    if self.testing:
                        print(f'continuous_helper: current top left = {rect.x, rect.y}')

                    (x, y) = (round(rect.x), round(rect.y))
                    try:
                            x, y = next(self.continuous_bres)
                    except StopIteration:
                        if self.testing:
                            print(f'continuous_helper: StopIteration')

                        self.compass_control.continuous_stop()

                        # return
                        break

                    if self.testing:
                        print(f'continuous_helper: new top left = {x, y}')

                    delta_x = abs(x - rect.x)
                    if self.continuous_target_x < x:
                        # keep everything moving in the right direction
                        delta_x *= -1

                    delta_y = abs(y - rect.y)
                    if self.continuous_target_y < y:
                        # keep everything moving in the right direction
                        delta_y *= -1

                    if self.testing:
                        print(f'continuous_helper: stepping from {rect.x, rect.y} to {x, y}, {delta_x=}, {delta_y=}')

                    # print(f'continuous_helper: before move {rect=}')
                    result, rect = _move_it(rect, rect_id, parent_rect, delta_x, delta_y,
                                                                self.compass_control.continuous_direction)
                    self.compass_control.continuous_rect = rect

                    # check pass or fail
                    if not result:
                        if self.testing:
                            print(f'continuous_helper: move failed')
                        self.compass_control.continuous_stop()
                        break
                        # print(f'continuous_helper: after move {rect=}')

                    # check whether we've gone far enough for this iteration
                    #
                    # horizontal check
                    cumulative_delta_x = abs(rect.x - initial_x)
                    if self.testing:
                        print(f'continuous_helper: {cumulative_delta_x=}, {self.continuous_width_increment=}')
                    if self.continuous_width_increment != 0 and cumulative_delta_x >= abs(self.continuous_width_increment):
                        if self.testing:
                            print(f'continuous_helper: moved horizontally as far as possible for current iteration, stopping')
                        break
                    #
                    # vertical check
                    cumulative_delta_y = abs(rect.y - initial_y)
                    if self.testing:
                        print(f'continuous_helper: {cumulative_delta_y=}, {self.continuous_height_increment=}')
                    if self.continuous_height_increment != 0 and cumulative_delta_y >= abs(self.continuous_height_increment):
                        if self.testing:
                            print(f'continuous_helper: moved vertically as far as possible for current iteration, stopping')
                        break

                return rect

            start_mutex_wait = time.time_ns()
            with self.compass_control.continuous_mutex:
                iteration = self.compass_control.continuous_iteration

                elapsed_time_ms = (time.time_ns() - start_mutex_wait) / 1e6
                if self.testing:
                    print(f'continuous_helper: iteration {iteration} mutex wait ({elapsed_time_ms} ms)')

                start_time = time.time_ns()

                # if self.testing:
                #     print(f'continuous_helper: current thread = {threading.get_native_id()}')

                if not self.continuous_job:
                    # seems sometimes this gets called while the job is being canceled, so just return in that case
                    return

                rect = self.compass_control.continuous_rect
                rect_id = self.compass_control.continuous_rect_id
                parent_rect = self.compass_control.continuous_parent_rect

                if self.testing:
                    print(f'continuous_helper: starting iteration {iteration} - {rect=}')

                direction_count = sum(self.compass_control.continuous_direction.values())
                if (
                    # if there's no work to do...
                    (not (self.continuous_width_increment or self.continuous_height_increment)) or
                    # for 'move out' operations, we stop if one of the two increments is zero
                    (direction_count == 4 and not (self.continuous_width_increment and self.continuous_height_increment))
                ):
                    if self.testing:
                        print(f'continuous_helper: rectangle move failed. {rect=}')
                    self.compass_control.continuous_stop()
                else:
                    # we have work to do
                    if direction_count == 1 or direction_count == 2:
                        result, rect = _move_it(rect, rect_id, parent_rect, self.continuous_width_increment,
                                                        self.continuous_height_increment, self.compass_control.continuous_direction)
                        self.compass_control.continuous_rect = rect
                        if not result:
                            if self.testing:
                                print(f'continuous_helper: move failed')
                            self.compass_control.continuous_stop()
                    else:
                        # move in/out
                        rect = _continuous_move_in_out(self, _move_it, rect, rect_id, parent_rect)

                elapsed_time_ms = (time.time_ns() - start_time) / 1e6
                if self.testing:
                    print(f'continuous_helper: iteration {iteration} done ({elapsed_time_ms} ms)')
                if elapsed_time_ms > self.continuous_move_frequency:
                    if self.compass_control.verbose_warnings != 0:
                        logging.warning(f'continuous_helper: move iteration {iteration} took {elapsed_time_ms}ms, longer than the current move_frequency setting. actual rate may not match the continuous_rate setting.')

                self.compass_control.continuous_iteration += 1

        def _continuous_reset(self) -> None:
            """Reset variables used during continuous operations"""
            with self.compass_control.continuous_mutex:
                self.continuous_width_increment = 0
                self.continuous_height_increment = 0
                self.continuous_job = None
                self.continuous_target_x = None
                self.continuous_target_y = None
                self.continuous_bres = None

        def move_pixels_relative(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect,
                                        delta_x: float, delta_y: float, direction: Direction) -> Tuple[ui.Rect, bool, bool]:
            """Move rectangle in given direction as indicated by the given delta values"""

            def _get_new_coordinates(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, x: float, y: float,
                                                                delta_x: float, delta_y: float, direction: Direction):
                horizontal_limit_reached = vertical_limit_reached = False

                direction_count = sum(direction.values())
                if direction_count == 1 or direction_count == 2:
                    if direction["left"]:
                        x -= delta_x

                    if direction["right"]:
                        x += delta_x

                    if direction["up"]:
                        y -= delta_y

                    if direction["down"]:
                        y += delta_y

                    new_x, new_y, horizontal_limit_reached, vertical_limit_reached = self._clip_to_fit(
                                                            rect, rect_id, parent_rect, x, y, rect.width, rect.height, direction)
                elif direction_count == 4: # move out
                    x += delta_x
                    y += delta_y

                    if self.testing:
                        print(f'move_pixels_relative: before clipping - new_x={x}, new_y={y}')

                    new_x, new_y, horizontal_limit_reached, vertical_limit_reached = self._clip_to_fit(
                                                            rect, rect_id, parent_rect, x, y, rect.width, rect.height, direction)

                    if self.testing:
                        print(f'move_pixels_relative: after clipping - {new_x=}, {new_y=}, {horizontal_limit_reached=}, {vertical_limit_reached=}')
                else:    # move in
                    new_x = x + delta_x
                    new_y = y + delta_y

                    # this branch is more complex because we need to check whether we've reached the center

                    target_x = round(parent_rect.center.x - rect.width / 2)
                    target_y = round(parent_rect.center.y - rect.height / 2)

                    # calculate distance between rectangle center and parent center
                    distance_x = round(parent_rect.center.x - rect.center.x)
                    distance_y = round(parent_rect.center.y - rect.center.y)

                    if self.testing:
                        print(f'move_pixels_relative: {new_x=}, {new_y=}, {parent_rect.center.x=}, {parent_rect.center.y=}')
                        print(f'move_pixels_relative: target point - {target_x=}, {target_y=}')

                    if (delta_x != 0):
                        if self.testing:
                            print(f'move_pixels_relative: {distance_x=}, {delta_x=}')

                        if (delta_x < 0 and (distance_x >= delta_x)) or (delta_x > 0 and (distance_x <= delta_x)):
                            # crossed target point, done moving horizontally
                            if self.testing:
                                print(f'move_pixels_relative: crossed horizontal target point')
                            new_x = target_x
                            horizontal_limit_reached = True

                    if delta_y != 0:
                        if self.testing:
                            print(f'move_pixels_relative: {distance_y=}, {delta_y=}')

                        if (delta_y < 0 and (distance_y >= delta_y)) or (delta_y > 0 and (distance_y <= delta_y)):
                            # crossed target point, done moving vertically
                            if self.testing:
                                print(f'move_pixels_relative: crossed vertical target point')
                            new_y = target_y
                            vertical_limit_reached = True

                return new_x, new_y, horizontal_limit_reached, vertical_limit_reached

            # move_pixels_relative

            start_time = time.time_ns()

            result = False

            # start with the current values
            x = rect.x
            y = rect.y

            if self.testing:
                print(f'move_pixels_relative: {delta_x=}, {delta_y=}, {x=}, {y=}')

            # apply changes as indicated
            new_x, new_y, horizontal_limit_reached, vertical_limit_reached = _get_new_coordinates(self, rect, rect_id, parent_rect,
                                                                                    x, y, delta_x, delta_y, direction)

            if (new_x, new_y) == (rect.x, rect.y):
                # nothing to change, this can happen via clipping...the delta values indicate a change,
                # but in the end the clipping prevents it from going ahead.
                result = True

                if self.testing:
                    print(f'move_pixels_relative: already there, nothing to do')
            else:
                try:
                    # make it so
                    new_rect = ui.Rect(new_x, new_y, rect.width, rect.height)
                    if self.testing:
                        print(f'move_pixels_relative: setting new rect: {rect} -> {new_rect}')

                    result, rect = self.compass_control.set_rect(rect, rect_id, new_rect)
                except CompassControl.RectUpdateError as e:
                    self.compass_control._handle_rect_update_error(e)

            elapsed_time_ms = (time.time_ns() - start_time) / 1e6
            if self.testing:
                print(f'move_pixels_relative: done {result=} ({elapsed_time_ms} ms)')

            return result, rect, horizontal_limit_reached, vertical_limit_reached

        def move_absolute(self, rect: ui.Rect, rect_id: int, x: float, y: float,
                                            region_in: Optional[Direction] = None) -> Tuple[bool, ui.Rect]:
            """Move rectangle in given direction to match the given values"""
            # find the point which we will move to the given coordinates, as indicated by the region.
            if region_in:
                x, y = self.translate_top_left_by_region(rect, rect_id, x, y, region_in)

                if self.testing:
                    print(f'move_absolute: translated top left position: {x,y}')

            result = False
            try:
                result, rect = self.compass_control.set_rect(rect, rect_id, ui.Rect(round(x), round(y),
                                                                        round(rect.width), round(rect.height)))
            except CompassControl.RectUpdateError as e:
                self.compass_control._handle_rect_update_error(e)

            if self.testing:
                print(f'move_absolute: {rect=}')
                # ctrl.mouse_move(x, y)

            return result, rect

        def resize_to_pointer(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, region: Direction) -> Tuple[bool, ui.Rect]:
            x, y = ctrl.mouse_pos()
            return self.move_absolute(rect, rect_id, x, y, region)

        def translate_top_left_by_region(self, rect: ui.Rect, rect_id: int,
                            target_x: float, target_y: float, region_in: Direction) -> Tuple[int, int]:
            """This code figures out what the top left coordinates should be for moving in the given direction"""

            width = rect.width
            height = rect.height

            if self.testing:
                print(f"_translate_top_left_by_region: initial rect: {rect}")
                print(f"_translate_top_left_by_region: move coordinates: {target_x=}, {target_y=}")

            top_left_x = target_x
            top_left_y = target_y

            direction_count = sum(region_in.values())
            if direction_count == 1:
                if region_in["left"]:
                    top_left_y = target_y - height / 2

                elif region_in["right"]:
                    top_left_x = target_x - width
                    top_left_y = target_y - height / 2

                elif region_in["up"]:
                    top_left_x = target_x - width / 2

                elif region_in["down"]:
                    top_left_x = target_x - width / 2
                    top_left_y = target_y - height

            elif direction_count == 2:
                if region_in["left"] and region_in["up"]:
                    # nothing to do here x and y are already set correctly for this case
                    pass

                elif region_in["right"] and region_in["up"]:
                    top_left_x = target_x - width

                elif region_in["right"] and region_in["down"]:
                    top_left_x = target_x - width
                    top_left_y = target_y - height

                elif region_in["left"] and region_in["down"]:
                    top_left_y = target_y - height

            elif direction_count == 0 or direction_count == 4:
                top_left_x = target_x - width / 2
                top_left_y = target_y - height / 2

            if self.testing:
                print(f"_translate_top_left_by_region: translated position: {top_left_x=}, {top_left_y=}")

            return round(top_left_x), round(top_left_y)

        def _clip_to_fit(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, x: float, y:
                            float, width: float, height: float, direction: Direction) -> Tuple[int, int, bool, bool]:
            """Adjust rectangle coordinates to keep it from overlapping the limits of the screen"""
            parent_x = parent_rect.x
            parent_y = parent_rect.y
            parent_width = parent_rect.width
            parent_height = parent_rect.height

            horizontal_limit_reached = vertical_limit_reached = False

            direction_count = sum(direction.values())

            new_x = x
            new_y = y
            if x <= parent_x and (direction_count == 0 or direction["left"]):
                new_x = parent_x
                horizontal_limit_reached = True
            elif x >= parent_x + parent_width - width and (direction_count == 0 or direction["right"]):
                new_x = parent_x + parent_width - width
                horizontal_limit_reached = True

            if y <= parent_y and (direction_count == 0 or direction["up"]):
                new_y = parent_y
                vertical_limit_reached = True
            elif y >= parent_y + parent_height - height and (direction_count == 0 or direction["down"]):
                new_y = parent_y + parent_height - height
                vertical_limit_reached = True

            return round(new_x), round(new_y), horizontal_limit_reached, vertical_limit_reached

        def test_bresenham(self):
            """Test code"""
            x0 = 0
            y0 = 0
            x1 = 100
            y1 = 4
            max_width = 4
            max_height = 4

            bres = self.bresenham(x0, y0, x1, y1)
            try:
                while True:
                    b0 = next(bres)
                    print(f'test_bresenham_1: bresenham: {b0}')
            except StopIteration:
                print(f'test_bresenham_1: bresenham done')

    class Sizer:
        def __init__(self, compass_control, settings_map: Dict, testing: bool):
            self.compass_control: CompassControl = compass_control

            # turn debug messages on and off
            self.testing: bool = testing

            # variables used during continuous move/resize operations
            self.continuous_width_increment: int = 0
            self.continuous_height_increment: int = 0
            self.continuous_job: Any = None
            self.continuous_alternation: str = None

            # keep rect history for use in detecting when the window stops shrinking during resize,
            # i.e. the minimum size has been reached and the resize operation should stop.
            self.continuous_resize_history: List = []

            # only one of these should be true at any time
            self.use_resize_history_for_shrink: bool = False
            self.use_change_check_for_shrink: bool = not self.use_resize_history_for_shrink

            # talon settings for managing continuous move/resize operations
            self._verbose_warnings: int = None
            self._continuous_resize_frequency_str: str = None
            self._continuous_resize_frequency: float = None
            self._continuous_resize_rate: float = None

            self.settings_map: Dict = settings_map
            self.refresh_map =  {
                talon_setting.path: local_name
                            for local_name, talon_setting in settings_map.items()
                                                                if hasattr(self, local_name) }

        @property
        def verbose_warnings(self):
            if self._verbose_warnings is None:
                self._verbose_warnings = self.settings_map['_verbose_warnings'].get()
            return self._verbose_warnings

        @property
        def continuous_resize_frequency_str(self):
            if self._continuous_resize_frequency_str is None:
                self._continuous_resize_frequency_str = self.settings_map['_continuous_resize_frequency_str'].get()
            return self._continuous_resize_frequency_str

        @property
        def continuous_resize_frequency(self):
            if self._continuous_resize_frequency is None:
                self._continuous_resize_frequency = float((self.continuous_resize_frequency_str)[:-2])
            return self._continuous_resize_frequency

        @property
        def continuous_resize_rate(self):
            if not self._continuous_resize_rate is None:
                self._continuous_resize_rate = self.settings_map['_continuous_resize_rate'].get()
            return self._continuous_resize_rate

        def refresh_settings(self, args):
            caller_id = 'CompassControl.Sizer'
            if args:
                self.compass_control._update_setting(self, caller_id, args)
            else:
                self.compass_control._update_all_settings(self, caller_id)

            # force a refresh for this value
            self._continuous_resize_frequency = None

        def continuous_init(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, multiplier: int,
                                        dpi_x: float, dpi_y: float, direction: Optional[Direction] = None) -> None:
            """Initialize continuous operation"""
            with self.compass_control.continuous_mutex:
                if self.continuous_job:
                    logging.warning('cannot start a resize job when one is already running')
                    return

                self.compass_control._continuous_reset()

                # get vertical and horizontal step sizes, to match the rate and frequency settings
                self.continuous_width_increment, self.continuous_height_increment = self.compass_control._get_continuous_parameters(
                                    rect, rect_id, parent_rect, self.continuous_resize_rate, self.continuous_resize_frequency,
                                        dpi_x, dpi_y, direction, '_resize')

                # apply multiplier to control whether we're stretching or shrinking
                self.continuous_width_increment *= multiplier
                self.continuous_height_increment *= multiplier

                # initialize
                self.compass_control.continuous_old_rect = rect.copy()
                self.compass_control.continuous_rect = rect
                self.compass_control.continuous_rect_id = rect_id
                self.compass_control.continuous_parent_rect = parent_rect
                self.compass_control.continuous_direction = direction

                if self.testing:
                    print(f'init_continuous: starting resize - {self.continuous_width_increment=}, {self.continuous_height_increment=}, {self.compass_control.continuous_direction=}, {multiplier=}')

                # let it roll
                self._continuous_start()

        def _continuous_start(self) -> None:
            """Commence continuous operation"""
            with self.compass_control.continuous_mutex:
                # enable tag to enable the 'stop' command
                ctx.tags = [self.compass_control.continuous_tag_name_qualified]

                # start the job
                self.continuous_job = cron.interval(self.continuous_resize_frequency_str, self._continuous_helper)

                if self.testing:
                    print(f'_start_continuous: {self.continuous_job=}')

        def _continuous_helper(self) -> None:
            """This is the engine that handles each continuous iteration"""

            def _check_history_for_max_shrinkage(self, rect: ui.Rect):
                # shrink is a special case, need to detect when the rectangle has shrunk to a minimum by
                # watching expected values to see when they stop changing as requested.
                if self.continuous_width_increment < 0 or self.continuous_height_increment < 0:
                    # check resize history
                    value = (rect.width, rect.height)
                    if len(self.continuous_resize_history) == 2:
                        if value == self.continuous_resize_history[0] == self.continuous_resize_history[1]:
                            # window size has stopped changing...so quit trying
                            if self.testing:
                                print('_win_resize_continuous_helper: window size has stopped changing, quitting...')
                            self.compass_control.continuous_stop()
                        else:
                            # chuck old data to make room for new data
                            self.continuous_resize_history.pop(0)
                    #
                    # update history
                    self.continuous_resize_history.append(value)

            def _check_resize_limits(self, resize_left_limit_reached: bool, resize_up_limit_reached: bool, resize_right_limit_reached: bool, resize_down_limit_reached: bool) -> None:
                direction = self.compass_control.continuous_direction
                direction_count = sum(direction.values())
                if direction_count == 1:    # horizontal or vertical
                    if (
                        (resize_left_limit_reached and direction['left']) or
                        (resize_up_limit_reached and direction['up']) or
                        (resize_right_limit_reached and direction['right']) or
                        (resize_down_limit_reached and direction['down'])
                    ):
                        if self.testing:
                            print(f'continuous_helper: single direction limit reached')
                        self.continuous_width_increment = 0
                        self.continuous_height_increment = 0
                elif direction_count == 2:    # diagonal
                    if (
                        (resize_left_limit_reached and direction['left']) or
                        (resize_right_limit_reached and direction['right'])
                    ):
                        if self.testing:
                            print(f'continuous_helper: horizontal limit reached')
                        self.continuous_width_increment = 0
                    #
                    if (
                        (resize_up_limit_reached and direction['up']) or
                        (resize_down_limit_reached and direction['down'])
                    ):
                        if self.testing:
                            print(f'continuous_helper: vertical limit reached')
                        self.continuous_height_increment = 0
                elif direction_count == 0 or direction_count == 4:    # in/out
                    if all([resize_left_limit_reached, resize_right_limit_reached]):
                        if self.testing:
                            print(f'continuous_helper: horizontal limit reached')
                        self.continuous_width_increment = 0

                    if all([resize_up_limit_reached, resize_down_limit_reached]):
                        if self.testing:
                            print(f'continuous_helper: vertical limit reached')
                        self.continuous_height_increment = 0

            start_mutex_wait = time.time_ns()

            with self.compass_control.continuous_mutex:
                iteration = self.compass_control.continuous_iteration

                elapsed_time_ms = (time.time_ns() - start_mutex_wait) / 1e6
                if self.testing:
                    print(f'continuous_helper: mutex wait ({elapsed_time_ms} ms)')

                start_time = time.time_ns()

                if not self.continuous_job:
                    # seems sometimes this gets called while the job is being canceled, so just return in that case
                    return

                # retrieve rectangle from previous iteration
                rect = self.compass_control.continuous_rect
                rect_id = self.compass_control.continuous_rect_id
                parent_rect = self.compass_control.continuous_parent_rect

                if self.testing:
                    print(f'continuous_helper: starting iteration {iteration} - {rect=}')

                if not self.continuous_width_increment and not self.continuous_height_increment:
                    # if there's no work to do...
                    if self.testing:
                        print(f'continuous_helper: rectangle resize failed. {rect=}')
                    self.compass_control.continuous_stop()
                else:
                    # do the resize
                    many_values = self.resize_pixels_relative(
                                    rect, rect_id, parent_rect,
                                        self.continuous_width_increment, self.continuous_height_increment,
                                            self.compass_control.continuous_direction
                                )
                    result, rect, resize_left_limit_reached, resize_up_limit_reached, \
                                                resize_right_limit_reached, resize_down_limit_reached = many_values

                    if self.testing:
                        print(f'continuous_helper: resize returned - {result=}, {rect=}, {resize_left_limit_reached=}, {resize_up_limit_reached=}, {resize_right_limit_reached=}, {resize_down_limit_reached=}')

                    # save updated rectangle for next iteration
                    self.compass_control.continuous_rect = rect

                    if result:
                        # the update succeeded, now need to check limits
                        _check_resize_limits(self, resize_left_limit_reached, resize_up_limit_reached, resize_right_limit_reached, resize_down_limit_reached)
                    else: # resize was not completely successful
                        if self.testing:
                            print(f'continuous_helper: resize failed')
                        if rect and self.use_resize_history_for_shrink:
                            if self.testing:
                                print(f'continuous_helper: checking for max shrinkage...5')
                            self._check_history_for_max_shrinkage(rect)
                        else:
                            if self.testing:
                                print(f'continuous_helper: rectangle resize failed. {rect=}')
                            self.compass_control.continuous_stop()

            elapsed_time_ms = (time.time_ns() - start_time) / 1e6
            if self.testing:
                print(f'continuous_helper: iteration {iteration} done ({elapsed_time_ms} ms)')
            if elapsed_time_ms > self.continuous_resize_frequency:
                if self.compass_control.verbose_warnings != 0:
                    logging.warning(f'continuous_helper: resize iteration {iteration} took {elapsed_time_ms}ms, longer than the current resize_frequency setting. actual rate may not match the current rate setting.')

            # for testing
            one_loop_only = False
            if one_loop_only:
                self.compass_control.continuous_stop()
                return

            self.compass_control.continuous_iteration += 1

        def _continuous_reset(self) -> None:
            """Reset variables used during continuous operations"""
            with self.compass_control.continuous_mutex:
                self.continuous_width_increment = 0
                self.continuous_height_increment = 0
                self.continuous_job = None
                self.continuous_alternation: str = None
                self.continuous_resize_history = []

        def resize_pixels_relative(self,
                    rect: ui.Rect, rect_id: int, parent_rect: ui.Rect,
                        delta_width: float, delta_height: float, direction_in: Direction
                            ) -> Tuple[bool, ui.Rect, bool, bool, bool, bool]:
            """Change size in given direction as indicated by the given delta values"""

            def _get_new_values(self,
                    rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, delta_width: float, delta_height: float,
                                        direction_in: Direction) -> Tuple[float, float, float, float, bool, bool, bool, bool]:

                result = resize_left_limit_reached = resize_up_limit_reached = resize_right_limit_reached = resize_down_limit_reached = False

                # start with the current values
                new_x = rect.x
                new_y = rect.y
                width = rect.width
                height = rect.height
                new_width = width + delta_width
                new_height = height + delta_height

                if self.testing:
                    print(f'resize_pixels_relative: starting {rect=}, {delta_width=}, {delta_height=}, {new_width=}, {new_height=}')

                # invert directions when shrinking non-uniformly. that is, we are shrinking *toward* the given
                # direction rather than shrinking away from that direction. note that we continue to use direction_in
                # for calls to the clipping methods, this is intentional and correct.
                direction = direction_in.copy()
                if not all(direction.values()): # => no direction values are set
                    if delta_width < 0:
                        temp = direction["right"]
                        direction["right"] = direction["left"]
                        direction["left"] = temp
                        # print(f'resize_pixels_relative: swapped left and right')
                    #
                    if delta_height < 0:
                        temp = direction["up"]
                        direction["up"] = direction["down"]
                        direction["down"] = temp
                        # print(f'resize_pixels_relative: swapped up and down')

                # are we moving diagonally?
                direction_count = sum(direction.values())

                if direction_count == 1:    # horizontal or vertical
                    # print(f'resize_pixels_relative: single direction (horizontal or vertical)')
                    # apply changes as indicated
                    if direction["left"]:
                        new_x = new_x - delta_width
                        new_x, new_width, resize_left_limit_reached = self._clip_left(rect, rect_id, parent_rect, new_x, new_width, direction_in)
                    #
                    if direction["up"]:
                        new_y = new_y - delta_height
                        new_y, new_height, resize_up_limit_reached = self._clip_up(rect, rect_id, parent_rect, new_y, new_height, direction_in)
                    #
                    if direction["right"]:
                        new_x, new_width, resize_right_limit_reached = self._clip_right(rect, rect_id, parent_rect, new_x, new_width, direction_in)
                    #
                    if direction["down"]:
                        new_y, new_height, resize_down_limit_reached = self._clip_down(rect, rect_id, parent_rect, new_y, new_height, direction_in)

                elif direction_count == 2:    # stretch diagonally
                    if direction["left"] and direction["up"]:
                        # we are stretching northwest so the coordinates must not change for the southeastern corner
                        new_x = new_x - delta_width
                        new_y = new_y - delta_height

                        new_x, new_width, resize_left_limit_reached = self._clip_left(rect, rect_id, parent_rect, new_x, new_width, direction_in)
                        new_y, new_height, resize_up_limit_reached = self._clip_up(rect, rect_id, parent_rect, new_y, new_height, direction_in)

                        #print(f'resize_pixels_relative: left and up')

                    elif direction["right"] and direction["up"]:
                        # we are stretching northeast so the coordinates must not change for the southwestern corner
                        # adjust y to account for the entire change in height
                        new_y = new_y - delta_height

                        new_x, new_width, resize_right_limit_reached = self._clip_right(rect, rect_id, parent_rect, new_x, new_width, direction_in)
                        new_y, new_height, resize_up_limit_reached = self._clip_up(rect, rect_id, parent_rect, new_y, new_height, direction_in)

                        #print(f'resize_pixels_relative: right and up')

                    elif direction["right"] and direction["down"]:
                        # we are stretching southeast so the coordinates must not change for the northwestern corner,
                        # nothing to do here x and y are already set correctly for this case
                        new_x, new_width, resize_right_limit_reached = self._clip_right(rect, rect_id, parent_rect, new_x, new_width, direction_in)
                        new_y, new_height, resize_down_limit_reached = self._clip_down(rect, rect_id, parent_rect, new_y, new_height, direction_in)

                        #print(f'resize_pixels_relative: right and down')

                    elif direction["left"] and direction["down"]:
                        # we are stretching southwest so the coordinates must not change for the northeastern corner,
                        # adjust x to account for the entire change in width
                        new_x = new_x - delta_width

                        new_x, new_width, resize_left_limit_reached = self._clip_left(rect, rect_id, parent_rect, new_x, new_width, direction_in)
                        new_y, new_height, resize_down_limit_reached = self._clip_down(rect, rect_id, parent_rect, new_y, new_height, direction_in)

                        #print(f'resize_pixels_relative: left and down')

                elif direction_count == 0 or direction_count == 4:    # stretch to/from center
                    # are delta values are divisible by two?
                    if (delta_width == 0 or abs(delta_width) >= 2) and (delta_height == 0 or abs(delta_height) >= 2):
                        # normal case, delta values are divisible by two
                        new_x = new_x - delta_width / 2
                        new_y = new_y - delta_height / 2
                    else:
                        if self.testing:
                            print(f'resize_pixels_relative: delta width and/or height are too small (<2), alternating size and position changes')

                        # alternate changing size and position, since we can only do one or the other when the delta is less than 2
                        if self.continuous_alternation == 'size':
                            # change position this time
                            new_x = new_x - delta_width
                            new_y = new_y - delta_height

                            # remove delta from the size values
                            new_width = width
                            new_height = height

                            self.continuous_alternation = 'position'
                        else:
                            # change size this time...nothing to actually do other than flip the toggle
                            self.continuous_alternation = 'size'

                    new_x, new_width, resize_left_limit_reached = self._clip_left(rect, rect_id, parent_rect, new_x, new_width, direction_in)

                    new_y, new_height, resize_up_limit_reached = self._clip_up(rect, rect_id, parent_rect, new_y, new_height, direction_in)

                    new_x, new_width, resize_right_limit_reached = self._clip_right(rect, rect_id, parent_rect, new_x, new_width, direction_in)

                    new_y, new_height, resize_down_limit_reached = self._clip_down(rect, rect_id, parent_rect, new_y, new_height, direction_in)

                if self.testing:
                    #     print(f'move_pixels_relative: {delta_x=}, {delta_y=}, {delta_width=}, {delta_height=}')
                    print(f'resize_pixels_relative: {width=}, {new_width=}, {height=}, {new_height=}')
                    #
                return new_x, new_y, new_width, new_height, resize_left_limit_reached, resize_up_limit_reached, resize_right_limit_reached, resize_down_limit_reached

            start_time = time.time_ns()

            width = rect.width
            height = rect.height

            new_x, new_y, new_width, new_height, \
                resize_left_limit_reached, resize_up_limit_reached, \
                    resize_right_limit_reached, resize_down_limit_reached \
                        = _get_new_values(self, rect, rect_id, parent_rect, delta_width, delta_height, direction_in)

            new_values = (new_x, new_y, new_width, new_height)

            if self.testing:
                print(f'resize_pixels_relative: setting rect {new_values=}')

            result = False
            old_rect = rect
            if (new_width, new_height) == (rect.width, rect.height):
                # nothing to change, this can happen via clipping...the delta values indicate a change,
                # but in the end the clipping prevents it from going ahead.
                result = True

                if self.testing:
                    print(f'resize_pixels_relative: already there, nothing to do')
            else:
                try:
                    # make it so
                    result, rect = self.compass_control.set_rect(rect, rect_id, ui.Rect(*new_values))
                except CompassControl.RectUpdateError as e:
                    self.compass_control._handle_rect_update_error(e)

                if not result and self.use_change_check_for_shrink:
                    resize_left_limit_reached, resize_up_limit_reached, resize_right_limit_reached, resize_down_limit_reached = \
                                                self._check_change_for_max_shrinkage(rect, new_x, new_y, new_width, new_height, old_rect)

            elapsed_time_ms = (time.time_ns() - start_time) / 1e6
            if self.testing:
                print(f'resize_pixels_relative: done ({elapsed_time_ms} ms)')

            return result, rect, resize_left_limit_reached, resize_up_limit_reached, resize_right_limit_reached, resize_down_limit_reached

        def resize_to_pointer(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, nd_direction: non_dual_direction) -> Tuple[bool, ui.Rect, bool, bool, bool, bool]:
            if self.testing:
                print(f'resize_to_pointer: starting - {rect=}, {nd_direction=}')

            mouse_x, mouse_y = ctrl.mouse_pos()
            if self.testing:
                print(f'resize_to_pointer: mouse position - {mouse_x, mouse_y}')

            direction = compass_direction([])
            delta_width = 0
            if nd_direction['horizontal'] or nd_direction['diagonal']:
                if mouse_x >= rect.x and mouse_x <= rect.x + rect.width:
                    # we are shrinking
                    if mouse_x < rect.center.x:
                        delta_width = rect.x - mouse_x
                        direction['right'] = True
                    elif mouse_x > rect.center.x:
                        # WIP - why are the parentheses required below?
                        delta_width = mouse_x - (rect.x + rect.width)
                        direction['left'] = True
                else:
                    # we are stretching
                    if mouse_x < rect.x:
                        delta_width = rect.x - mouse_x
                        direction['left'] = True
                    else:
                        # WIP - why are the parentheses required below?
                        delta_width = mouse_x - (rect.x + rect.width)
                        direction['right'] = True

            delta_height = 0
            if nd_direction['vertical'] or nd_direction['diagonal']:
                if mouse_y >= rect.y and mouse_y <= rect.y + rect.height:
                    # we are shrinking
                    if mouse_y < rect.center.y:
                        delta_height = rect.y - mouse_y
                        direction['down'] = True
                    elif mouse_y > rect.center.y:
                        # WIP - why are the parentheses required below?
                        delta_height = mouse_y - (rect.y + rect.height)
                        direction['up'] = True
                else:
                    # we are stretching
                    if mouse_y < rect.y:
                        delta_height = rect.y - mouse_y
                        direction['up'] = True
                    else:
                        # WIP - why are the parentheses required below?
                        delta_height = mouse_y - (rect.y + rect.height)
                        direction['down'] = True

            if self.testing:
                print(f'resize_to_pointer: {delta_width=}, {delta_height=}, {direction=}')

            return self.resize_pixels_relative(rect, rect_id, parent_rect, delta_width, delta_height, direction)

        def _check_change_for_max_shrinkage(self, rect: ui.Rect, new_x: float, new_y: float, new_width: float, new_height: float, old_rect: ui.Rect):
            # shrink is a special case, need to detect when the rectangle has shrunk to a minimum by
            # watching expected values to see when they stop changing as requested.

            resize_left_limit_reached = resize_up_limit_reached = resize_right_limit_reached = resize_down_limit_reached = False

            if self.continuous_width_increment < 0:
                # if a change was requested and not delivered, i.e. if the requested value is not the same as the old one AND
                # the requested value is not the same as the new value.
                if (new_x != old_rect.x and rect.x == old_rect.x) and (new_width != old_rect.width and rect.width == old_rect.width):
                    resize_left_limit_reached = True
                    resize_right_limit_reached = True
                    if self.testing:
                        # print(f'resize_pixels_relative: horizontal shrink limit reached')
                        print(f'resize_pixels_relative: horizontal shrink limit reached - {rect.x=}, {new_x=}, {rect.width=}, {new_width=}')

            if self.continuous_height_increment < 0:
                # if a change was requested and not delivered, i.e. if the requested value is not the same as the old one AND
                # the requested value is not the same as the new value.
                if (new_y != old_rect.y and rect.y == old_rect.y) and (new_height != old_rect.height and rect.height == old_rect.height):
                    resize_up_limit_reached = True
                    resize_down_limit_reached = True
                    if self.testing:
                        print(f'resize_pixels_relative: vertical shrink limit reached')

            return resize_left_limit_reached,resize_up_limit_reached,resize_right_limit_reached,resize_down_limit_reached

        def resize_absolute(self, rect: ui.Rect, rect_id: int, target_width: float,
                                        target_height: float, region_in: Optional[Direction] = None) -> Tuple[bool, ui.Rect]:
            """Change size in given direction to match the given values"""
            x = rect.x
            y = rect.y

            delta_width = target_width - rect.width
            delta_height = target_height - rect.height

            region = None
            if region_in:
                # find the point which we will move to the given coordinates, as indicated by the given region.

                region = region_in.copy()
                # invert directions when shrinking. that is, we are shrinking *toward* the
                #  given direction rather than shrinking away from that direction.
                if delta_width < 0:
                    region["left"] = region_in["right"]
                    region["right"] = region_in["left"]
                #
                if delta_height < 0:
                    region["up"] = region_in["down"]
                    region["down"] = region_in["up"]

                x, y = self.translate_top_left_by_region(rect, rect_id, target_width, target_height, region)

                if self.testing:
                    print(f'resize_absolute: translated top left position: {x,y}')

            result = False
            try:
                result, rect = self.compass_control.set_rect(rect, rect_id, ui.Rect(round(x), round(y), round(target_width), round(target_height)))
            except CompassControl.RectUpdateError as e:
                self.compass_control._handle_rect_update_error(e)

            if self.testing:
                print(f'resize_absolute: {rect=}')
                # ctrl.mouse_move(rect.x, rect.y)

            return result, rect

        def translate_top_left_by_region(self, rect: ui.Rect, rect_id: int,
                        target_width: float, target_height: float, direction: Direction) -> Tuple[int, int]:
            """This code figures out what the top left coordinates should be for resizing in the given direction"""

            x = rect.x
            y = rect.y

            delta_width = target_width - rect.width
            delta_height = target_height - rect.height

            if self.compass_control.verbose_warnings != 0:
                if abs(delta_width) < 2:
                    logging.warning(f'_translate_top_left_by_region: width change is less than 2, which is too small for normal resize calculations, ymmv: {delta_width=}')
                if abs(delta_height) < 2:
                    logging.warning(f'_translate_top_left_by_region: height change is less than 2, which is too small for normal resize calculations, ymmv: {delta_height=}')

            if self.testing:
                print(f"_translate_top_left_by_region: initial rect: {rect}")
                print(f"_translate_top_left_by_region: resize coordinates: {target_width=}, {target_height=}")

            direction_count = sum(direction.values())
            if direction_count == 1:
                if direction["left"]:
                    # stretching west, x coordinate must not change for the eastern corners, so push top left to the west
                    x = x - delta_width

                    # adjust y to account for half the change in height
                    y = y - delta_height / 2

                elif direction["up"]:
                    # stretching north, y coordinate must not change for the southern corners,
                    # adjust x to account for half the change in width
                    x = x - delta_width / 2

                    # adjust y to account for the entire change in height
                    y = y - delta_height

                elif direction["right"]:
                    # we are stretching east, so the x coordinate must not change for the western corners, i.e. top left

                    # adjust y to account for half the change in height
                    y = y - delta_height / 2

                elif direction["down"]:
                    # stretching south, y coordinate must not change for the northern corners, i.e. top left

                    # adjust x to account for half the change in width
                    x = x - delta_width / 2

            elif direction_count == 2:
                if direction["left"] and direction["up"]:
                    # we are stretching northwest so the coordinates must not change for the southeastern corner
                    x = x - delta_width
                    y = y - delta_height

                elif direction["right"] and direction["up"]:
                    # we are stretching northeast so the coordinates must not change for the southwestern corner,
                    # adjust y to account for the entire change in height
                    y = y - delta_height

                elif direction["right"] and direction["down"]:
                    # we are stretching southeast so the coordinates must not change for the northwestern corner,
                    # nothing to do here x and y are already set correctly for this case
                    pass

                elif direction["left"] and direction["down"]:
                    # we are stretching southwest so the coordinates must not change for the northeastern corner,
                    # adjust x to account for the entire change in width
                    x = x - delta_width

            elif direction_count == 0 or direction_count == 4:
                # resize in all directions
                x = x - delta_width / 2
                y = y - delta_height / 2

            if self.testing:
                print(f"_translate_top_left_by_region: translated position: {x=}, {y=}, {target_width=}, {target_height=}")

            return round(x), round(y)

        def _clip_left(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, x: float, width: float, direction: Direction) -> Tuple[int, int, bool]:
            """Adjust rectangle coordinates to keep it from overlapping the left limit of the screen"""

            if self.testing:
                print(f'_clip_left: before clip: {x=}, {width=}')

            resize_left_limit_reached = False

            direction_count = sum(direction.values())

            # clip to parent rectangle
            if x < parent_rect.x and (direction_count == 0 or direction['left']):

                # update width before updating new_x
                width = width - (parent_rect.x - x)
                x = parent_rect.x

                resize_left_limit_reached = True

                if self.testing:
                    print(f'_clip_left: {resize_left_limit_reached=}')

            if self.testing:
                print(f'_clip_left: after clip: {x=}, {width=}')

            return round(x), round(width), resize_left_limit_reached

        def _clip_up(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, y: float,
                                    height: float, direction: Direction) -> Tuple[int, int, bool]:
            """Adjust rectangle coordinates to keep it from overlapping the upper limit of the screen"""

            if self.testing:
                print(f'_clip_up: before clip: {y=}, {height=}')

            resize_up_limit_reached = False

            direction_count = sum(direction.values())

            # clip to parent rectangle
            if y < parent_rect.y and (direction_count == 0 or direction['up']):

                # update height before updating y
                height = height - (parent_rect.y - y)
                y = parent_rect.y

                resize_up_limit_reached = True

                if self.testing:
                    print(f'_clip_up: {resize_up_limit_reached=}')

            if self.testing:
                print(f'_clip_up: after clip: {y=}, {height=}')

            return round(y), round(height), resize_up_limit_reached

        def _clip_right(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, x: float,
                                    width: float, direction: Direction) -> Tuple[int, int, bool]:
            """Adjust rectangle coordinates to keep it from overlapping the right limit of the screen"""

            if self.testing:
                print(f'_clip_right: before clip: {x=}, {width=}')

            resize_right_limit_reached = False

            direction_count = sum(direction.values())

            if x + width > parent_rect.x + parent_rect.width and (direction_count == 0 or direction['right']):
                # print(f'_clip_right: right clipping')

                width = parent_rect.x + parent_rect.width - rect.x

                resize_right_limit_reached = True

                if self.testing:
                    print(f'_clip_right: {resize_right_limit_reached=}')

            if self.testing:
                print(f'_clip_right: after clip: {x=}, {width=}')

            return round(x), round(width), resize_right_limit_reached

        def _clip_down(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, y: float,
                                    height: float, direction: Direction) -> Tuple[int, int, bool]:
            """Adjust rectangle coordinates to keep it from overlapping the lower limit of the screen"""

            if self.testing:
                print(f'_clip_down: before clip: {y=}, {height=}')

            resize_down_limit_reached = False

            direction_count = sum(direction.values())

            if y + height > parent_rect.y + parent_rect.height and (direction_count == 0 or direction['down']):
                height = parent_rect.y + parent_rect.height - rect.y

                resize_down_limit_reached = True

                if self.testing:
                    print(f'_clip_down: {resize_down_limit_reached=}')

            if self.testing:
                print(f'_clip_down: after clip: {y=}, {height=}')

            return round(y), round(height), resize_down_limit_reached


    # CompassControl methods

    def _get_continuous_parameters(
                self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, rate_cps: float, frequency: float,
                    dpi_x: float, dpi_y: float, direction: Direction, operation: str
        ) -> Tuple[int, int]:
            """Return horizontal and vertical increments to advance at each continuous iteration in order to match the given frequency, density and rate values"""
            if self.testing:
                print(f'get_continuous_parameters: {rate_cps=}')

            # convert rate from centimeters to inches, to match dpi units
            rate_ips = rate_cps / 2.54

            # calculate dots per millisecond
            dpms_x = (rate_ips * dpi_x) / 1000
            dpms_y = (rate_ips * dpi_y) / 1000

            if self.testing:
                print(f'get_continuous_parameters: {dpms_x=}, {dpms_y=}')

            width_increment = height_increment = 0

            direction_count = sum(direction.values())
            if direction_count == 1:
                # single direction
                if direction["left"] or direction["right"]:
                    width_increment = dpms_x * frequency
                elif direction["up"] or direction["down"]:
                    height_increment = dpms_y * frequency
            else:    # diagonal
                width_increment = dpms_x * frequency
                height_increment = dpms_y * frequency

                if direction_count == 0 and operation == 'move':    # move in (toward the center)
                    if self.testing:
                        print(f"get_continuous_parameters: 'move in' special case")

                    # special case, return signed values
                    if rect.center.x > parent_rect.center.x:
                        width_increment *= -1
                    #
                    if rect.center.y > parent_rect.center.y:
                        height_increment *= -1
                elif direction_count == 4 and operation == 'move':    # move out (away from center)
                    if self.testing:
                        print(f"get_continuous_parameters: 'move out' special case")

                    # special case, return signed values
                    if rect.center.x < parent_rect.center.x:
                        width_increment *= -1
                    #
                    if rect.center.y < parent_rect.center.y:
                        height_increment *= -1

            if self.testing:
                print(f"get_continuous_parameters: returning {width_increment=}, {height_increment=}")

            return round(width_increment), round(height_increment)

    def continuous_stop(self) -> None:
            """Stop the current continuous move/resize operation"""
            with self.continuous_mutex:
                if not self.mover.continuous_job and not self.sizer.continuous_job:
                    if self.testing:
                        print('continuous_stop: no jobs to stop (may have stopped automatically via clipping logic)')
                    return

                if self.testing:
                    print(f'continuous_stop: current thread = {threading.get_native_id()}')

                if self.mover.continuous_job:
                    cron.cancel(self.mover.continuous_job)

                if self.sizer.continuous_job:
                    cron.cancel(self.sizer.continuous_job)

                # disable 'stop' command
                ctx.tags = []

                if self.continuous_old_rect:
                    # remember starting rectangle
                    if self.testing:
                        print(f'continuous_stop: {self.continuous_old_rect=}')

                    self._save_last_rect()

                self._continuous_reset()

                # finally, invoke caller's stop method
                stop_method = self.continuous_stop_method
                stop_method()

    def _continuous_reset(self) -> None:
        """Reset variables used during continuous operations"""
        with self.continuous_mutex:
            self.mover._continuous_reset()
            self.sizer._continuous_reset()

            self.continuous_direction = None
            self.continuous_old_rect = None
            self.continuous_iteration = 0
            self.continuous_rect = None
            self.continuous_rect_id = None
            self.continuous_parent_rect = None

    def set_rect(self, old_rect: ui.Rect, rect_id: int, rect_in: ui.Rect) -> Tuple[bool, ui.Rect]:
            """Invoke the given set method with updated rectangle values, so if old rectangle values for revert"""

            # invoke caller's set method
            set_method = self.set_method
            result = set_method(old_rect, rect_id, rect_in)

            # remember old rectangle, for 'revert'
            self._save_last_rect(rect_id, old_rect)

            return result

    def _save_last_rect(self, rect_id=None, rect=None):
        """After a change, save state of the original rectangle so it can be restored later"""
        # if self.testing:
        #     print(f'save_last_rect: {self}, {self.continuous_rect_id=}, {self.continuous_old_rect=}')

        if not rect_id:
            rect_id=self.continuous_rect_id
        if not rect:
            rect=self.continuous_old_rect

        self.last_rect = {
            'id': rect_id,
            'rect': rect
        }

    def revert(self, rect: ui.Rect, rect_id: int) -> Tuple[bool, ui.Rect]:
        """Restore state of rectangle from before the last change"""
        result, rect = False, rect
        if self.last_rect and self.last_rect['id'] == rect_id:
            if self.testing:
                print(f'revert: reverting size and/or position for {self.last_rect}')

            result = False
            try:
                result, rect = self.set_rect(rect, rect_id, self.last_rect['rect'])
            except CompassControl.RectUpdateError as e:
                self._handle_rect_update_error(e)

        return result, rect

    def snap(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, percent: int, direction: Direction) -> None:
        """Move rectangle to center and size it according to the given direction and screen size percentage"""
        target_width = (parent_rect.width * (percent/100))
        target_height = (parent_rect.height * (percent/100))

        old_rect = rect.copy()
        if self.testing:
            print(f'snap: starting - {old_rect=}')

        if (rect.x, rect.y) != (parent_rect.center.x, parent_rect.center.y):
            # move rectangle center to parent rectangle center
            result, rect = self.mover.move_absolute(rect, rect_id, parent_rect.center.x, parent_rect.center.y, direction)
            if not result:
                if self.testing:
                    print(f'snap: move to center failed, {rect=}')

        if self.testing:
            print(f'snap: after move - {old_rect=}')

        if (rect.width, rect.height) != (parent_rect.width, parent_rect.height):
            # set rectangle size
            result, rect = self.sizer.resize_absolute(rect, rect_id, target_width, target_height, direction)
            if not result:
                if self.testing:
                    print(f'snap: resize failed, {rect=}')

        if self.testing:
            print(f'snap: after resize - {old_rect=}')

        # remember old rectangle, for 'revert'
        self._save_last_rect(rect_id, old_rect)

    def get_center_to_center_rect(self, rect: ui.Rect, rect_id: int, other_rect: ui.Rect) -> Tuple[ui.Rect, bool, bool]:
        """Return rectangle whose diagonal is the line connecting the centers of the two given rectangles"""
        width = rect.width
        height = rect.y

        rect_center = rect.center

        other_center = other_rect.center

        width = abs(rect_center.x - other_center.x)
        horizontal_multiplier = 1 if rect_center.x <= other_center.x else -1

        height = abs(rect_center.y - other_center.y)
        vertical_multiplier = 1 if rect_center.y <= other_center.y else -1

        center_to_center_rect = ui.Rect(round(other_center.x), round(rect_center.y), round(width), round(height))
        # print(f'_get_center_to_center_rect: returning {center_to_center_rect=}, {horizontal_multiplier=}, {vertical_multiplier=}')

        return center_to_center_rect, horizontal_multiplier, vertical_multiplier

    def get_center_to_intercept_rect(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect) -> Tuple[ui.Rect, bool, bool]:
        """Return rectangle with corners at the center of the parent rectangle and at the center-to-center intercept point"""
        width = rect.width
        height = rect.y

        rect_center = rect.center

        intercept_x, intercept_y = self.get_center_to_center_intercept(rect, parent_rect)

        width = abs(rect_center.x - intercept_x)
        horizontal_multiplier = 1 if rect_center.x <= intercept_x else -1

        height = abs(rect_center.y - intercept_y)
        vertical_multiplier = 1 if rect_center.y <= intercept_y else -1

        result_rect = ui.Rect(round(intercept_x), round(rect_center.y), round(width), round(height))
        if self.testing:
            print(f'get_center_to_intercept_rect: returning {result_rect=}, {horizontal_multiplier=}, {vertical_multiplier=}')

        return result_rect, horizontal_multiplier, vertical_multiplier

    def get_component_dimensions(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect,
                                    distance: float, direction: Direction, operation: str) -> Tuple[int, int]:
        """Return horizontal and vertical distances corresponding to the given distance along the diagonal of the given rectangle"""
        delta_width = delta_height = 0
        direction_count = sum(direction.values())
        if operation == 'move' and (direction_count == 0 or direction_count == 4):    # in/out
            # this is a special case - we return signed values for this case only

            if direction_count == 0:    # in
                rect, horizontal_multiplier, vertical_multiplier = self.get_center_to_center_rect(rect, rect_id, parent_rect)
            else: # direction_count == 4
                rect, horizontal_multiplier, vertical_multiplier = self.get_center_to_intercept_rect(rect, rect_id, parent_rect)

            diagonal_length = self.get_diagonal_length(rect)

            rect_center = rect.center

            parent_center = parent_rect.center

            # from https://math.stackexchange.com/questions/175896/finding-a-point-along-a-line-a-certain-distance-away-from-another-point
            ratio_of_differences = distance / diagonal_length
            new_x = (((1 - ratio_of_differences) * rect_center.x) + (ratio_of_differences * parent_center.x))
            new_y = (((1 - ratio_of_differences) * rect_center.y) + (ratio_of_differences * parent_center.y))

            if self.testing:
                print(f"get_component_dimensions: {diagonal_length=}, {new_x=}, {new_y=}")

            delta_width = abs(new_x - rect_center.x) * horizontal_multiplier
            delta_height = abs(new_y - rect_center.y) * vertical_multiplier

            if self.testing:
                x_steps = 0
                if delta_width != 0:
                    x_steps = rect.width/delta_width
                print(f"get_component_dimensions: x steps={x_steps}")

                y_steps = 0
                if delta_height != 0:
                    y_steps = rect.height/delta_height
                print(f"get_component_dimensions: y steps={y_steps}")
        else:
            if direction_count == 1:    # horizontal or vertical
                if direction["left"] or direction["right"]:
                    delta_width = distance
                elif direction["up"] or direction["down"]:
                    delta_height = distance
            else:  # diagonal
                diagonal_length = self.get_diagonal_length(rect)
                ratio = distance / diagonal_length
                delta_width = rect.width * ratio
                delta_height = rect.height * ratio

        if self.testing:
            print(f"get_component_dimensions: returning {delta_width}, {delta_height}")

        return round(delta_width), round(delta_height)

    def get_component_dimensions_by_percent(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect,
                                                percent: float, direction: Direction, operation: str) -> Tuple[int, int]:
        """Return horizontal and vertical distances corresponding to the given percentage of the diagonal of the given rectangle"""
        if self.testing:
            print(f'_get_component_dimensions_by_percent: {percent=}')

        direction_count = sum(direction.values())
        if operation == 'move':
            if direction_count == 0:    # in
                rect, *unused = self.get_center_to_center_rect(rect, rect_id, parent_rect)
            elif direction_count == 4:
                rect, *unused = self.get_center_to_intercept_rect(rect, rect_id, parent_rect)

        if direction_count  == 1:    # horizontal or vertical
            if direction["left"] or direction["right"]:
                distance = rect.width * (percent/100)
            elif direction["up"] or direction["down"]:
                distance =  rect.height * (percent/100)
        else:  # diagonal
            diagonal_length = self.get_diagonal_length(rect)
            distance = diagonal_length * (percent/100)

        return self.get_component_dimensions(rect, rect_id, parent_rect, distance, direction, operation)

    # Bresenham line code, from
    #       https://github.com/encukou/bresenham/blob/master/bresenham.py
    def bresenham(self, x0: int, y0: int, x1: int, y1: int) -> Tuple[int, int]:
        """Yield integer coordinates on the line from (x0, y0) to (x1, y1).

        Input coordinates should be integers.

        The result will contain both the start and the end point.
        """
        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0

        for x in range(dx + 1):
            yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy

    def get_edge_midpoint(self, rect: ui.Rect, direction: Direction) -> Tuple[float, float]:
        """Return midpoint of the rectangle edge indicated by the given direction"""

        x = y = None

        direction_count = sum(direction.values())
        if direction_count == 1:
            if direction['left']: # west
                x = rect.x
                y = (rect.y + rect.height) // 2
            elif direction['up']: # north
                x = (rect.x + rect.width) // 2
                y = rect.y
            elif direction['right']: # east
                x = rect.x + rect.width
                y = (rect.y + rect.height) // 2
            elif direction['down']: # south
                x = (rect.x + rect.width) // 2
                y = rect.y + rect.height

        return round(x), round(y)

    def get_corner(self, rect: ui.Rect, direction: Direction) -> Tuple[float, float]:
        """Return coordinates of the rectangle corner indicated by the given direction"""
        x = y = None

        direction_count = sum(direction.values())
        if direction_count == 2:
            if direction['left'] and direction['up']: # northwest
                x = rect.x
                y = rect.y
            elif direction['right'] and direction['up']: # northeast
                x = rect.x + rect.width
                y = rect.y
            elif direction['right'] and direction['down']: # southeast
                x = rect.x + rect.width
                y = rect.y + rect.height
            elif direction['left'] and direction['down']: # southwest
                x = rect.x
                y = rect.y + rect.height

        return round(x), round(y)

    def get_center(self, rect: ui.Rect) -> Tuple[float, float]:
        """Return coordinates of the rectangle center"""
        return round(rect.center.x), round(rect.center.y)

    # from https://stackoverflow.com/questions/9526726/find-the-cgpoint-on-a-uiview-rectangle-intersected-by-a-straight-line-at-a-given
    # return coordinates of the point at which the center-to-center line crosses the nearest parent edges
    def get_center_to_center_intercept(self, rect, parent_rect) -> Tuple[float, float]:

        # handle special case which would otherwise result in division by zero in subsequent code
        if parent_rect.center.x == rect.center.x:
            result_x = rect.center.x

            if rect.center.y > parent_rect.center.y:
                result_y = parent_rect.y + parent_rect.height
                print(f'get_center_to_center_intercept: below - {result_x=}, {result_y=}')
            else:
                result_y = parent_rect.y
                print(f'get_center_to_center_intercept: above - {result_x=}, {result_y=}')

            if self.testing:
                angle_between = math.radians(90)
                print(f'get_center_to_center_intercept: {angle_between=} ({math.degrees(angle_between)} degrees), {result_x=}, {result_y=}')

            return round(result_x), round(result_y)

        # get the angle between the center-to-center line and the horizontal
        #
        # a horizontal line has a slope of zero
        slope1 = 0
        #
        # get slope of the center-to-center line between the two rectangles
        slope2 = (rect.center.y - parent_rect.center.y) / (rect.center.x - parent_rect.center.x)

        # from https://math.stackexchange.com/questions/1269050/finding-the-angle-between-two-line-equations
        angle_between = math.atan(slope2)
        if rect.center.x < parent_rect.center.x:
            angle_between += math.radians(180)
        if angle_between < 0:
            angle_between += math.radians(360)

        tan_angle_between = math.tan(angle_between)

        radius_x = parent_rect.width / 2
        radius_y = parent_rect.height / 2

        # get y intersection with right edge
        relative_offset_y = radius_x * tan_angle_between

        # is y within the parent rect or outside?
        if abs(relative_offset_y) <= radius_y:
            # it's inside => the intercept is on the right edge or left edge

            if angle_between < (math.pi / 2) or angle_between > 3 * (math.pi / 2):
                # right edge
                relative_offset_x = radius_x
            else:
                # left edge
                relative_offset_x = -radius_x
                relative_offset_y = -relative_offset_y
        else:
            # it's outside - the intercept is on the top edge or bottom edge

            # get x instersection with bottom edge
            relative_offset_x = radius_y / tan_angle_between

            if angle_between < math.pi:
                # bottom edge
                relative_offset_y = radius_y
            else:
                # top edge
                relative_offset_x = -relative_offset_x
                relative_offset_y = -radius_y

        # apply the relative offset to the parent center to get the actual coordinates
        result_x = parent_rect.center.x + relative_offset_x
        result_y = parent_rect.center.y + relative_offset_y

        if self.testing:
            print(f'get_center_to_center_intercept: {angle_between=} ({math.degrees(angle_between)} degrees), {radius_x=}, {radius_y=}, {result_x=}, {result_y=}')

        return round(result_x), round(result_y)

    def get_target_point(self, rect: ui.Rect, rect_id: int, parent_rect: ui.Rect, direction: Direction) -> Tuple[int, int]:
        """Return the target point indicated by the given direction"""
        target_x = target_y = None

        direction_count = sum(direction.values())
        if direction_count == 0:    #  in/center
            # get top left coordinate when rectangle is at parent center
            target_x = round(parent_rect.center.x - (rect.width / 2))
            target_y = round(parent_rect.center.y - (rect.height / 2))
        elif direction_count == 1:    # horizontal or vertical
            target_x, target_y = self.get_edge_midpoint(parent_rect, direction)
        elif direction_count == 2:    # diagonal
            target_x, target_y = self.get_corner(parent_rect, direction)
        elif direction_count == 4:    # out
            center_intercept_x, center_intercept_y = self.get_center_to_center_intercept(rect, parent_rect)
            # translate center coordinates to top left
            target_x = round(center_intercept_x - (rect.width / 2))
            target_y = round(center_intercept_y - (rect.height / 2))

            if self.testing:
                print(f'get_target_point: center to center intercept - {center_intercept_x, center_intercept_y}')
                print(f'get_target_point: corresponding top left coordinates - {target_x, target_y}')

        return target_x, target_y

    def get_diagonal_length(self, rect: ui.Rect) -> float:
        """Get diagonal length of given rectangle"""
        return math.sqrt(((rect.width - rect.x) ** 2) + ((rect.height - rect.y) ** 2))

# # explicitly trigger re-import of dependent modules, since the talon reload mechanism won't do it
# DEPENDENTS = [ 'window_tweak.py' ]

# print(f'compass_control.py - triggering re-import of dependent modules: {DEPENDENTS}')

# import os
# from pathlib import Path

# curdir = os.path.dirname(__file__)
# for dependent in DEPENDENTS:
#     Path(os.path.join(curdir, dependent)).touch()
