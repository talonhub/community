from typing import Callable

from talon import Context, actions, clip

ctx = Context()
ctx.matches = r"""
tag: user.readline
"""


@ctx.action_class("edit")
class EditActions:
    def delete_line():
        actions.edit.line_end()
        actions.key("ctrl-u")

    def word_left():
        actions.key("alt-b")

    def word_right():
        actions.key("alt-f")

    def line_end():
        actions.key("ctrl-e")

    def line_start():
        actions.key("ctrl-a")

    def undo():
        actions.key("ctrl-_")


# Wraps a method in a clip revert.
# Might actually not be necessary for readline because in the default implementation it uses a seperate clipboard to the desktop
# Though left in in case that has been modified
def with_clip_revert(f: Callable) -> Callable:

    def wrapped_method():
        with clip.revert():
            f()

    return wrapped_method


def with_selection_revert(f: Callable) -> Callable:
    def wrapped_method():
        f()
        actions.key("ctrl-y")

    return wrapped_method


def cut_word():
    actions.edit.word_left()
    actions.user.cut_word_right()


def cut_line_start():
    actions.key("ctrl-x backspace")


def cut_line_end():
    actions.key("ctrl-k")


compound_actions = {
    # Delete
    ("delete", "wordLeft"): with_clip_revert(actions.user.cut_word_left),
    ("delete", "wordRight"): with_clip_revert(actions.user.cut_word_right),
    ("delete", "word"): with_clip_revert(cut_word),
    ("delete", "line"): with_clip_revert(actions.user.cut_line),
    ("delete", "lineStart"): with_clip_revert(cut_line_start),
    ("delete", "lineEnd"): with_clip_revert(cut_line_end),
    # Copy
    ("copyToClipboard", "wordLeft"): with_selection_revert(actions.user.cut_word_left),
    ("copyToClipboard", "wordRight"): with_selection_revert(
        actions.user.cut_word_right
    ),
    ("copyToClipboard", "word"): with_selection_revert(cut_word),
    ("copyToClipboard", "line"): with_selection_revert(actions.user.cut_line),
    ("copyToClipboard", "lineStart"): with_selection_revert(cut_line_start),
    ("copyToClipboard", "lineEnd"): with_selection_revert(cut_line_end),
    # Cut
    ("cutToClipboard", "wordLeft"): actions.user.cut_word_left,
    ("cutToClipboard", "wordRight"): actions.user.cut_word_right,
    ("cutToClipboard", "word"): cut_word,
    ("cutToClipboard", "line"): actions.user.cut_line,
    ("cutToClipboard", "lineStart"): cut_line_start,
    ("cutToClipboard", "lineEnd"): cut_line_end,
}


@ctx.action_class("user")
class Actions:
    def cut_line():
        actions.edit.line_start()
        actions.key("ctrl-k")

    def cut_word_left():
        actions.key("ctrl-w")

    def cut_word_right():
        actions.key("alt-d")

    def copy_word_left():
        actions.user.cut_word_left()
        actions.key("ctrl-y")

    def copy_word_right():
        actions.user.cut_word_right()
        actions.key("ctrl-y")

    def get_compound_edit_action_modifier_callback(
        pair: tuple[str, str],
    ) -> Callable | None:
        return compound_actions.get(pair) or actions.next(pair)
