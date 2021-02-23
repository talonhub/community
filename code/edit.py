import time
from talon import Context, Module, actions, clip, ui

ctx = Context()
mod = Module()


@ctx.action_class("edit")
class edit_actions:
    def selected_text() -> str:
        with clip.capture() as s:
            actions.edit.copy()
        try:
            return s.get()
        except clip.NoChange:
            return ""


@mod.action_class
class Actions:
    def paste(text: str):
        """Pastes text and preserves clipboard"""

        with clip.revert():
            clip.set_text(text)
            actions.edit.paste()
            # sleep here so that clip.revert doesn't revert the clipboard too soon
            actions.sleep("150ms")

    def down_n(n: int):
        """Goes down n lines"""
        for _ in range(n):
            actions.edit.down()
            actions.sleep("10ms")

    def up_n(n: int):
        """Goes up n lines"""
        for _ in range(n):
            actions.edit.up()
            actions.sleep("10ms")

    def left_n(n: int):
        """Goes left n lines"""
        for _ in range(n):
            actions.edit.left()

    def right_n(n: int):
        """Goes right n lines"""
        for _ in range(n):
            actions.edit.right()
