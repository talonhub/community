import getpass
from dataclasses import dataclass
import json
import time
from pathlib import Path
from tempfile import gettempdir
from typing import Any, List
from uuid import uuid4

from talon import Module, actions, Context


STALE_TIMEOUT_MS = 10_000

mod = Module()

ctx = Context()
mac_ctx = Context()

ctx.matches = r"""
app: vscode
"""
mac_ctx.matches = r"""
os: mac
app: vscode
"""


class NotSet:
    def __repr__(self):
        return "<argument not set>"


def run_vscode_command_by_command_palette(command_id: str):
    """Execute command via command palette. Preserves the clipboard."""
    actions.user.command_palette()
    actions.user.paste(command_id)
    actions.key("enter")


def write_json_exclusive(path: Path, body: Any):
    """Writes jsonified object to file, failing if the file already exists

    Args:
        path (Path): The path of the file to write
        body (Any): The object to convert to json and write
    """
    with path.open("x") as out_file:
        out_file.write(json.dumps(body))


@dataclass
class Request:
    command_id: str
    args: List[Any]
    wait_for_finish: bool
    return_command_output: bool
    uuid: str

    def to_dict(self):
        return {
            "commandId": self.command_id,
            "args": self.args,
            "waitForFinish": self.wait_for_finish,
            "returnCommandOutput": self.return_command_output,
            "uuid": self.uuid,
        }


def write_request(request: Request, path: Path):
    """Converts the given request to json and writes it to the file, failing if
    the file already exists unless it is stale in which case it replaces it

    Args:
        request (Request): The request to serialize
        path (Path): The path to write to

    Raises:
        Exception: If another process has an active request file
    """
    try:
        write_json_exclusive(path, request.to_dict())
    except FileExistsError:
        stats = path.stat()

        modified_time_ms = stats.st_mtime_ns / 1e6
        current_time_ms = time.time() * 1e3

        if abs(modified_time_ms - current_time_ms) < STALE_TIMEOUT_MS:
            raise Exception("Another process has an active request file")
        else:
            print("Removing stale request file")
            path.unlink()
            write_json_exclusive(path, request.to_dict())


def run_vscode_command(
    command_id: str,
    *args: str,
    wait_for_finish: bool = False,
    return_command_output: bool = False,
    decode_json_arguments: bool = False,
):
    """Runs a VSCode command, using command server if available

    Args:
        command (str): The ID of the VSCode command to run
        wait_for_finish (bool, optional): Whether to wait for the command to finish before returning. Defaults to False.
        return_command_output (bool, optional): Whether to return the output of the command. Defaults to False.
        decode_json_arguments (bool, optional): Whether to decode JSON arguments. Defaults to False.

    Raises:
        Exception: If there is an issue with the file-based communication

    Returns:
        Object: The response from the command, if requested.
    """
    # NB: This is a hack to work around the fact that talon doesn't support
    # variable argument lists
    args = [x for x in args if x is not NotSet]

    if decode_json_arguments:
        args = [json.loads(arg) for arg in args]

    username = getpass.getuser()

    communication_dir_path = Path(gettempdir()) / f"vscode-command-server-{username}"

    if not communication_dir_path.exists():
        if args or return_command_output or decode_json_arguments:
            raise Exception("Must use command-server extension for advanced commands")
        print("Port file not found; using command palette")
        run_vscode_command_by_command_palette(command_id)
        return

    request_path = communication_dir_path / "request.json"
    response_path = communication_dir_path / "response.json"

    uuid = str(uuid4())

    unlink_if_exists(response_path)

    request = Request(
        command_id=command_id,
        args=args,
        wait_for_finish=wait_for_finish,
        return_command_output=return_command_output,
        uuid=uuid,
    )

    write_request(
        request,
        request_path,
    )

    # Issue command to VSCode telling it to update the port file.  Because only
    # the active VSCode instance will accept keypresses, we can be sure that
    # the active VSCode instance will be the one to write the port.
    actions.user.trigger_command_server_command_execution()

    try:
        decoded_contents = read_json_with_timeout(response_path)
    finally:
        unlink_if_exists(request_path)
        unlink_if_exists(response_path)

    if decoded_contents["uuid"] != uuid:
        raise Exception("uuids did not match")

    if decoded_contents["error"] is not None:
        raise Exception(decoded_contents["error"])

    actions.sleep("25ms")

    return decoded_contents["returnValue"]


def unlink_if_exists(path):
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def read_json_with_timeout(path: str) -> Any:
    """Repeatedly tries to read a json object from the given path, waiting until there is a trailing new line indicating that the write is complete

    Args:
        path (str): The path to write to

    Raises:
        Exception: If we timeout waiting for a response

    Returns:
        Any: The json-decoded contents of the file
    """
    start_time = time.perf_counter()
    sleep_time = 0.0005
    while True:
        try:
            raw_text = path.read_text()

            if raw_text.endswith("\n"):
                break
        except FileNotFoundError:
            # If not found, keep waiting
            pass

        actions.sleep(sleep_time)
        sleep_time *= 2
        if time.perf_counter() - start_time > 3.0:
            raise Exception("Timed out waiting for response")

    return json.loads(raw_text)


@mod.action_class
class Actions:
    def vscode(command_id: str):
        """Execute command via vscode command server, if available."""
        run_vscode_command(command_id)

    def trigger_command_server_command_execution():
        """Issue keystroke to trigger command server to execute command that was written to the file."""
        actions.key("ctrl-shift-alt-p")

    def vscode_and_wait(command_id: str):
        """Execute command via vscode command server, if available, and wait for command to finish."""
        run_vscode_command(command_id, wait_for_finish=True)

    def vscode_with_plugin(
        command_id: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ):
        """Execute command via vscode command server."""
        run_vscode_command(
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
        run_vscode_command(
            command_id,
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            wait_for_finish=True,
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
        return run_vscode_command(
            command_id,
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            return_command_output=True,
        )


@mac_ctx.action_class("user")
class MacUserActions:
    def trigger_command_server_command_execution():
        actions.key("cmd-shift-alt-p")
