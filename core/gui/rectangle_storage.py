from dataclasses import dataclass

from skia import Rect
from talon import actions

DIRECTORY_NAME = "gui_rectangles"


@dataclass
class RelativeRectangle:
    x: float
    y: float
    width: float
    height: float

    def __init__(self, screen: Rect, rect: Rect):
        self.width = rect.width / screen.width
        self.height = rect.height / screen.height
        self.x = (rect.x - screen.x) / screen.width
        self.y = (rect.y - screen.y) / screen.height

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
