"""
Draws a set of tags as a floating overlay. Allows users to indicate a particular
point on the screen by name.
"""

from typing import List, NamedTuple, Optional

import re

from talon import screen, canvas, ui, ctrl
from talon import cron
from talon.types import Rect
from talon.skia.bitmap import Bitmap
from talon.skia.typeface import Typeface


class MarkerUi:
    """
    Draws some markers pointing to particular locations on the screen
    """

    class Marker(NamedTuple):
        target_region: Rect
        label: str

    def __init__(self, markers: List[Marker]=[], screen_idx: Optional[int]=None):
        """
        Args:

            markers: List of marker locations and labels to show
            screen_idx: The Talon screen index we're showing the markers on. If
              None, then try to autoselect the active screen.
        """
        if screen_idx is None:
            active_window = ui.active_window()
            if active_window.id == -1:
                rect = ui.main_screen().rect
            else:
                rect = active_window.screen.rect

            self.can = canvas.Canvas.from_rect(rect)
        else:
            self.can = canvas.Canvas.from_screen(ui.screens()[screen_idx])

        self.markers = markers
        self.can.register("draw", self._draw)
        self.can.hide()
        self.visible = False

    def show(self):
        self.can.show()
        # Freeze stops draw being called at 60Hz and just uses the initial paint
        self.can.freeze()
        self.visible = True

    def hide(self):
        self.can.hide()
        self.visible = False

    def destroy(self):
        self.can.close()

    def find_rect(self, identifier: str) -> Optional[Rect]:
        """
        Finds the rectangle corresponding to the given identifier, or None if
        it couldn't be found.
        """

        for marker in self.markers:
            if marker.label == identifier:
                return marker.target_region

        return None

    def _draw(self, canvas):
        self.draw_markers(canvas, self.markers)

    @staticmethod
    def draw_markers(canvas, markers):
        """
        Draws out the given set of markers on the given canvas. Split out so that it can be 
        applied to canvases managed by other classes.
        """
        paint = canvas.paint
        paint.textsize = 12
        paint.typeface = Typeface.from_name('monospace')
        min_width = 10
        min_height = 10
        for marker in markers:
            region = marker.target_region

            # trect.x and .y are the offsets the text is printed at
            _, trect = paint.measure_text(marker.label)

            # Draw the box
            height = max(trect.height, min_height) + 2
            width = max(trect.width, min_width) + 2
            ypos = region.y + (region.height - height) // 2
            bg_rect = Rect(
                region.x + (region.width - width) // 2,
                ypos,
                width,
                height
            )

            paint.style = paint.Style.FILL
            paint.color = 'aaffffff'
            canvas.draw_rect(bg_rect)
            paint.color = 'black'

            # Draw the label
            paint.style = paint.Style.FILL
            canvas.draw_text(
                marker.label,
                bg_rect.x - trect.x + (bg_rect.width - trect.width) / 2,
                bg_rect.y - trect.y + (bg_rect.height - trect.height) / 2
            )
