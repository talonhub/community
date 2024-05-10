import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from tempfile import gettempdir
from typing import Any, Callable
from uuid import uuid4

from talon import actions


# The amount of time to wait for application to perform a command, in seconds
RPC_COMMAND_TIMEOUT_SECONDS = 3.0

# When doing exponential back off waiting for application to perform a command, how
# long to sleep the first time
MINIMUM_SLEEP_TIME_SECONDS = 0.0005

# How old a request file needs to be before we declare it stale and are willing
# to remove it
STALE_TIMEOUT_MS = 60_000


@dataclass
class Request:
    version = 1
    uuid: str
    wait_for_finish: bool
    return_command_output: bool
    payload: Any

    def to_dict(self):
        return {
            "version": self.version,
            "uuid": self.uuid,
            "waitForFinish": self.wait_for_finish,
            "returnCommandOutput": self.return_command_output,
            "payload": self.payload,
        }


def run_rpc_command(
    communication_dir_path: Path,
    trigger_execution: Callable[[], None],
    wait_for_finish: bool,
    return_command_output: bool,
    payload: Any,
):
    """Runs a command, using file based rpc

    Args:
        communication_dir_path (str): The path to the directory used for communication
        trigger_execution (Callable[[], None]): A function that triggers the application to execute the request
        wait_for_finish (bool, optional): Whether to wait for the command to finish before returning. Defaults to False.
        return_command_output (bool, optional): Whether to return the output of the command. Defaults to False.
        payload (Any): The payload/data to send to the application

    Raises:
        Exception: If there is an issue with the file-based communication, or
        application raises an exception

    Returns:
        Object: The response from the command, if requested.
    """

    request_path = communication_dir_path / "request.json"
    response_path = communication_dir_path / "response.json"

    # Generate uuid that will be mirrored back to us by command server for
    # sanity checking
    uuid = str(uuid4())

    request = Request(
        uuid=uuid,
        wait_for_finish=wait_for_finish,
        return_command_output=return_command_output,
        payload=payload,
    )

    # First, write the request to the request file, which makes us the sole
    # owner because all other processes will try to open it with 'x'
    write_request(request, request_path)

    # We clear the response file if it does exist, though it shouldn't
    if response_path.exists():
        print("WARNING: Found old response file")
        robust_unlink(response_path)

    # Then, perform keystroke telling application to execute the command in the
    # request file.  Because only the active application instance will accept
    # keypresses, we can be sure that the active application instance will be the
    # one to execute the command.
    trigger_execution()

    try:
        decoded_contents = read_json_with_timeout(response_path)
    finally:
        # NB: We remove response file first because we want to do this while we
        # still own the request file
        robust_unlink(response_path)
        robust_unlink(request_path)

    if decoded_contents["uuid"] != uuid:
        raise Exception("uuids did not match")

    for warning in decoded_contents["warnings"]:
        print(f"WARNING: {warning}")

    if decoded_contents["error"] is not None:
        raise Exception(decoded_contents["error"])

    actions.sleep("25ms")

    return decoded_contents["returnValue"]


def write_json_exclusive(path: Path, body: Any):
    """Writes jsonified object to file, failing if the file already exists

    Args:
        path (Path): The path of the file to write
        body (Any): The object to convert to json and write
    """
    with path.open("x") as out_file:
        out_file.write(json.dumps(body))


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
        request_file_exists = False
    except FileExistsError:
        request_file_exists = True

    if request_file_exists:
        handle_existing_request_file(path)
        write_json_exclusive(path, request.to_dict())


def handle_existing_request_file(path):
    stats = path.stat()

    modified_time_ms = stats.st_mtime_ns / 1e6
    current_time_ms = time.time() * 1e3
    time_difference_ms = abs(modified_time_ms - current_time_ms)

    if time_difference_ms < STALE_TIMEOUT_MS:
        raise Exception(
            "Found recent request file; another Talon process is probably running"
        )

    print("Removing stale request file")
    robust_unlink(path)


def get_communication_dir_path(dir_name) -> Path:
    """Returns directory that is used by command-server for communication

    Returns:
        Path: The path to the communication dir
    """
    suffix = ""

    # NB: We don't suffix on Windows, because the temp dir is user-specific
    # anyways
    if hasattr(os, "getuid"):
        suffix = f"-{os.getuid()}"

    return Path(gettempdir()) / f"{dir_name}{suffix}"


def robust_unlink(path: Path):
    """Unlink the given file if it exists, and if we're on windows and it is
    currently in use, just rename it

    Args:
        path (Path): The path to unlink
    """
    try:
        path.unlink(missing_ok=True)
    except OSError as e:
        if hasattr(e, "winerror") and e.winerror == 32:
            graveyard_dir = path.parent / "graveyard"
            graveyard_dir.mkdir(parents=True, exist_ok=True)
            graveyard_path = graveyard_dir / str(uuid4())
            print(
                f"WARNING: File {path} was in use when we tried to delete it; "
                f"moving to graveyard at path {graveyard_path}"
            )
            path.rename(graveyard_path)
        else:
            raise e


def read_json_with_timeout(path: Path) -> Any:
    """Repeatedly tries to read a json object from the given path, waiting
    until there is a trailing new line indicating that the write is complete

    Args:
        path (str): The path to read from

    Raises:
        Exception: If we timeout waiting for a response

    Returns:
        Any: The json-decoded contents of the file
    """
    timeout_time = time.perf_counter() + RPC_COMMAND_TIMEOUT_SECONDS
    sleep_time = MINIMUM_SLEEP_TIME_SECONDS
    while True:
        try:
            raw_text = path.read_text()

            if raw_text.endswith("\n"):
                break
        except FileNotFoundError:
            # If not found, keep waiting
            pass

        actions.sleep(sleep_time)

        time_left = timeout_time - time.perf_counter()

        if time_left < 0:
            raise Exception("Timed out waiting for response")

        # NB: We use minimum sleep time here to ensure that we don't spin with
        # small sleeps due to clock slip
        sleep_time = max(min(sleep_time * 2, time_left), MINIMUM_SLEEP_TIME_SECONDS)

    return json.loads(raw_text)
