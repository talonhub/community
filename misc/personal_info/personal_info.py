import json
import os
import sys
from typing import Set

from talon import Context, Module, actions, fs, imgui, settings, ui

mod = Module()
mod.mode("personal_info")
mod.setting(
    "personal_info_auto_select",
    type=int,
    default=1,
    desc="Auto select specified entry in json list, or none if 0",
)
mod.list("personal_info", desc="List of personal info populated by json file")
ctx = Context()


@mod.capture
def personal_info(m) -> list:
    """Returns a personal_info name"""


@ctx.capture(rule="{user.personal_info}")
def personal_info(m):
    return m.personal_info


# ctx.matches = r"""
# mode: command
# """

main_screen = ui.main_screen()

personal_info_list = []


def close_personal_info():
    gui.hide()
    actions.mode.disable("user.personal_info")


@imgui.open(y=0, x=main_screen.width / 2.6, software=False)
def gui(gui: imgui.GUI):
    global personal_info_list
    gui.text("Select an entry")
    gui.line()
    index = 1
    for word in personal_info_list:
        gui.text("Pick {}: {} ".format(index, word))
        index = index + 1

    if gui.button("Hide"):
        close_personal_info()


class PersonalInfo:
    db = None
    command_key_map = {}

    def __init__(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        self.personal_info_file = os.path.join(cwd, "personal_info.json")
        self.update_commands()
        fs.watch(self.personal_info_file, self.__on_fs_change)

    def __on_fs_change(self, name, flags):
        print("updating personal info commands")
        self.update_commands()

    def update_commands(self):
        with open(self.personal_info_file, "r") as f:
            self.db = json.loads(f.read())
            for key in self.db:
                self.command_key_map[" ".join(key.split("-"))] = key
        global ctx
        ctx.lists["user.personal_info"] = self.command_key_map


pi = PersonalInfo()


def raise_personal_info():
    actions.mode.enable("user.personal_info")
    gui.freeze()


@mod.action_class
class Actions:
    def personal_info_hide():
        """Hides the personal_info display"""
        close_personal_info()

    def personal_info(record: str):
        """Insert some info from the personal info database"""
        global pi
        global personal_info_list
        record_data = pi.db[record]
        if type(record_data) == list:
            if len(record_data) > 1:

                auto_index = settings.get("user.personal_info_auto_select")
                personal_info_list = record_data
                if auto_index <= len(record_data):
                    record_data = record_data[auto_index]
                else:
                    raise_personal_info()
            else:
                record_data = record_data[0]
        actions.insert(f"{record_data}")

    def personal_info_by_id(record: str, index: int):
        """Insert some info from the personal info database"""
        global pi
        global personal_info_list
        record_data = pi.db[record]
        if type(record_data) == list:
            if index - 1 > len(record_data):
                index = 0
            record_data = record_data[index - 1]
            actions.insert(f"{record_data}")
        else:
            actions.insert(f"{record_data}")

    def personal_info_select(number: int):
        """selects the personal_info by number"""
        if number <= len(personal_info_list) and number > 0:
            return personal_info_list[number - 1]

        error = "personal_info.py index {} is out of range (1-{})".format(
            number, len(personal_info_list)
        )
        app.notify(error)
        raise error
