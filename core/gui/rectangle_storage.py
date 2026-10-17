from skia import Rect
from talon import actions

DIRECTORY_NAME = "gui_rectangles"


def get_rectangle(id: str) -> Rect | None:
    if not id:
        return None
    if not actions.user.stored_state_does_file_exist(DIRECTORY_NAME, id):
        return None
    text = actions.user.stored_state_get_text(DIRECTORY_NAME, id)
    x, y, width, height = [int(v) for v in text.split(",")]
    return Rect(x, y, width, height)


def store_rectangle(id: str, rectangle: Rect | None):
    if not id or not rectangle:
        return
    text = ",".join(
        [
            str(int(v))
            for v in (rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        ]
    )
    actions.user.stored_state_set_value(DIRECTORY_NAME, id, text)
