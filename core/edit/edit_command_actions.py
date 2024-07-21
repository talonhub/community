from dataclasses import dataclass
from typing import Callable, Union

from talon import Module, actions


@dataclass
class EditAction:
    type: str

    def __str__(self):
        return self.type


@dataclass
class EditInsertAction(EditAction):
    type = "insert"
    text: str


@dataclass
class EditFormatAction(EditAction):
    type = "applyFormatter"
    formatters: str


mod = Module()
mod.list("edit_action", desc="Actions for the edit command")


@mod.capture(rule="{user.edit_action}")
def edit_simple_action(m) -> EditSimpleAction:
    return EditSimpleAction(m.edit_action)


@mod.capture(rule="<user.edit_simple_action>")
def edit_action(m) -> EditAction:
    return m[0]


simple_action_callbacks: dict[str, Callable] = {
    "select": actions.skip,
    "goBefore": actions.edit.left,
    "goAfter": actions.edit.right,
    "copyToClipboard": actions.edit.copy,
    "cutToClipboard": actions.edit.cut,
    "pasteFromClipboard": actions.edit.paste,
    "insertLineAbove": actions.edit.line_insert_up,
    "insertLineBelow": actions.edit.line_insert_down,
    "insertCopyAfter": actions.edit.selection_clone,
    "delete": actions.edit.delete,
}


def get_action_callback(action: EditAction) -> Callable:
    action_type = action.type

    if action_type in simple_action_callbacks:
        return simple_action_callbacks[action_type]

    match action_type:
        case "insert":
            assert isinstance(action, EditInsertAction)
            return lambda: actions.insert(action.text)

        case "applyFormatter":
            assert isinstance(action, EditFormatAction)
            return lambda: actions.user.formatters_reformat_selection(action.formatters)

    raise ValueError(f"Unknown edit action: {action}")
