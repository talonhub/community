import re
from typing import Optional

from talon.experimental.textarea import (
    DarkThemeLabels,
    LightThemeLabels,
    Span,
    TextArea,
)

word_matcher = re.compile(r"([^\s]+)(\s*)")


def calculate_text_anchors(text, cursor_position, anchor_labels=None):
    """
    Produces an iterator of (anchor, start_word_index, end_word_index, last_space_index)
    tuples from the given text. Each tuple indicates a particular point you may want to
    reference when editing along with some useful ranges you may want to operate on.

    - text is the text you want to process.
    - cursor_position is the current position of the cursor, anchors will be placed around
      this.
    - anchor_labels is a list of characters you want to use for your labels.
    - *index is just a character offset from the start of the string (e.g. the first character is at index 0)
    - end_word_index is the index of the character after the last one included in the
      anchor. That is, you can use it with a slice directly like [start:end]
    - anchor is a short piece of text you can use to identify it (e.g. 'a', or '1').
    """
    anchor_labels = anchor_labels or "abcdefghijklmnopqrstuvwxyz"

    if len(text) == 0:
        return []

    # Find all the word spans
    matches = []
    cursor_idx = None
    for match in word_matcher.finditer(text):
        matches.append((match.start(), match.end() - len(match.group(2)), match.end()))
        if matches[-1][0] <= cursor_position and matches[-1][2] >= cursor_position:
            cursor_idx = len(matches) - 1

    # Now work out what range of those matches are getting an anchor. The aim is
    # to centre the anchors around the cursor position, but also to use all the
    # anchors.
    anchors_before_cursor = len(anchor_labels) // 2
    anchor_start_idx = max(0, cursor_idx - anchors_before_cursor)
    anchor_end_idx = min(len(matches), anchor_start_idx + len(anchor_labels))
    anchor_start_idx = max(0, anchor_end_idx - len(anchor_labels))

    # Now add anchors to the selected matches
    for i, anchor in zip(range(anchor_start_idx, anchor_end_idx), anchor_labels):
        word_start, word_end, whitespace_end = matches[i]
        yield (anchor, word_start, word_end, whitespace_end)


class DraftManager:
    """
    API to the draft window
    """

    def __init__(self):
        self.area = TextArea()
        self.area.title = "Talon Draft"
        self.area.value = ""
        self.area.register("label", self._update_labels)
        self.set_styling()

    def set_styling(self, theme="dark", text_size=20, label_size=20, label_color=None):
        """
        Allow settings the style of the draft window. Will dynamically
        update the style based on the passed in parameters.
        """

        area_theme = DarkThemeLabels if theme == "dark" else LightThemeLabels
        theme_changes = {
            "text_size": text_size,
            "label_size": label_size,
        }
        if label_color is not None:
            theme_changes["label"] = label_color
        self.area.theme = area_theme(**theme_changes)

    def show(self, text: Optional[str] = None):
        """
        Show the window. If text is None then keep the old contents,
        otherwise set the text to the given value.
        """

        if text is not None:
            self.area.value = text
        self.area.show()

    def hide(self):
        """
        Hide the window.
        """

        self.area.hide()

    def get_text(self) -> str:
        """
        Gets the context of the text area
        """

        return self.area.value

    def get_rect(self) -> "talon.types.Rect":
        """
        Get the Rect for the window
        """

        return self.area.rect

    def reposition(
        self,
        xpos: Optional[int] = None,
        ypos: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        """
        Move the window or resize it without having to change all properties.
        """

        rect = self.area.rect
        if xpos is not None:
            rect.x = xpos

        if ypos is not None:
            rect.y = ypos

        if width is not None:
            rect.width = width

        if height is not None:
            rect.height = height

        self.area.rect = rect

    def select_text(
        self, start_anchor, end_anchor=None, include_trailing_whitespace=False
    ):
        """
        Selects the word corresponding to start_anchor. If end_anchor supplied, selects
        from start_anchor to the end of end_anchor. If include_trailing_whitespace=True
        then also selects trailing space characters (useful for delete).
        """

        start_index, end_index, last_space_index = self.anchor_to_range(start_anchor)
        if end_anchor is not None:
            _, end_index, last_space_index = self.anchor_to_range(end_anchor)

        if include_trailing_whitespace:
            end_index = last_space_index

        self.area.sel = Span(start_index, end_index)

    def position_caret(self, anchor, after=False):
        """
        Positions the caret before the given anchor. If after=True position it directly after.
        """

        start_index, end_index, _ = self.anchor_to_range(anchor)
        index = end_index if after else start_index

        self.area.sel = index

    def anchor_to_range(self, anchor):
        anchors_data = calculate_text_anchors(
            self._get_visible_text(), self.area.sel.left
        )
        for loop_anchor, start_index, end_index, last_space_index in anchors_data:
            if anchor == loop_anchor:
                return (start_index, end_index, last_space_index)

        raise RuntimeError(f"Couldn't find anchor {anchor}")

    def _update_labels(self, _visible_text):
        """
        Updates the position of the labels displayed on top of each word
        """

        anchors_data = calculate_text_anchors(
            self._get_visible_text(), self.area.sel.left
        )
        return [
            (Span(start_index, end_index), anchor)
            for anchor, start_index, end_index, _ in anchors_data
        ]

    def _get_visible_text(self):
        # Placeholder for a future method of getting this
        return self.area.value


if False:
    # Some code for testing, change above False to True and edit as desired
    draft_manager = DraftManager()
    draft_manager.show(
        "This is a line of text\nand another line of text and some more text so that the line gets so long that it wraps a bit.\nAnd a final sentence"
    )
    draft_manager.reposition(xpos=100, ypos=100)
    draft_manager.select_text("c")
