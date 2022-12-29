"""
Exposes the Marker UI and associated functionality as actions.
"""

from typing import List

from talon import Module, Context, actions, registry, app
from talon.types import Rect as TalonRect

from .marker_ui import MarkerUi


mod = Module()
mod.tag("marker_ui_showing", desc="The marker UI labels are showing")
mod.list("marker_ui_label", desc="List of marker labels used by the marker UI")

ctx = Context()

marker_ui = None


def _populate_list():
    # Do this after boot to ensure that knausj has loaded first
    ctx.lists["user.marker_ui_label"] = registry.lists["user.letter"][0]

app.register("ready", _populate_list)


@mod.action_class
class MarkerUiActions:
    """
    Actions related to showing, hiding, and using the marker UI interface.
    """

    def marker_ui_show(rects: List[TalonRect]):
        """
        Shows the given markers in the Marker UI. They can then be clicked or moved
        to using other actions in this class.
        """

        global marker_ui

        if marker_ui is not None:
            marker_ui.destroy()

        markers = [
            MarkerUi.Marker(
                rect,
                label
            )
            for rect, label in zip(rects, ctx.lists["user.marker_ui_label"].values())
        ]

        marker_ui = MarkerUi(markers)

        marker_ui.show()
        ctx.tags = ["user.marker_ui_showing"]

    def marker_ui_hide():
        """
        Hides any visible marker UI
        """

        global marker_ui

        if marker_ui is not None:
            marker_ui.destroy()

        marker_ui = None
        ctx.tags = []

    def marker_ui_mouse_move(label: str):
        """
        Moves the mouse cursor to the label corresponding to the given label
        """

        global marker_ui

        if marker_ui is None:
            return

        rect = marker_ui.find_rect(label)

        if rect is None:
            return

        actions.mouse_move(
            rect.x + rect.width / 2,
            rect.y + rect.height / 2,
        )
