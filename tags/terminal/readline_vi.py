from talon import Context, actions
from typing import Callable
from dataclasses import dataclass
from time import sleep


ctx = Context()
ctx.matches = """
tag: user.readline_vi
"""

@dataclass
class PendingSelection():
    motion: str
    endAction: str
    count: int = 1


# @dataclass
# class EditModifier:
#     type: str
#     count: int = 1

@dataclass
class EditModifierCallback:
    modifier: str
    callback: str


pendingSelection: PendingSelection = None


modifiers: dict[str, EditModifierCallback] = {
    item.modifier: item for item in
    [
        EditModifierCallback("word", "iwi"),
        EditModifierCallback("wordLeft", "bi"),
        EditModifierCallback("wordRight", "wa"),
        EditModifierCallback("line", "_i"),
        EditModifierCallback("lineEnd", "$a"),
        EditModifierCallback("lineStart", "0i"),
    ]
}

edit_action_vi_keys: dict[str, str] = {
        "cut": "c",
        "delete": "c",
        "goBefore": "",
        "goAfter": "",
        # We can't actually use the clipboard for these operations
        "copyToClipboard": "y",
        "cutToClipboard": "c",
        "pasteFromClipboard": "y",
}

def normal_cmd(keys):
    actions.key("escape")
    # sleep to avoid interpreting as an escape sequence
    sleep(0.2)
    actions.insert(keys)


# This operates on a paradigm of staying in insert mode, but at least allows standard community text editing commands if the user has set their shell to vi mode in read line.
# Vi bindings may occasionally have an issue at the start or end of a line, because the cursor may get stuck and the subsequent reentering of insert mode will leave the cursor one before the end of the line.
@ctx.action_class("edit")
class EditActions:
    # Map possible edit actions to letters, run the edit action first, then modifier letter/callback
    # def edit_command(action, modifier):
    #     """Perform edit command"""
    #     # count = modifier.count
    #     actions.key("escape")
    #     actions.insert(action.type)
    #     actions.insert(modifier.callback)

    def delete_line():
        normal_cmd("cc")

    def word_left():
        normal_cmd("bi")

    def word_right():
        actions.key("escape")
        sleep(0.1)
        # the escape key shifts the position one to the left
        actions.key("right")
        actions.insert("w")
        # Unfortunately this will end up one character before the end if we have reached the last word of the line
        actions.insert("i")

    def line_end():
        normal_cmd("A")

    def line_start():
        normal_cmd("I")

    def undo():
        # Technically control underscore works in vi readline mode as well, but this also works in zsh
        normal_cmd("ua")

    # TODO: we don't want to overwrite the system's paste action, should this be a separate command?
    # def paste():

    # Read line doesn't have any selection mechanism, so instead we add any "selections" to a pending selection object, which get applied when the edit next action is called
    def extend_line_end():
        global pendingSelection
        pendingSelection = PendingSelection("$", "a")

    def extend_line_start():
        global pendingSelection
        pendingSelection = PendingSelection("0", "i")

    def extend_word_left():
        global pendingSelection
        pendingSelection = PendingSelection("b", "i")

    def extend_word_right():
        global pendingSelection
        pendingSelection = PendingSelection("w", "i")



@ctx.action_class("user")
class Actions:

    def run_action_callback(action):
        """
        Run a callback that applies an edit action to the selected
        Intended for internal use and overwriting
        """
        action_type = action.type

        if action_type in edit_action_vi_keys:
            normal_cmd(edit_action_vi_keys[action_type])
        else:
            try:
                callback = actions.user.get_simple_action_callback(action_type)
                callback()
            except KeyError as ex:
                print("readline_vi only supports simple action callbacks")
                return

        actions.insert(str(pendingSelection.count))
        actions.insert(pendingSelection.motion)
        actions.insert(pendingSelection.endAction)

    # def run_modifier_callback(modifier: EditModifier):
    #     """
    #     Store pending text movement callbacks for the next action to apply to
    #     """
    #     count = modifier.count
    #     modifier = actions.user.get_modifier_callback(EditModifier)
    #     pendingSelection = PendingSelection(
    #         modifier.callback, "", range(1, count + 1)
    #     )

    # def edit_command(action: EditAction, modifier: EditModifier):
    #     """Perform edit command with associated modifier. Same as function in
    #     edit command actions except calling action before modifier."""
    #     key = (action.type, modifier.type)
    #     count = modifier.count

    #     if key in custom_callbacks:
    #         custom_callbacks[key](action, modifier.type, count)
    #         return

    #     elif key in compound_actions:
    #         for i in range(1, count + 1):
    #             compound_actions[key]()
    #         return

    #     run_action_callback(action)
    #     run_modifier_callback(modifier)

    def cut_line():
        actions.key("escape")
        actions.insert("cc")

    # def delete_word():
    #     actions.key("escape")
    #     actions.insert("ciw")

    # def delete_word_left():
    #     actions.key("ctrl-w")

    # def delete_word_right():
    #     actions.user.cut_word_right()

    def cut_word_right():
        actions.key("escape")
        actions.insert("cw")

    def cut_word_left():
        actions.key("escape")
        actions.insert("cb")

    def copy_word_left():
        actions.key("escape")
        actions.key("right")
        # Yanking backwards doesn't consider the current character the cursor is on, so we need to move the cursor one to the right
        actions.insert("ybi")

    def copy_word_right():
        actions.key("escape")
        actions.insert("ywa")

    # def cut_word():
    #     actions.key("escape")]
    #     actions.insert("ciw")

    # def copy_word():
    #     actions.key("escape")
    #     actions.insert("yiwa")

    # def delete_word():
    #     actions.key("escape")
    #     actions.insert("ciw")
