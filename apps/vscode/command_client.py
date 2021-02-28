from queue import Queue
import requests
from threading import Thread
from time import sleep
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


MAX_DELAY = 500


class QueueItemType(Enum):
    DIE = auto()
    COMMAND = auto()


@dataclass
class QueueItem:
    type: QueueItemType
    payload: Any = None


@dataclass
class CommandInfo:
    command: str
    args: List[Any]
    timestamp: datetime.datetime


class VSCodeCommandPipe:
    def __init__(self, queue: Queue):
        self.queue = queue
        self.output_fifo_path = Path("/tmp/vscode-command-pipe-in")
        self.input_fifo_path = Path("/tmp/vscode-command-pipe-out")
        self.mkfifo(self.output_fifo_path)
        self.mkfifo(self.input_fifo_path)

    def mkfifo(self, fifo_path):
        if not fifo_path.exists():
            mkfifo(fifo_path)
        elif not fifo_path.is_fifo():
            raise Exception(f"Path {fifo_path} exists but is not a fifo")

    def __call__(self):
        print("Starting vscode command pipe thread")
        while True:
            item = queue.get()
            if item.type == QueueItemType.DIE:
                print("Thread killed")
                break
            payload = item.payload
            print(f"Working on {item}")
            self.send(payload.command, payload.args, payload.timestamp)
            print(f"Finished {item}")
            # queue.task_done()

    def send(self, command, args, timestamp: datetime.datetime):
        with self.output_fifo_path.open("w") as out:
            out.write(
                json.dumps(
                    {
                        "commandId": command,
                        "args": args,
                        "expectResponse": False,
                        "timestamp": timestamp.isoformat(),
                    }
                )
            )

        with self.input_fifo_path.open("r") as input_fifo:
            response = input_fifo.read()
            print(response)


try:
    actions.user.kill_vscode_command_pipe_thread()
except KeyError:
    pass

queue = Queue()
vscode_command_pipe = VSCodeCommandPipe(queue)

# # turn-on the worker thread
# Thread(target=vscode_command_pipe, daemon=True).start()

# # send thirty task requests to the worker
# for item in range(30):
#     q.put(item)
# print('All task requests sent\n', end='')

# # block until all tasks are done
# q.join()
# print('All work completed')


@mod.action_class
class Actions:
    def vscode(command: str, args: Optional[List[Any]] = None):
        """Execute command via vscode command pipe."""
        if args is None:
            args = []

        # if not is_mac:
        #     actions.key("ctrl-shift-alt-p")
        # else:
        #     actions.key("cmd-shift-alt-p")

        with open("/tmp/vscode-host") as host_file:
            host = host_file.read()
        response = requests.post(
            f"http://{host}",
            json={
                "commandId": command,
                "args": args,
                "expectResponse": False,
                # "timestamp": timestamp.isoformat(),
            },
            timeout=(0.05, 3.05),
        )
        response.raise_for_status()
        print(response.text)
        # queue.join()

    def kill_vscode_command_pipe_thread():
        """Kill existing vscode command pipe thread"""
        queue.put(QueueItem(type=QueueItemType.DIE))