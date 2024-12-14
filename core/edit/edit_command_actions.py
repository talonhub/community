from dataclasses import dataclass
from typing import Callable, Union

from talon import Module, actions


@dataclass
class EditSimpleAction:
    """ "Simple" actions are actions that don't require any arguments, only a type (select, copy, delete, etc.)"""

    type: str

    def __str__(self):
        return self.type


@dataclass
class EditInsertAction:
    type = "insert"
    text: str

    def __str__(self):
        return self.type


@dataclass
class EditWrapAction:
    type = "wrapWithDelimiterPair"
    pair: list[str]

    def __str__(self):
        return self.type


@dataclass
class EditFormatAction:
    type = "applyFormatter"
    formatters: str

    def __str__(self):
        return self.type


EditAction = Union[
    EditSimpleAction,
    EditInsertAction,
    EditWrapAction,
    EditFormatAction,
]

mod = Module()
mod.list("edit_action", desc="Actions for the edit command")


@mod.capture(rule="{user.edit_action}")
def edit_simple_action(m) -> EditSimpleAction:
    return EditSimpleAction(m.edit_action)


@mod.capture(rule="<user.delimiter_pair> wrap")
def edit_wrap_action(m) -> EditWrapAction:
    return EditWrapAction(m.delimiter_pair)


@mod.capture(rule="<user.formatters> format")
def edit_format_action(m) -> EditFormatAction:
    return EditFormatAction(m.formatters)


@mod.capture(
    rule="<user.edit_simple_action> | <user.edit_wrap_action> | <user.edit_format_action>"
)
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

        case "wrapWithDelimiterPair":
            assert isinstance(action, EditWrapAction)
            return lambda: actions.user.delimiter_pair_wrap_selection(action.pair)

        case "applyFormatter":
            assert isinstance(action, EditFormatAction)
            actions.user.formatters_reformat_selection(action.formatters)

        case _:
            raise ValueError(f"Unknown edit action: {action_type}")
