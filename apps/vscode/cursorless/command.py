from talon import Context, actions, ui, Module, app, clip
import json
from typing import Any
from ..command_client import NotSet


mod = Module()


@mod.action_class
class Actions:
    def cursorless_single_target_command(
        action: str,
        target: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
    ):
        """Execute single-target cursorlses command"""
        actions.user.vscode_and_wait(
            "cursorless.command",
            action,
            [json.loads(target)],
            arg1,
            arg2,
            arg3,
        )
