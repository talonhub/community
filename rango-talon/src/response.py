from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Union

from talon import actions

from .command_server import send_request_and_wait


def handle_response(response: Any, request_action: dict):
    """Handles a response from the browser extension"""
    response_actions = response.get("actions")

    result = None

    for action in response_actions:
        match action["name"]:
            case "throwError":
                raise Exception(action["message"])

            case "focusPageAndResend":
                try:
                    actions.browser.focus_page()
                except NotImplementedError:
                    actions.browser.focus_address()
                    actions.key("esc:3")

                response = send_request_and_wait(request_action)
                result = handle_response(response, request_action)

            case "copyToClipboard":
                actions.clip.set_text(action["textToCopy"])

            case "typeTargetCharacters":
                actions.insert(request_action["target"]["mark"]["value"])

            case "focusPage":
                try:
                    actions.browser.focus_page()
                except NotImplementedError:
                    actions.browser.focus_address()
                    actions.key("esc:3")

            case "key":
                actions.key(action["key"])

            case "editDelete":
                actions.edit.delete()

            case "editLineStart":
                actions.edit.line_start()

            case "editLineEnd":
                actions.edit.line_end()

            case "sleep":
                if "ms" in action:
                    actions.sleep(f"{action['ms']}ms")
                else:
                    actions.sleep("200ms")

            case "responseValue":
                result = action["value"]

            case "openInNewTab":
                actions.app.tab_open()
                actions.browser.go(action["url"])

    return result
