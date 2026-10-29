import traceback
from dataclasses import dataclass

from skia import Rect
from talon import actions, screen

DIRECTORY_NAME = "gui_rectangles"


@dataclass
class RelativeRectangle:
    """The x and y are relative to an absolute rectangle's x and y. The coordinates and dimensions are fractions of the absolute rectangle's relevant dimension.`"""

    x: float
    y: float
    width: float
    height: float

    @staticmethod
    def from_rectangle(rect: Rect, input_screen_rect: Rect | None = None):
        if not input_screen_rect:
            input_screen_rect = screen.nearest(*rect.center).rect
        width = rect.width / input_screen_rect.width
        height = rect.height / input_screen_rect.height

        rect_x = rect.x
        rect_y = rect.y

        # clamp rectangle coordinates to the screen
        rect_x = max(input_screen_rect.x, rect_x)
        rect_x = min(input_screen_rect.x + input_screen_rect.width - rect.width, rect_x)
        rect_y = max(input_screen_rect.y, rect_y)
        rect_y = min(input_screen_rect.y + input_screen_rect.height - rect.height, rect_y)

        x = (rect_x - input_screen_rect.x) / input_screen_rect.width
        y = (rect_y - input_screen_rect.y) / input_screen_rect.height

        return RelativeRectangle(x, y, width, height)

    def compute_absolute_rectangle(self, screen_rect: Rect) -> Rect:
        """Create an absolute rectangle by putting it on the screen and scaling it by the screen's dimensions"""
        x = screen_rect.x + screen_rect.width * self.x
        y = screen_rect.y + screen_rect.height * self.y
        width = screen_rect.width * self.width
        height = screen_rect.height * self.height
        return Rect(x, y, width, height)


def report_error(exception: Exception, context: str):
    """Give a simple notification to the user and a more detailed message in the log"""
    message_prefix = f"Something went wrong {context}: "
    actions.app.notify(message_prefix + str(exception))
    print(message_prefix)
    traceback.print_tb(exception.__traceback__)


def get_relative_rectangle(id: str) -> RelativeRectangle | None:
    """Get the relative rectangle with the id from disk if possible. Otherwise return None"""
    if not id or not actions.user.stored_state_does_file_exist(DIRECTORY_NAME, id):
        return None
    try:
        text = actions.user.stored_state_get_text(DIRECTORY_NAME, id)
    except OSError as ex:
        report_error(ex, f"trying to load the relative rectangle for {id}")
        return None
    values = list(map(float, text.split(",")))
    return RelativeRectangle(*values)


def store_relative_rectangle(id: str, rectangle: RelativeRectangle):
    """Save the relative rectangle with the given id on disk so it can be retrieved with the id"""
    if not id:
        raise ValueError("You cannot store a relative rectangle without an id!")
    if not rectangle:
        raise ValueError("Tried to store a relative rectangle that was None!")
    text = ",".join(
        [str(v) for v in (rectangle.x, rectangle.y, rectangle.width, rectangle.height)]
    )
    try:
        actions.user.stored_state_set_value(DIRECTORY_NAME, id, text)
    except OSError as ex:
        report_error(ex, f"trying to store the relative rectangle for {id}")
