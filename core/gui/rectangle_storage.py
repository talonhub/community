from dataclasses import dataclass

from skia import Rect
from talon import actions, screen

DIRECTORY_NAME = "gui_rectangles"


@dataclass
class RelativeRectangle:
    x: float
    y: float
    width: float
    height: float

    @staticmethod
    def from_rectangle(rect: Rect, input_screen: Rect | None=None):
        if not input_screen:
            input_screen = screen.containing(rect.x, rect.y).rect
        width = rect.width / input_screen.width
        height = rect.height / input_screen.height
        x = (rect.x - input_screen.x) / input_screen.width
        y = (rect.y - input_screen.y) / input_screen.height
        return RelativeRectangle(x, y, width, height)

    def compute_absolute_rectangle(self, screen: Rect) -> Rect:
        x = screen.x + screen.width * self.x
        y = screen.y + screen.height * self.y
        width = screen.width * self.width
        height = self.height * screen.height
        return Rect(x, y, width, height)


def get_relative_rectangle(id: str) -> RelativeRectangle | None:
    if not id:
        return None
    if not actions.user.stored_state_does_file_exist(DIRECTORY_NAME, id):
        return None
    text = actions.user.stored_state_get_text(DIRECTORY_NAME, id)
    x, y, width, height = [float(v) for v in text.split(",")]
    return RelativeRectangle(x, y, width, height)


def store_relative_rectangle(id: str, rectangle: RelativeRectangle | None):
    if not id or not rectangle:
        return
    text = ",".join(
        [str(v) for v in (rectangle.x, rectangle.y, rectangle.width, rectangle.height)]
    )
    actions.user.stored_state_set_value(DIRECTORY_NAME, id, text)
