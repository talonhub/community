from dataclasses import dataclass
from typing import Callable

from talon import Context, actions

sleep = actions.sleep

ctx = Context()
ctx.matches = """
tag: user.readline_vi
"""


@dataclass
class PendingSelection:
    motion: str
    endAction: str
    count: int = 1


pending_selection: PendingSelection | None = None


# using d instead of c for removal so that we remain in normal mode and the character sent to exit normal mode doesn't get inserted
edit_action_vi_keys: dict[str, str] = {
    "cut": "d",
    "delete": "d",
    "goBefore": "",
    "goAfter": "",
    # We can't actually use the clipboard for these operations
    # "copyToClipboard": "y",
    # "cutToClipboard": "d",
    # "pasteFromClipboard": "y",
}


def normal_cmd(keys):
    actions.key("escape")
    # sleep to avoid interpreting as an escape sequence
    sleep(0.2)
    actions.key(keys)


def add_pending(motion, end):
    global pending_selection
    if pending_selection and pending_selection.motion == motion:
        pending_selection.count += 1
    else:
        pending_selection = PendingSelection(motion, end)


def delete_word_right():
    # need a custom function, because otherwise the right key that moves the cursor will interfere with the pending action
    # the normal escape key shifts the position one to the left, so let's undo that first
    normal_cmd("right d w i")


simple_action_callbacks: dict[str, Callable] = {}

custom_callbacks = {}

compound_actions = {
    ("delete", "word"): lambda: normal_cmd("d i w"),
    ("delete", "wordLeft"): lambda: actions.key("ctrl-w"),
    ("delete", "wordRight"): delete_word_right,

    ("cutToClipboard", "word"): lambda: normal_cmd("c i w "),
    ("cutToClipboard", "wordLeft"): lambda: normal_cmd("c b"),
    ("cutToClipboard", "wordRight"): lambda: normal_cmd("c w"),

    ("copyToClipboard", "word"): lambda: normal_cmd("y i w"),
    ("copyToClipboard", "wordLeft"):
    # Yanking backwards doesn't consider the current character the cursor is on, so we need to move the cursor one to the right
    lambda: normal_cmd("right y b i"),
    ("copyToClipboard", "wordRight"): lambda: normal_cmd("y w a")
}


# This operates on a paradigm of staying in insert mode, but at least allows standard community text editing commands if the user has set their shell to vi mode in read line.
# Vi bindings may occasionally have an issue at the start or end of a line, because the cursor may get stuck and the subsequent reentering of insert mode will leave the cursor one before the end of the line.
@ctx.action_class("edit")
class EditActions:
    def delete_line():
        normal_cmd("c c")

    def word_left():
        normal_cmd("b i")

    def word_right():
        # the escape key shifts the position one to the left, sir undo that first to ensure we have not ended up on the previous word
        normal_cmd("right")
        actions.key("w")
        # Unfortunately this will end up one character before the end if we have reached the last word of the line, but using 'a' would result in always being in the second character of any other word in the line
        actions.key("i")

    def line_end():
        normal_cmd("A")

    def line_start():
        normal_cmd("I")

    def undo():
        # Technically control underscore works in vi readline mode as well, but this also works in zsh
        normal_cmd("u i")

    def redo():
        # This does not work in readline (no redo command at all), but will work in zsh and other vi emulators
        normal_cmd("ctrl-r a")

    # TODO: we don't want to overwrite the system's paste action, should this be a separate command?
    # def paste():

    # Read line doesn't have any selection mechanism, so instead we add any "selections" to a pending selection object, which get applied when the edit next action is called
    def extend_line_end():
        add_pending("$", "a")

    def extend_line_start():
        pendingSelection = add_pending("0", "i")

    def extend_word_left():
        add_pending("b", "i")

    def extend_word_right():
        add_pending("w", "i")


@ctx.action_class("user")
class Actions:
    def run_edit_action_callback(action):
        """
        Run a callback that applies an edit action to the selected
        Intended for internal use and overwriting
        """
        global pending_selection
        action_type = action.type

        if action_type in edit_action_vi_keys:
            normal_cmd(edit_action_vi_keys[action_type])
        else:
            callback = actions.user.get_simple_edit_action_callback(action_type)
            if callback:
                callback()
            else:
                print("readline_vi only supports simple action callbacks")
                return

        if not pending_selection:
            print("readline_vi: No pending selection")
            return
        actions.insert(str(pending_selection.count))
        actions.insert(pending_selection.motion)
        actions.insert(pending_selection.endAction)
        pending_selection = None

    # Cut and copy actions can't use the system clipboard,
    # which we actually want to reserve for copy/paste at terminal anyway,
    # but we can at least repast them by manually using 'p' if needed
    def cut_line():
        normal_cmd("c c")

    def get_simple_edit_action_callback(action_type: str) -> Callable | None:
        """Convert a edit action type created from a string into its associated Callback.
        If it can't find one in this file, it will try the next most specific community version
        """
        cb = simple_action_callbacks.get(action_type)
        if not cb:
            cb = actions.next(action_type)
        return cb

    def get_compound_edit_action_modifier_callback(
        pair: tuple[str, str],
    ) -> Callable | None:
        return (
            custom_callbacks.get(pair)
            or compound_actions.get(pair)
            or actions.next(pair)
        )
