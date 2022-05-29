import concurrent.futures
import json
import os
import pprint
from pathlib import Path
import asyncio
import time
from nats.aio.client import Client as NATS
from pynats import NATSClient

from talon import Module, actions, app, imgui, speech_system

# We keep command_history_size lines of history, but by default display only
# command_history_display of them.
mod = Module()
setting_command_history_size = mod.setting("command_history_size", int, default=50)
# setting_comm, and_history_display = mod.setting(
#     "command_history_display", int, default=10
# )


def parse_phrase(word_list):
    return " ".join(word.split("\\")[0] for word in word_list)


# This is really  broken,  I keep getting the broken pipe errors from nats:
# 6: ------------------------------------------------# cron thread
# 5:                      talon/scripting/rctx.py:233| # 'phrase' user.knausj_talon.code.history_maciek:on_phrase()
# 4:     user/knausj_talon/code/history_maciek.py:52 | self.send_message(to_dump)
# 3:     user/knausj_talon/code/history_maciek.py:34 | self.client.publish(self.channel_name,..
# 2: lib/python3.9/site-packages/pynats/client.py:273| self._send(PUB_OP, subject, reply, len..
# 1: lib/python3.9/site-packages/pynats/client.py:325| self._socket.sendall(_SPC_.join(self._encode(p) for p in parts) + _CRLF_)
# BrokenPipeError: [Errno 32] Broken pipe


# def publish_with_retry(client, *args, **kwargs):
#     while True:
#         try:
#             client.publish(*args, **kwargs)
#             break
#         except BrokenPipeError as e:
#             print(100 * "=")
#             print("reconnecting")
#             client.reconnect()
#             time.sleep(0.1)


class HistoryLogger(object):
    def __init__(self) -> None:
        super().__init__()
        self.history = []
        self.channel_name = "talon.history"
        # self.executor = concurrent.futures.ProcessPoolExecutor()

        # self.client.connect()

    def send_message(self, msg):
        client = NATSClient()
        client.connect()
        client.publish(self.channel_name, payload=json.dumps(msg))
        # publish_with_retry(client, self.channel_name, payload=json.dumps(msg))
        client.close()

    def send_message_with_retry(self, msg, retries=3):
        print("executing in another process")
        print(f"PID = {os.getpid()}")
        for i in range(retries):
            try:
                self.send_message(msg)
            except BrokenPipeError as e:
                # TODO(maciek): I have forgotten that I can sleep here because this will increase talon latency.
                time.sleep(0.2)
                print(100 * "=")
                print("reconnecting")
            else:
                print("success!")
                break

    def on_phrase(self, j):
        print("type of j", type(j))
        print("j", j)
        print(j.keys())
        if "_metadata" in j.keys():
            print(j["samples"])
            # print(help(j["samples"]))
            to_dump = j["_metadata"]
            # print(to_dump)
            to_print = ["audio_ms", "emit_ms", "compile_ms", "decode_ms", "total_ms"]
            for name in to_print:
                print(f"{name} =  {to_dump[name]}")
            # diagnostics = create_diagnostics()
            # to_dump["diagnostics"] = diagnostics
            # raise RuntimeError
            path = str(Path.home() / ".talon_maciek/logs")
            # flac_filename=
            # flac_path =Path.home() / f".talon_maciek/{filename}"

            print(f"path =  {path}")
            to_dump["samples"] = j["samples"]
            # self.executor.submit(self.send_message_with_retry, to_dump)
            # self.send_message_with_retry(to_dump)

            with open(path, mode="a") as f:
                f.write(json.dumps(to_dump))

                f.write("\n")
                f.write("---\n")

        try:
            val = parse_phrase(getattr(j["parsed"], "_unmapped", j["phrase"]))
        except:
            val = parse_phrase(j["phrase"])
        print(100 * "=")

        print(type(val))


history_logger = HistoryLogger()
speech_system.register("phrase", history_logger.on_phrase)
