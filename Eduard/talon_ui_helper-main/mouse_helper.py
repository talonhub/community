"""
Useful actions related to moving the mouse
"""

import os
import math
import subprocess
from typing import Union, Optional, List

from talon import actions, ui, clip, screen, Module
from talon.types import Rect as TalonRect
from talon.experimental import locate

from .blob_detector import calculate_blob_rects
from .marker_ui import MarkerUi


mod = Module()
setting_template_directory = mod.setting(
    "mouse_helper_template_directory",
    type=str,
    desc=(
        "The folder that templated images are saved to."
        " Defaults to image_templates in your user folder"
    ),
    default=None
)


def get_image_template_directory():
    """
    Gets the full path to the directory where template images are stored.
    """

    maybe_value = setting_template_directory.get()
    if maybe_value:
        return maybe_value
    else:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../image_templates"
        )


def find_active_window_rect() -> TalonRect:
    return ui.active_window().rect


def screencap_to_image(rect: TalonRect) -> 'talon.skia.image.Image':
    """
    Captures the given rectangle off the screen
    """

    return screen.capture(rect.x, rect.y, rect.width, rect.height, retina=False)


def calculate_relative(modifier: str, start: float, end: float) -> float:
    """
    Helper method for settings. Lets you specify numbers relative to a
    range. For example:

        calculate_relative("-10.0", 0, 100) == 90
        calculate_relative("10", 0, 100) == 10
        calculate_relative("-0", 0, 100) == 100

    Note that positions and offset are floats.
    """
    if modifier.startswith("-"):
        modifier_ = float(modifier[1:])
        rel_end = True
    elif modifier == ".":
        # In the middle
        return (end + start) // 2
    else:
        modifier_ = float(modifier)
        rel_end = False

    if rel_end:
        return end - modifier_
    else:
        return start + modifier_


saved_mouse_pos = None


