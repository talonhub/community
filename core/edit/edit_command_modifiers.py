from contextlib import suppress
from dataclasses import dataclass
from typing import Callable

from talon import Module, actions

mod = Module()
mod.list("edit_modifier", desc="Modifiers for the edit command")
mod.list(
    "edit_modifier_repeatable",
    desc="Modifiers for the edit command that are repeatable",
)


@dataclass
class EditModifier:
    type: str
    count: int = 1


@dataclass
class EditModifierCallback:
    modifier: str
    callback: Callable


@mod.capture(
    rule="({user.edit_modifier}) | ([<number_small>] {user.edit_modifier_repeatable})"
)
def edit_modifier(m) -> EditModifier:
    count = 1
    with suppress(AttributeError):
        count = m.number_small

    with suppress(AttributeError):
        type = m.edit_modifier

    with suppress(AttributeError):
        type = m.edit_modifier_repeatable

    return EditModifier(type, count=count)


modifiers = [
    EditModifierCallback("document", actions.edit.select_all),
    EditModifierCallback("paragraph", actions.edit.select_paragraph),
    EditModifierCallback("word", actions.edit.extend_word_right),
    EditModifierCallback("wordLeft", actions.edit.extend_word_left),
    EditModifierCallback("wordRight", actions.edit.extend_word_right),
    EditModifierCallback("left", actions.edit.extend_left),
    EditModifierCallback("right", actions.edit.extend_right),
    EditModifierCallback("lineUp", actions.edit.extend_line_up),
    EditModifierCallback("lineDown", actions.edit.extend_line_down),
    EditModifierCallback("line", actions.edit.select_line),
    EditModifierCallback("lineEnd", actions.edit.extend_line_end),
    EditModifierCallback("lineStart", actions.edit.extend_line_start),
    EditModifierCallback("fileStart", actions.edit.extend_file_start),
    EditModifierCallback("fileEnd", actions.edit.extend_file_end),
    EditModifierCallback("selection", actions.skip),
]

modifier_dictionary: dict[str, EditModifierCallback] = {
    item.modifier: item for item in modifiers
}


def run_modifier_callback(modifier: EditModifier):
    modifier_type = modifier.type
    if modifier_type not in modifier_dictionary:
        raise ValueError(f"Unknown edit modifier: {modifier_type}")

    count = modifier.count
    modifier = modifier_dictionary[modifier_type]
    for i in range(1, count + 1):
        modifier.callback()
