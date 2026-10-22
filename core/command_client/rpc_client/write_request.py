import json
import time
from pathlib import Path
from typing import Any

from .robust_unlink import robust_unlink
from .types import Request

# How old a request file needs to be before we declare it stale and are willing
# to remove it
STALE_TIMEOUT_MS = 60_000


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


def write_json_exclusive(path: Path, body: Any):
    """Writes jsonified object to file, failing if the file already exists

    Args:
        path (Path): The path of the file to write
        body (Any): The object to convert to json and write
    """
    with path.open("x") as out_file:
        out_file.write(json.dumps(body))


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