@mod.action_class
class MouseActions:
    def mouse_helper_position_save():
        """
        Saves the mouse position to a global variable
        """

        global saved_mouse_pos

        saved_mouse_pos = (actions.mouse_x(), actions.mouse_y())

    def mouse_helper_position_restore():
        """
        Restores a saved mouse position
        """

        if saved_mouse_pos is None:
            return

        actions.mouse_move(
            saved_mouse_pos[0],
            saved_mouse_pos[1]
        )

    def mouse_helper_move_active_window_relative(xpos: str, ypos: str):
        """
        Positions the mouse relative to the active window
        """

        rect = find_active_window_rect()

        actions.mouse_move(
            calculate_relative(xpos, 0, rect.width) + rect.x,
            calculate_relative(ypos, 0, rect.height) + rect.y,
        )

    def mouse_helper_move_relative(xdelta: float, ydelta: float):
        """
        Moves the mouse relative to its current position
        """

        new_xpos = actions.mouse_x() + xdelta
        new_ypos = actions.mouse_y() + ydelta
        actions.mouse_move(new_xpos, new_ypos)

    def mouse_helper_calculate_relative_rect(relative_rect_offsets: str, region:str ="active_screen") -> TalonRect:
        """
        Calculates a talon rectangle relative to the entire screen based on the given region
        of interest and a set of offsets. Examples:

            "0 0 -0 -0", "active_screen": Would indicate the entire active screen.
            "10 20 30 40", "active_window": Would indicate the region between pixels (10, 20) and (30, 40)
              on the currently focussed window.
            "10 20 -30 40", "active_window": Would indicate the region between pixels (10, 20) and
              the pixel 30 units from the right hand side of the window and 40 units from the top.
        """

        if region == "active_screen":
            active_window = ui.active_window()
            if active_window.id == -1:
                base_rect = ui.main_screen().rect
            else:
                base_rect = active_window.screen.rect
        elif region == "active_window":
            base_rect = find_active_window_rect()
        else:
            assert "Unhandled region"

        mods = relative_rect_offsets.split(" ")
        _calc_pos = calculate_relative
        x = _calc_pos(mods[0], base_rect.x, base_rect.x + base_rect.width)
        y = _calc_pos(mods[1], base_rect.y, base_rect.y + base_rect.height)
        rect = TalonRect(
            x,
            y,
            _calc_pos(mods[2], 0, base_rect.width) - float(mods[0]),
            _calc_pos(mods[3], 0, base_rect.height) - float(mods[1]),
        )

        return rect

    def mouse_helper_find_template_relative(
        template_path: str,
        xoffset: float=0,
        yoffset: float=0,
        region: Optional[TalonRect]=None
    ) -> List[TalonRect]:
        """
        Finds all matches for the given image template within the given region.

        :param template_path: Filename of the image to find. Can be an absolute path or
            if no '/' or '\\' character is specified, it is relative to the image
            templates directory.
        :param xoffset: Amount to shift in the x direction relative to the
            center of the template.
        :param yoffset: Amount to shift in the y direction relative to the
            center of the template.
        :param region: The region to search for the template in. Either a screen relative
            TalonRect (see mouse_helper_calculate_relative_rect) or None to just use the
            active screen.
        """

        if region is None:
            rect = actions.user.mouse_helper_calculate_relative_rect(
                "0 0 -0 -0",
                "active_screen"
            )
        else:
            rect = region

        if os.pathsep in template_path:
            # Absolute path specified
            template_file = template_path
        else:
            # Filename in image templates directory specified
            template_file = os.path.join(get_image_template_directory(), template_path)

        matches = [
            TalonRect(
                match.x + xoffset,
                match.y + yoffset,
                match.width,
                match.height
            )

            for match in locate.locate(
                template_file,
                rect=rect
            )
        ]

        return sorted(
            matches,
            key=lambda m: (m.x, m.y)
        )

    def mouse_helper_move_image_relative(
        template_path: str,
        disambiguator: Union[int, str]=0,
        xoffset: float=0,
        yoffset: float=0,
        region: Optional[TalonRect]=None
    ):
        """
        Moves the mouse relative to the template image given in template_path.

        :param template_path: Filename of the image to find. Can be an absolute path or
            if no '/' or '\\' character is specified, it is relative to the image
            templates directory.
        :param disambiguator: If there are multiple matches, use this to indicate
            which one you want to match. Matches are ordered left to right top to
            bottom. If disambiguator is an integer then it's just an index into that list.
            If it's the string "mouse" then it's the next match in the region to the right
            and down from the mouse after shifting back the offset amount and up and left
            half the size and width of the template. If it is "mouse_cycle" then if there
            are no further matches it will attempt to start from the top of the screen again.
            This is useful for iterating through rows in a table for example.
        :param xoffset: Amount to shift in the x direction relative to the
            center of the template.
        :param yoffset: Amount to shift in the y direction relative to the
            center of the template.
        :param region: The region to search for the template in. Either a screen relative
            TalonRect (see mouse_helper_calculate_relative_rect) or None to just use the
            active screen.
        """

        if region is None:
            rect = actions.user.mouse_helper_calculate_relative_rect(
                "0 0 -0 -0",
                "active_screen"
            )
        else:
            rect = region

        sorted_matches = actions.user.mouse_helper_find_template_relative(
            template_path,
            xoffset,
            yoffset,
            rect
        )

        if len(sorted_matches) == 0:
            # Throw an exception to cancel any following commands in the .talon file
            raise RuntimeError("No matches")

        if disambiguator in ("mouse", "mouse_cycle"):
            # math.ceil is needed here to ensure we only look at pixels after the current template match if we're
            # cycling between matches. math.floor would pick up the current one again.
            xnorm = math.ceil(actions.mouse_x() - sorted_matches[0].width / 2)
            ynorm = math.ceil(actions.mouse_y() - sorted_matches[0].height / 2)
            filtered_matches = [
                match
                for match in sorted_matches
                if (match.y == ynorm and match.x > xnorm) or match.y > ynorm
            ]

            if len(filtered_matches) > 0:
                match_rect = filtered_matches[0]
            elif disambiguator == "mouse_cycle":
                match_rect = sorted_matches[0]
            else:
                return
        else:
            if len(sorted_matches) <= disambiguator:
                return

            match_rect = sorted_matches[disambiguator]

        actions.mouse_move(
            math.ceil(rect.x + match_rect.x + (match_rect.width / 2)),
            math.ceil(rect.y + match_rect.y + (match_rect.height / 2)),
        )

    def mouse_helper_blob_picker(bounding_rectangle: TalonRect, min_gap_size: int=5):
        """
        Attempts to find clickable elements within the given bounding rectangle, then
        draws a labelled overlay allowing you to click or move the mouse to them.

        See mouse_helper_calculate_relative_rect for how to get the bounding rectangle.
        """

        image = screencap_to_image(bounding_rectangle)
        rects = calculate_blob_rects(image, bounding_rectangle)

        if len(rects) == 0:
            return

        actions.user.marker_ui_show(rects)
