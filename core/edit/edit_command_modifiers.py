from dataclasses import dataclass
from typing import Callable
from contextlib import suppress

from talon import Module, actions

mod = Module()
mod.list("edit_modifier", desc="Modifiers for the edit command")


@dataclass
class EditModifier:
    type: str

@dataclass
class EditModifierCallback:
    modifier: str
    callback: Callable
    repeatable: False


@mod.capture(rule="{user.edit_modifier}")
def edit_modifier(m) -> EditModifier:
    return EditModifier(m.edit_modifier)


modifiers =  [
    EditModifierCallback("document", actions.edit.select_all, False), 
    EditModifierCallback("paragraph", actions.edit.select_paragraph, False),
    EditModifierCallback("word", actions.edit.extend_word_right,  True),
    EditModifierCallback("wordLeft",  actions.edit.extend_word_left,  True),
    EditModifierCallback("wordRight",  actions.edit.extend_word_right,  True),
    EditModifierCallback("left", actions.edit.extend_left,  True),
    EditModifierCallback("right",  actions.edit.extend_right,  True),
    EditModifierCallback("lineUp",  actions.edit.extend_line_up, True),
    EditModifierCallback("lineDown",  actions.edit.extend_line_down, True),
    EditModifierCallback("line",  actions.edit.select_line, False),
    EditModifierCallback("lineEnd",  actions.edit.extend_line_end, False),
    EditModifierCallback("lineStart",  actions.edit.extend_line_start, False),
    EditModifierCallback("fileStart",  actions.edit.extend_file_start,  False),
    EditModifierCallback("fileEnd",  actions.edit.extend_file_end,   False),
    EditModifierCallback("selection",  actions.skip,   False),
]

modifier_dictionary : dict[str, EditModifierCallback] = { item.modifier : item for item in modifiers}

def run_modifier_callback(modifier: EditModifier, count: int):
    modifier_type = modifier.type
    if modifier_type not in modifier_dictionary:
        raise ValueError(f"Unknown edit modifier: {modifier_type}")

    modifier = modifier_dictionary[modifier_type]
    count = 1 if not modifier.repeatable else count 
    for i in range(1, count + 1):
        modifier.callback()
