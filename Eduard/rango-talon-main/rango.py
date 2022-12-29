from talon import Module, Context, actions, clip, settings, app
import json
import time
from typing import Any, Union

mod = Module()
ctx = Context()
ctx.matches = r"""
tag: browser
"""

mod.tag(
    "rango_direct_clicking",
    desc="Commands for direct clicking with the extension rango",
)
ctx.tags = ["user.rango_direct_clicking"]

rango_start_with_direct_clicking = mod.setting(
    "rango_start_with_direct_clicking",
    type=bool,
    default=True,
    desc="Rango direct clicking mode setting",
)


def update_clicking_mode(setting_value):
    if setting_value == 1:
        ctx.tags = ["user.rango_direct_clicking"]
    else:
        ctx.tags = []


settings.register("user.rango_start_with_direct_clicking", update_clicking_mode)

mod.list("rango_hint_styles", desc="list of Rango hint styles")
mod.list("rango_hint_weights", desc="list of Rango hint weights")
mod.list("rango_hints_toggle_levels", desc="list of Rango hints toggle levels")
mod.list(
    "rango_page_location_property",
    desc="list of properties to be found in window.location",
)

hint_styles = ["boxed", "subtle"]
ctx.lists["user.rango_hint_styles"] = {k: k for k in hint_styles}
hint_weights = ["bold", "normal", "auto"]
ctx.lists["user.rango_hint_weights"] = {k: k for k in hint_weights}
toggle_levels = ["everywhere", "tab", "host", "page", "now"]
ctx.lists["user.rango_hints_toggle_levels"] = {k: k for k in toggle_levels}
ctx.lists["user.rango_page_location_property"] = {
    "address": "href",
    "host name": "hostname",
    "host": "host",
    "origin": "origin",
    "path": "pathname",
    "port": "port",
    "protocol": "protocol",
}


@mod.capture(rule="<user.letter> | <user.letter> <user.letter>")
def rango_hint(m) -> str:
    return "".join(m.letter_list)


@mod.capture(rule="<user.rango_hint> | <user.rango_hint> (and <user.rango_hint>)+")
def rango_hints(m) -> list:
    return m.rango_hint_list


@mod.capture(rule="<user.rango_hints>")
def rango_target(m) -> Union[str, list[str]]:
    if len(m.rango_hints) == 1:
        return m.rango_hints[0]
    else:
        return m.rango_hints


RANGO_COMMAND_TIMEOUT_SECONDS = 3.0
MINIMUM_SLEEP_TIME_SECONDS = 0.0005


def read_json_response_with_timeout() -> Any:
    """Repeatedly tries to read a json object from the clipboard, waiting
    until the message type is "response"

    Raises:
        Exception: If we timeout waiting for a response

    Returns:
        Any: The json-decoded contents of the file
    """
    timeout_time = time.perf_counter() + RANGO_COMMAND_TIMEOUT_SECONDS
    sleep_time = MINIMUM_SLEEP_TIME_SECONDS
    message = None
    initial_raw_text = clip.text()
    while True:
        raw_text = clip.text()
        try:
            message = json.loads(raw_text)
        # We make sure the message is valid JSON. For example, if a click command
        # results in something being copied to the clipboard and we check the clipboard
        # before Rango has time to copy the response to the clipboard.
        except ValueError as error:
            if initial_raw_text != raw_text:
                continue
            else:
                # Sanity check to make sure the initial request was valid JSON
                raise ValueError("The request message wasn't valid JSON")

        if message["type"] == "response":
            break

        actions.sleep(sleep_time)

        time_left = timeout_time - time.perf_counter()

        if time_left < 0:
            raise Exception("Timed out waiting for response")

        # NB: We use minimum sleep time here to ensure that we don't spin with
        # small sleeps due to clock slip
        sleep_time = max(min(sleep_time * 2, time_left), MINIMUM_SLEEP_TIME_SECONDS)

    return message


def send_request_and_wait_for_response(action: dict):
    message = {"version": 1, "type": "request", "action": action}
    json_message = json.dumps(message)
    response = None
    with clip.revert():
        clip.set_text(json_message)
        if app.platform == "mac":
            actions.key("ctrl-shift-3")
        else:
            actions.key("ctrl-shift-insert")
        response = read_json_response_with_timeout()

    if response["action"]["type"] == "copyToClipboard":
        actions.clip.set_text(response["action"]["textToCopy"])

    if response["action"]["type"] == "noHintFound":
        actions.insert(action["target"])


@mod.action_class
class Actions:
    def rango_command_with_target(
        actionType: str,
        target: Union[str, list[str]],
        arg: Union[str, float, None] = None,
    ):
        """Executes a Rango command"""

    def rango_command_without_target(
        actionType: str, arg: Union[str, float, None] = None
    ):
        """Executes a Rango command without a target"""

    def rango_enable_direct_clicking():
        """Enables rango direct mode so that the user doesn't have to say 'click' before the hint letters"""

    def rango_disable_direct_clicking():
        """Disables rango direct mode"""


@ctx.action_class("user")
class UserActions:
    def rango_command_with_target(
        actionType: str,
        target: Union[str, list[str]],
        arg: Union[str, float, None] = None,
    ):
        action = {"type": actionType, "target": target}
        if arg:
            action["arg"] = arg
        send_request_and_wait_for_response(action)

    def rango_command_without_target(
        actionType: str, arg: Union[str, float, None] = None
    ):

        action = {"type": actionType}
        if arg:
            action["arg"] = arg
        send_request_and_wait_for_response(action)

    def rango_enable_direct_clicking():
        ctx.tags = ["user.rango_direct_clicking"]

    def rango_disable_direct_clicking():
        ctx.tags = []
