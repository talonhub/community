from dataclasses import dataclass
from typing import Callable

from talon import Module, actions


@dataclass
class EditAction:
    type: str


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
def edit_simple_action(m) -> EditAction:
    return EditAction(m.edit_action)


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


def run_action_callback(action: EditAction):
    action_type = action.type

    if action_type in simple_action_callbacks:
        callback = simple_action_callbacks[action_type]
        callback()
        return

    match action_type:
        case "insert":
            assert isinstance(action, EditInsertAction)
            actions.insert(action.text)

        case "applyFormatter":
            assert isinstance(action, EditFormatAction)
            actions.user.formatters_reformat_selection(action.formatters)

        case _:
            raise ValueError(f"Unknown edit action: {action_type}")
