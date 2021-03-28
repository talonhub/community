import requests
from typing import Any
from talon import Module, actions
from pathlib import Path
from tempfile import gettempdir


mod = Module()


class NotSet:
    def __repr__(self):
        return "<argument not set>"


def run_vscode_command(
    command: str,
    *args: str,
    wait_for_finish: bool = False,
    expect_response: bool = False,
):
    """Execute command via vscode command server."""
    # NB: This is a hack to work around the fact that talon doesn't support
    # variable argument lists
    args = list(
        filter(
            lambda x: x is not NotSet,
            args,
        )
    )

    port_file_path = Path(gettempdir()) / "vscode-port"
    port = port_file_path.read_text()

    response = requests.post(
        f"http://localhost:{port}/execute-command",
        json={
            "commandId": command,
            "args": args,
            "waitForFinish": wait_for_finish,
            "expectResponse": expect_response,
        },
        timeout=(0.05, 3.05),
    )
    response.raise_for_status()

    actions.sleep("25ms")

    if expect_response:
        return response.json()


@mod.action_class
class Actions:
    def vscode(
        command: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ):
        """Execute command via vscode command server."""
        run_vscode_command(
            command,
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
        )

    def vscode_and_wait(
        command: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ):
        """Execute command via vscode command server and wait for command to finish."""
        run_vscode_command(
            command,
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            wait_for_finish=True,
        )

    def vscode_get(
        command: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ) -> Any:
        """Execute command via vscode command server and return command output."""
        return run_vscode_command(
            command,
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            expect_response=True,
        )
