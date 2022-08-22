import string
from pickle import FALSE
from typing import Any

from talon import Context, Module, actions

from .command_client import NoFileServerException, NotSet

ctx = Context()

ctx.matches = r"""
app: vscode
"""
ctx.tags = ["user.command_client"]
mod = Module()


def command_client_fallback(command_id: str):
    """Execute command via command palette. Preserves the clipboard."""
    actions.user.command_palette()
    actions.user.paste(command_id)
    actions.key("enter")
    print(
        "Command issues via command palette for better performance install the VSCode extension for Talon"
    )


@ctx.action_class("user")
class VsCodeAction:
    def command_server_directory() -> string:
        return "vscode-command-server"


@mod.action_class
class Actions:
    def vscode(command_id: str):
        """Execute command via vscode command server, if available, or fallback
        to command palette."""
        try:
            actions.user.run_command(command_id)
        except NoFileServerException:
            command_client_fallback(command_id)

    def vscode_and_wait(command_id: str):
        """Execute command via vscode command server, if available, and wait
        for command to finish.  If command server not available, uses command
        palette and doesn't guarantee that it will wait for command to
        finish."""
        try:
            actions.user.run_command_and_wait(command_id)
        except NoFileServerException:
            command_client_fallback(command_id)

    def vscode_with_plugin(
        command_id: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ):
        """Execute command via vscode command server."""
        actions.user.run_command(
            command_id,
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
        )

    def vscode_with_plugin_and_wait(
        command_id: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ):
        """Execute command via vscode command server and wait for command to finish."""
        actions.user.run_command_with_plugin_and_wait(
            command_id, arg1, arg2, arg3, arg4, arg5
        )

    def vscode_get(
        command_id: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ) -> Any:
        """Execute command via vscode command server and return command output."""
        return actions.user.run_command_get(command_id, arg1, arg2, arg3, arg4, arg5)
