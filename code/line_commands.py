import os
import os.path
import requests
import time
from pathlib import Path
from talon import ctrl, ui, Module, Context, actions, clip
import tempfile

mod = Module()

mod.tag(
    "line_commands",
    desc="Tag for enabling generic line navigation and selection commands",
)


@mod.action_class
class Actions:
    def select_until_line(verb: str, line: int):
        """Performs action on selection from current line to the specified line."""

    def select_range(line_start: int, line_end: int):
        """Performs action on selection from line line_start to line line_end"""
        actions.edit.jump_line(line_start)
        actions.edit.extend_line_end()

        number_of_lines = line_end - line_start
        for i in range(0, number_of_lines):
            actions.edit.extend_line_down()
        actions.edit.extend_line_end()

    def line_clone(line: int):
        """Clones specified line at current position"""

