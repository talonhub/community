from typing import Any, Callable
from uuid import uuid4

from talon import Module, actions

from .get_communication_dir_path import get_communication_dir_path
from .read_json_with_timeout import read_json_with_timeout
from .robust_unlink import robust_unlink
from .types import NoFileServerException, Request
from .write_request import write_request

mod = Module()


@mod.action_class
class Actions:
    def rpc_client_run_command(
        dir_name: str,
        trigger_command_execution: Callable,
        command_id: str,
        args: list[Any],
        wait_for_finish: bool = False,
        return_command_output: bool = False,
    ):
        """Runs a command, using command server if available

        Args:
            dir_name (str): The name of the directory to use for communication.
            trigger_command_execution (Callable): The function to call to trigger command execution.
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
        communication_dir_path = get_communication_dir_path(dir_name)

        if not communication_dir_path.exists():
            if args or return_command_output:
                raise Exception(
                    "Communication directory not found. Must use command-server extension for advanced commands"
                )
            raise NoFileServerException("Communication directory not found")

        request_path = communication_dir_path / "request.json"
        response_path = communication_dir_path / "response.json"

        # Generate uuid that will be mirrored back to us by command server for
        # sanity checking
        uuid = str(uuid4())

        request = Request(
            command_id=command_id,
            args=args,
            wait_for_finish=wait_for_finish,
            return_command_output=return_command_output,
            uuid=uuid,
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
        trigger_command_execution()

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
