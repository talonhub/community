import os
import os.path
import requests
import time
from pathlib import Path
from talon import ctrl, ui, Module, Context, actions, clip
import tempfile

select_verbs_map = {
    "select": [],
    "copy": [actions.edit.copy],
    "cut": [actions.edit.cut],
    "clear": [actions.edit.delete],
    "comment": [actions.code.toggle_comment],
    "replace": [actions.edit.paste],
    # TODO: figure these out
    # "expand": [actions.user.ide_expand_region],
    # "collapse": [actions.user.ide_collapse_region],
    # "refactor": [actions.user.ide_refactor_in_line],
    # "rename": [actions.user.ide_refactor_rename],
    "indent": [actions.edit.indent_more],
    "unindent": [actions.edit.indent_less],
    "drag up": [actions.edit.line_swap_up],
    "drag down": [actions.edit.line_swap_down],
}

movement_verbs_map = {
    "go": [],
    "paste": [actions.edit.paste],
}

ctx = Context()
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
        # actions.user.perform_selection_action(verb)

    def line_clone(line: int):
        """Clones specified line at current position"""

