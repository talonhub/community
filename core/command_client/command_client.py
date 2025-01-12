from pathlib import Path
from typing import Any

from talon import Context, Module, actions, speech_system

from .rpc_client.get_communication_dir_path import get_communication_dir_path

# Indicates whether a pre-phrase signal was emitted during the course of the
# current phrase
did_emit_pre_phrase_signal = False

mod = Module()
ctx = Context()
mac_ctx = Context()

ctx.matches = r"""
tag: user.command_client
"""
mac_ctx.matches = r"""
os: mac
tag: user.command_client
"""


class NotSet:
    def __repr__(self):
        return "<argument not set>"


def run_command(
    command_id: str,
    *args,
    wait_for_finish: bool = False,
    return_command_output: bool = False,
):
    """Runs a command, using command server if available

    Args:
        command_id (str): The ID of the command to run.
        args: The arguments to the command.
        wait_for_finish (bool, optional): Whether to wait for the command to finish before returning. Defaults to False.
        return_command_output (bool, optional): Whether to return the output of the command. Defaults to False.

    Raises:
        Exception: If there is an issue with the file-based communication, or
        application raises an exception

    Returns:
        Object: The response from the command, if requested.
    """
    # NB: This is a hack to work around the fact that talon doesn't support
    # variable argument lists
    args = [x for x in args if x is not NotSet]

    return actions.user.rpc_client_run_command(
        actions.user.command_server_directory(),
        actions.user.trigger_command_server_command_execution,
        command_id,
        args,
        wait_for_finish,
        return_command_output,
    )


@mod.action_class
class Actions:
    def run_rpc_command(
        command_id: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ):
        """Execute command via RPC."""
        run_command(
            command_id,
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
        )

    def run_rpc_command_and_wait(
        command_id: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ):
        """Execute command via application command server and wait for command to finish."""
        run_command(
            command_id,
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            wait_for_finish=True,
        )

    def run_rpc_command_get(
        command_id: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
        arg4: Any = NotSet,
        arg5: Any = NotSet,
    ) -> Any:
        """Execute command via application command server and return command output."""
        return run_command(
            command_id,
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            return_command_output=True,
        )

    def command_server_directory() -> str:
        """Return the directory of the command server"""

    def trigger_command_server_command_execution():
        """Issue keystroke to trigger command server to execute command that
        was written to the file.  For internal use only"""
        actions.key("ctrl-shift-f17")

    def emit_pre_phrase_signal() -> bool:
        """
        If in an application supporting the command client, returns True
        and touches a file to indicate that a phrase is beginning execution.
        Otherwise does nothing and returns False.
        """
        return False

    def did_emit_pre_phrase_signal() -> bool:
        """Indicates whether the pre-phrase signal was emitted at the start of this phrase"""
        # NB: This action is used by cursorless; please don't delete it :)
        return did_emit_pre_phrase_signal


@mac_ctx.action_class("user")
class MacUserActions:
    def trigger_command_server_command_execution():
        actions.key("cmd-shift-f17")


@ctx.action_class("user")
class UserActions:
    def emit_pre_phrase_signal():
        get_signal_path("prePhrase").touch()
        return True


class MissingCommunicationDir(Exception):
    pass


def get_signal_path(name: str) -> Path:
    """
    Get the path to a signal in the signal subdirectory.

    Args:
        name (str): The name of the signal

    Returns:
        Path: The signal path
    """
    dir_name = actions.user.command_server_directory()
    communication_dir_path = get_communication_dir_path(dir_name)

    if not communication_dir_path.exists():
        raise MissingCommunicationDir()

    signal_dir = communication_dir_path / "signals"
    signal_dir.mkdir(parents=True, exist_ok=True)

    return signal_dir / name


def pre_phrase(_: Any):
    try:
        global did_emit_pre_phrase_signal

        did_emit_pre_phrase_signal = actions.user.emit_pre_phrase_signal()
    except MissingCommunicationDir:
        pass


def post_phrase(_: Any):
    global did_emit_pre_phrase_signal
    did_emit_pre_phrase_signal = False


speech_system.register("pre:phrase", pre_phrase)
speech_system.register("post:phrase", post_phrase)
