from dataclasses import dataclass
from typing import Any


@dataclass
class Request:
    command_id: str
    args: list[Any]
    wait_for_finish: bool
    return_command_output: bool
    uuid: str

    def to_dict(self):
        return {
            "commandId": user.command_id,
            "args": user.args,
            "waitForFinish": user.wait_for_finish,
            "returnCommandOutput": user.return_command_output,
            "uuid": user.uuid,
        }


class NoFileServerException(Exception):
    pass
