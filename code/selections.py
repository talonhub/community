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
    "comment": [actions.user.ide_toggle_comment],
    "replace": [actions.edit.paste],
    "expand": [actions.user.ide_expand_region],
    "collapse": [actions.user.ide_collapse_region],
    "refactor": [actions.user.ide_refactor_in_line],
    "rename": [actions.user.ide_refactor_rename],
    "indent": [actions.edit.indent_more],
    "unindent": [actions.edit.indent_less],
}

movement_verbs_map = {
    "go": [],
}

ctx = Context()
mod = Module()

mod.list('selection_verbs', desc='Verbs for selecting in the editor')
mod.list('navigation_verbs', desc='Verbs for navigating lines in the editor')
mod.tag("line_commands", desc='Tag for enabling generic line navigation and selection commands')

@mod.capture
def selection_verbs(m) -> list:
    """Returns a list of verbs"""

@mod.capture
def navigation_verbs(m) -> list:
    """Returns a list of verbs"""

def perform_selection_action(verb: str):
    acts = select_verbs_map[verb]
    for act in acts:
        act()

def perfom_movement_action(verb: str):
    acts = select_verbs_map[verb]
    for act in acts:
        act()

@mod.action_class
class Actions:
    def go_to_line(line: int):
        """Goes to a line"""

    def select_whole_line(verb: str, line: int):
        """Selects entire line"""
        actions.user.go_to_line(line)
        actions.edit.extend_line_start()
        actions.edit.extend_line_end()
        perform_selection_action(verb)

    def select_current_line(verb: str):
        """Select current line"""
        actions.edit.line_start()
        actions.edit.extend_line_end()
        perform_selection_action(verb)

    def select_line(verb: str, line: int):
        """Performs action on selection of specified line"""
        actions.user.go_to_line(line)
        actions.edit.extend_line_end()
        perform_selection_action(verb)
    
    def select_until_line(verb: str, line: int):
        """Performs action on selection from current line to the specified line."""

    def select_range(verb: str, line_start: int, line_end: int):
        """Performs action on selection from line line_start to line line_end"""
        actions.user.go_to_line(line_start)
        actions.edit.extend_line_end()
        
        number_of_lines = line_end - line_start
        for i in range(0, number_of_lines):
            actions.edit.extend_line_down()
        actions.edit.extend_line_end()
        perform_selection_action(verb)

    def select_way_left(verb: str):
        """Performs action on selection from cursor to line start"""
        actions.edit.extend_line_start()
        perform_selection_action(verb)

    def select_way_right(verb: str):
        """Performs action on selection from cursor to line end"""
        actions.edit.extend_line_end()
        perform_selection_action(verb)

    def select_way_up(verb: str):
        """Performs action on selection from cursor to file start""" 
        actions.edit.extend_file_start()
        perform_selection_action(verb)

    def select_way_down(verb: str):
        """Performs action on selection from cursor to file end""" 
        actions.edit.extend_file_end()
        perform_selection_action(verb)

    def select_camel_left(verb: str):
        """Perform action on camel-based selection to the left."""

    def select_camel_right(verb: str):
        """Perform action on camel-based selection to the right"""

    def select_all(verb: str):
        """Perform action on entire file"""
        actions.edit.extend_select_all()
        perform_selection_action(verb)

    def select_left(verb: str):
        """Perform action on selection to the left"""
        actions.edit.extend_left()
        perform_selection_action(verb)

    def select_right(verb: str):
        """Perform action on selection to the right"""
        actions.edit.extend_right()
        perform_selection_action(verb)

    def select_up(verb: str):
        """Perform action on upward selection """
        actions.edit.extend_up()
        perform_selection_action(verb)

    def select_down(verb: str):
        """Perform action on downward selection"""
        actions.edit.extend_down()
        perform_selection_action(verb)    

    def select_word_left(verb: str):
        """Perform action on left word selection"""
        actions.edit.extend_word_left()
        perform_selection_action(verb)    

    def select_word_right(verb: str):
        """Perform action on right word selection"""
        actions.edit.extend_word_left()
        perform_selection_action(verb) 

    def move_camel_left(verb: str):
        """Moves and performs action on camel left"""

    def move_camel_right(verb: str):
        """Moves and performs action on camel left"""   

@ctx.capture(rule='{self.selection_verbs}')
def selection_verbs(m):
    return m.selection_verbs

@ctx.capture(rule='{self.navigation_verbs}')
def navigation_verbs(m):
    return m.navigation_verbs

ctx.lists['self.selection_verbs'] = select_verbs_map.keys()
ctx.lists['self.navigation_verbs'] = movement_verbs_map.keys()
