from dataclasses import dataclass
from typing import Callable

from talon import Module, actions

mod = Module()
mod.list("edit_modifier", desc="Modifiers for the edit command")


@dataclass
class EditModifier:
    type: str


@mod.capture(rule="{user.edit_modifier}")
def edit_modifier(m) -> EditModifier:
    return EditModifier(m.edit_modifier)


modifier_callbacks = {
    "document": actions.edit.select_all,
    "paragraph": actions.edit.select_paragraph,
    "word": actions.edit.select_word,
    "line": actions.edit.select_line,
    "lineEnd": actions.user.select_line_end,
    "lineStart": actions.user.select_line_start,
}


def get_modifier_callback(modifier: EditModifier) -> Callable:
    key = str(modifier)

    if key in modifier_callbacks:
        return modifier_callbacks[key]

    raise ValueError(f"Unknown edit modifier: {modifier}")
