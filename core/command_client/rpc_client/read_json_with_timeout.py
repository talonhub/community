import json
import time
from pathlib import Path
from typing import Any

from talon import Module, actions, settings

mod = Module()

mod.setting(
    "rpc_command_timeout_seconds",
    type=float,
    default=3.0,
    desc="The amount of time to wait for application to perform a command, in seconds",
)


# When doing exponential back off waiting for application to perform a command, how
# long to sleep the first time
MINIMUM_SLEEP_TIME_SECONDS = 0.0005


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
    timeout_time = time.perf_counter() + settings.get(
        "user.rpc_command_timeout_seconds"
    )
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
