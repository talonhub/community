from queue import SimpleQueue
from threading import Thread
from typing import Any, List, Optional
from talon import Context, actions, ui, Module, app, clip
import datetime
from pathlib import Path
from os import mkfifo
import json

# from queue import queue

mod = Module()
is_mac = app.platform == "mac"

from enum import Enum, auto
from dataclasses import dataclass


class QueueItemType(Enum):
    DIE = auto()
    COMMAND = auto()


@dataclass
class QueueItem:
    type: QueueItemType
    payload: Any = None


class VSCodeCommandPipe:
    def __init__(self, queue: SimpleQueue):
        self.mkfifo()
        self.queue = queue

    def mkfifo(self):
        self.fifo_path = Path("/tmp/vscode-command-pipe-in")

        if not self.fifo_path.exists():
            mkfifo(self.fifo_path)
        elif not self.fifo_path.is_fifo():
            raise Exception(f"Path {self.fifo_path} exists but is not a fifo")

    def __call__(self):
        print("Starting vscode command pipe thread")
        while True:
            item = queue.get()
            if item.type == QueueItemType.DIE:
                print("Thread killed")
                break
            payload = item.payload
            print(f"Working on {item}")
            self.send(*payload)
            print(f"Finished {item}")

    def send(self, command, *args):
        with self.fifo_path.open("w") as out:
            out.write(
                json.dumps(
                    {
                        "commandId": command,
                        "args": args,
                        "expectResponse": False,
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                    }
                )
            )


try:
    actions.user.kill_vscode_command_pipe_thread()
except KeyError:
    pass

queue = SimpleQueue()
vscode_command_pipe = VSCodeCommandPipe(queue)

# # turn-on the worker thread
Thread(target=vscode_command_pipe, daemon=True).start()

# # send thirty task requests to the worker
# for item in range(30):
#     q.put(item)
# print('All task requests sent\n', end='')

# # block until all tasks are done
# q.join()
# print('All work completed')


@mod.action_class
class Actions:
    def vscode_via_command_pipe(command: str, args: Optional[List[Any]] = None):
        """Execute command via vscode command pipe."""
        if args is None:
            args = []

        if not is_mac:
            actions.key("ctrl-shift-alt-p")
        else:
            actions.key("cmd-shift-alt-p")

        queue.put(QueueItem(type=QueueItemType.COMMAND, payload=[command, *args]))

    def kill_vscode_command_pipe_thread():
        """Kill existing vscode command pipe thread"""
        queue.put(QueueItem(type=QueueItemType.DIE))