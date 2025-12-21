from .command_server import send_request_and_wait
from .response import handle_response
from .versions import COMMAND_VERSION


def run_targeted_command(action_name: str, target: dict, **kwargs):
    """Sends a targeted command to the browser extension"""
    action = {"name": action_name, "target": target, **kwargs}
    command = {"version": COMMAND_VERSION, "type": "request", "action": action}
    response = send_request_and_wait(command)
    return handle_response(response, action)


def run_simple_command(action_name: str, **kwargs):
    """Sends a command without a target to the browser extension"""
    action = {"name": action_name, **kwargs}
    command = {"version": COMMAND_VERSION, "type": "request", "action": action}
    response = send_request_and_wait(command)
    return handle_response(response, action)
