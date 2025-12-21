from typing import Union

from talon import Module, actions

from .command_server import send_request_and_wait

mod = Module()


def _target_to_array(target: dict) -> list[str]:
    """Convert a rango target into an array of hint strings"""
    if "items" in target:
        return [item["mark"]["value"] for item in target["items"]]
    else:
        return [target["mark"]["value"]]


# Legacy command v1
# This is here in case users have defined their own commands outside of
# rango-talon. To be marked as deprecated. 2024-11-11
@mod.action_class
class Actions:
    def rango_command_with_target(
        actionType: str,
        target: dict,
        arg: Union[str, float, None] = None,
    ):
        """Executes a Rango command with target"""
        target = _target_to_array(target)
        action = {"type": actionType, "target": target}

        if arg:
            action["arg"] = arg

        return send_request_and_wait(
            {"version": 1, "type": "request", "action": action}
        )

    def rango_command_without_target(
        actionType: str,
        arg: Union[str, float, None] = None,
        arg2: Union[str, None] = None,
        arg3: Union[bool, None] = None,
    ):
        """Executes a Rango command without a target"""
        action = {"type": actionType}
        if arg:
            action["arg"] = arg
        if arg2:
            action["arg2"] = arg2
        if arg3 is not None:
            action["arg3"] = arg3
        return send_request_and_wait(
            {"version": 1, "type": "request", "action": action}
        )
