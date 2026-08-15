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
            "commandId": self.command_id,
            "args": self.args,
            "waitForFinish": self.wait_for_finish,
            "returnCommandOutput": self.return_command_output,
            "uuid": self.uuid,
        }


class NoFileServerException(Exception):
    pass
