import requests
import time
import json
from typing import Any
from talon import Module, actions, app
from pathlib import Path
from tempfile import gettempdir

is_mac = app.platform == "mac"

mod = Module()


class NotSet:
    def __repr__(self):
        return "<argument not set>"


def run_vscode_command(
    command: str,
    *args: str,
    wait_for_finish: bool = False,
    expect_response: bool = False,
    decode_json_arguments: bool = False,
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
    if decode_json_arguments:
        args = [json.loads(arg) for arg in args]

    port_file_path = Path(gettempdir()) / "vscode-port"
    original_contents = port_file_path.read_text()

    # Issue command to VSCode telling it to update the port file.  Because only
    # the active VSCode instance will accept keypresses, we can be sure that
    # the active VSCode instance will be the one to write the port.
    if is_mac:
        actions.key("cmd-shift-alt-p")
    else:
        actions.key("ctrl-shift-alt-p")

    # Wait for the VSCode instance to update the port file.  This generally
    # happens within the first millisecond, but we give it 3 seconds just in
    # case.
    start_time = time.monotonic()
    new_contents = port_file_path.read_text()
    sleep_time = 0.0005
    while True:
        if new_contents != original_contents:
            try:
                decoded_contents = json.loads(new_contents)
                # If we're successful, we break out of the loop
                break
            except ValueError:
                # If we're not successful, we keep waiting; we assume it was a
                # partial write from VSCode
                pass
        time.sleep(sleep_time)
        sleep_time *= 2
        if time.monotonic() - start_time > 3.0:
            raise Exception("Timed out waiting for VSCode to update port file")
        new_contents = port_file_path.read_text()

    port = decoded_contents["port"]

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

    def vscode_json_and_wait(
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
            decode_json_arguments=True,
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
