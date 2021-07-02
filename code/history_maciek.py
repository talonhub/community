import os
from dearpygui import core, simple
from talon import Module, actions, app, imgui, speech_system

# We keep command_history_size lines of history, but by default display only
# command_history_display of them.
mod = Module()
setting_command_history_size = mod.setting("command_history_size", int, default=50)
setting_command_history_display = mod.setting(
    "command_history_display", int, default=10
)

hist_more = False


def parse_phrase(word_list):
    return " ".join(word.split("\\")[0] for word in word_list)


# todo: dynamic rect?

import json
import pprint

import psutil


class HistoryView(object):
    def __init__(self) -> None:
        super().__init__()
        self.history = []
        # with simple.window("Example Window"):
        # core.add_text("Hello world")

    def on_phrase(self, j):
        # print("got", pprint.pprint(j))
        # to_display = ["audio_ms", "emit_ms", "compile_ms"]
        # print(j["_metadata"])
        # print(j.items()
        if "_metadata" in j.keys():
            to_dump = j["_metadata"]
            diagnostics = self.create_diagnostics()
            to_dump["diagnostics"] = diagnostics

            with open("/home/maciek/.talon_maciek/logs", mode="a") as f:
                f.write(json.dumps(to_dump))

                f.write("\n")
                f.write("---\n")

        try:
            val = parse_phrase(getattr(j["parsed"], "_unmapped", j["phrase"]))
        except:
            val = parse_phrase(j["phrase"])

        if val != "":
            self.history.append(val)
            self.history = self.history[-setting_command_history_size.get() :]

    def create_diagnostics(self):
        load1, load5, load15 = os.getloadavg()
        diagnostics = {}
        diagnostics["load1"] = load1
        diagnostics["load5"] = load5
        diagnostics["load15"] = load15
        diagnostics["swap_used"] = psutil.swap_memory().percent

        return diagnostics


history_view = HistoryView()


# def f():
#    core.start_dearpygui()
#

# import threading

# x = threading.Thread(target=f, args=())
# x.start()
# print(100 * "done")
speech_system.register("phrase", history_view.on_phrase)
# core.start_dearpy1gui()


@mod.action_class
class Actions:
    def history_maciek_toggle():
        """Toggles viewing the history"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def history_maciek_enable():
        """Enables the history"""
        gui.show()

    def history_maciek_disable():
        """Disables the history"""
        gui.hide()

    def history_maciek_clear():
        """Clear the history"""
        global history
        history = []

    def history_maciek_more():
        """Show more history"""
        global hist_more
        hist_more = True

    def history_maciek_less():
        """Show less history"""
        global hist_more
        hist_more = False
