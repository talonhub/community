from talon import Context, actions, ui, Module, app, clip
import json
from typing import Any

mod = Module()


class NotSet:
    def __repr__(self):
        return "<argument not set>"


@mod.action_class
class Actions:
    def cursorless_command(
        action: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ):
        """Perform a cursorless command."""
        args = [
            json.loads(arg)
            for arg in [arg1, arg2, arg3, arg4, arg5]
            if arg is not NotSet
        ]

        actions.user.vscode(
            "cursorless.command",
            action,
            *args,
        )