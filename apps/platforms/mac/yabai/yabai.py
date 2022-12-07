import os
from typing import List

from talon import Context, Module, actions

mod = Module()
ctx = Context()


mod.list("yabai_dir", desc="Cardinal directions for yabai")
ctx.lists["user.yabai_dir"] = {
    "north": "north",
    "south": "south",
    "east": "east",
    "west": "west",
    "up": "north",
    "down": "south",
    "left": "west",
    "right": "east",
}

mod.list("yabai_selector", desc="Window/space/stack selectors for yabai")
ctx.lists["user.yabai_selector"] = {
    "prev": "prev",
    "next": "next",
    "first": "first",
    "last": "last",
    "recent": "recent",
    "mouse": "mouse",
    "largest": "largest",
    "smallest": "smallest",
    "sibling": "sibling",
    "first nephew": "first_nephew",
    "second nephew": "second_nephew",
    "uncle": "uncle",
    "first cousin": "first_cousin",
    "second cousin": "second_cousin",
    **ctx.lists["user.yabai_dir"],
}


YABAI_PATH = "/opt/homebrew/bin/yabai"


@mod.action_class
class Actions:
    def yabai(command: str):
        """Send a message to yabai"""
        os.system(f"{YABAI_PATH} -m {command}")

    def yabai_win_resize(arrow_key: str, amount: int):
        """Adjust window size in a given direction"""
        if arrow_key == "up":
            m = f"window --resize top:0:{-amount}"
        elif arrow_key == "down":
            m = f"window --resize bottom:0:{amount}"
        elif arrow_key == "left":
            m = f"window --resize left:{-amount}:0"
        else:
            m = f"window --resize right:{amount}:0"

        actions.user.yabai(m)
