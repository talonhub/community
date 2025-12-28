from dataclasses import dataclass
from typing import Optional

from talon import Module

mod = Module()


@dataclass
class TimestampedText:
    text: str
    start: float
    end: float


@dataclass
class TextRange:
    start: Optional[TimestampedText]
    after_start: bool
    end: Optional[TimestampedText]
    before_end: bool


@dataclass
class TextPosition:
    text: TimestampedText
    position: str


@mod.capture(rule="<user.prose>")
def timestamped_prose_only(m) -> TimestampedText:
    """user.prose with timestamps."""
    return TimestampedText(text=m.prose, start=m.prose_start, end=m.prose_end)


@mod.capture(rule="{user.onscreen_ocr_text}")
def onscreen_text(m) -> TimestampedText:
    """Timestamped text appearing onscreen."""
    return TimestampedText(
        text=m[0], start=m.onscreen_ocr_text_start, end=m.onscreen_ocr_text_end
    )


@mod.capture(rule="<self.timestamped_prose_only> | <self.onscreen_text>")
def timestamped_prose(m) -> TimestampedText:
    """Timestamped prose or onscreen text."""
    return m[0]


@mod.capture(rule="[before | after] <self.timestamped_prose>")
def prose_position(m) -> TextPosition:
    """Position relative to prose."""
    return TextPosition(
        text=m.timestamped_prose,
        position=m[0] if m[0] in ("before", "after") else "",
    )


@mod.capture(
    rule="<self.one_ended_prose_range> | <self.prose_position> through <self.prose_position>"
)
def prose_range(m) -> TextRange:
    """A range of onscreen text."""
    if hasattr(m, "one_ended_prose_range"):
        return m.one_ended_prose_range
    return TextRange(
        start=m.prose_position_1.text,
        after_start=m.prose_position_1.position == "after",
        end=m.prose_position_2.text,
        before_end=m.prose_position_2.position == "before",
    )


@mod.capture(rule="[through | from] <self.prose_position>")
def one_ended_prose_range(m) -> TextRange:
    """A range of onscreen text with only start or end specified."""
    has_through = m[0] == "through"
    has_from = m[0] == "from"
    # As a convenience, allow dropping "through" or "from" if position is provided.
    if m.prose_position.position:
        return TextRange(
            start=None,
            after_start=False,
            end=m.prose_position.text,
            before_end=m.prose_position.position == "before",
        )
    elif has_through:
        # Select current cursor point through the text after the cursor.
        return TextRange(
            start=None,
            after_start=False,
            end=m.prose_position.text,
            before_end=False,
        )
    elif has_from:
        # Select from the text before the cursor up to the current cursor point.
        return TextRange(
            start=None,
            after_start=False,
            end=m.prose_position.text,
            before_end=True,
        )
    else:
        # Select the phrase itself.
        return TextRange(
            start=m.prose_position.text,
            after_start=m.prose_position.position == "after",
            end=None,
            before_end=False,
        )
