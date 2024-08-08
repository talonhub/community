from typing import Callable
from talon import Context, Module, actions, settings

mod = Module()

mod.apps.libreoffice = """
os: linux
and app.exe: soffice.bin
"""

ctx = Context()
ctx.matches = r"""
app: libreoffice
"""

# Unlike most other applications, LibreOffice does not move the cursor to the
# start/end of the selection when pressing left/right. Instead, it only moves
# the cursor one step. 
@ctx.action_class("user")
class UserActions:
    def dictation_peek(left, right):
        # clobber selection if it exists
        actions.key("space backspace")
        before, after = None, None
        if left:
            actions.edit.extend_word_left()
            actions.edit.extend_word_left()
            before = actions.edit.selected_text()
            repeat_action(actions.edit.right,len(before))
        if right:
            actions.edit.extend_word_right()
            actions.edit.extend_word_right()
            after = actions.edit.selected_text()
            repeat_action(actions.edit.left,len(after))
        return (before, after)


def repeat_action(action: Callable, count: int):
    for _ in range(count):
        action()
