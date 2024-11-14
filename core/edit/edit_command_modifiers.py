from dataclasses import dataclass
from typing import Callable
from contextlib import suppress

from talon import Module, actions

mod = Module()
mod.list("edit_modifier", desc="Modifiers for the edit command")


@dataclass
class EditModifier:
    type: str
    count: int


@mod.capture(rule="{user.edit_modifier} [<number_small>]")
def edit_modifier(m) -> EditModifier:
    count = 1
    with suppress(AttributeError):
        count = m.number_small
    return EditModifier(m.edit_modifier, count)


modifier_callbacks: dict[str, Callable] = {
    "document": actions.edit.select_all,
    "paragraph": actions.edit.select_paragraph,
    "word": actions.edit.select_word,
    "wordLeft": actions.edit.extend_word_left,
    "wordRight": actions.edit.extend_word_right,
    "left": actions.edit.extend_left,
    "right": actions.edit.extend_right,
    "lineUp": actions.edit.extend_line_up,
    "lineDown": actions.edit.extend_line_down,
    "line": actions.edit.select_line,
    "lineEnd": actions.user.select_line_end,
    "lineStart": actions.user.select_line_start,
    "fileStart": actions.edit.extend_file_start, 
    "fileEnd": actions.edit.extend_file_end, 
}

def run_modifier_callback(modifier: EditModifier):
    modifier_type = modifier.type
    count = modifier.count
    if modifier_type not in modifier_callbacks:
        raise ValueError(f"Unknown edit modifier: {modifier_type}")

    callback = modifier_callbacks[modifier_type]

    for i in range(1, count + 1):
        callback()
