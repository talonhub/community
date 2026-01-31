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


@mod.action_class
class Actions:
    def run_edit_action_callback(action: EditAction):
        """
        Run a callback that applies an edit action to the selected
        Intended for internal use and overwriting
        """
        action_type = action.type

        callback = actions.user.get_simple_edit_action_callback(action_type)
        if callback:
            callback()
            return

        match action_type:
            case EditInsertAction.type:
                assert isinstance(action, EditInsertAction)
                actions.insert(action.text)

            case EditWrapAction.type:
                assert isinstance(action, EditWrapAction)
                # triggered by e.g. "quad wrap word left"
                actions.user.delimiter_pair_wrap_selection(action.pair)

            case EditFormatAction.type:
                assert isinstance(action, EditFormatAction)
                actions.user.formatters_reformat_selection(action.formatters)

            case _:
                raise ValueError(f"Unknown edit action: {action_type}")

    def get_simple_edit_action_callback(action_type: str) -> Callable | None:
        """Convert a edit action type created from a string into its associated Callback"""
        return simple_action_callbacks.get(action_type)
