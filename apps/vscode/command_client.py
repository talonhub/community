import requests
from typing import Any
from talon import Module
from pathlib import Path
from tempfile import gettempdir


mod = Module()


class NotSet:
    def __repr__(self):
        return "<argument not set>"


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
        # NB: This is a hack to work around the fact that talon doesn't support
        # variable argument lists
        args = list(
            filter(
                lambda x: x is not NotSet,
                [
                    arg1,
                    arg2,
                    arg3,
                    arg4,
                    arg5,
                ],
            )
        )

        port_file_path = Path(gettempdir()) / "vscode-port"
        port = port_file_path.read_text()

        response = requests.post(
            f"http://localhost:{port}/execute-command",
            json={
                "commandId": command,
                "args": args,
                "waitForReturnValue": False,
            },
            timeout=(0.05, 3.05),
        )
        response.raise_for_status()
