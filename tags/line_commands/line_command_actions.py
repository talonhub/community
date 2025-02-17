from dataclasses import dataclass
from typing import Callable, Union
from talon import actions, Module, settings
from ...core.edit.edit_command_actions import EditAction

mod = Module()
mod.list("line_action", desc="Actions for lines")

@dataclass
class LineAction:
    """ "Simple" actions are actions that don't require any arguments, only a type (select, copy, delete, etc.)"""

    type: str

    def __str__(self):
        return self.type


@mod.capture(rule="{user.line_action}")
def line_action_simple(m) -> LineAction:
    return LineAction(m.line_action)

@mod.capture(rule="<user.edit_action> | <user.line_action_simple>")
def line_action(m)-> Union[LineAction, EditAction]: 
    return m[0]

def execute_lines_command(start: int, end: int, action: Union[EditAction, LineAction]):
    selection_delay = f"{settings.get('user.edit_command_line_selection_delay')}ms"
    actions.sleep(selection_delay)
    match action.type:
        case "select":
            actions.user.select_range(start, end)
        case "goAfter":
            actions.edit.jump_line(end)
            actions.edit.line_end()
        case "goBefore":
            actions.edit.jump_line(end)
        case "copyToClipboard":
            actions.user.select_range(start, end)
            actions.edit.copy()
        case "cutToClipboard":
            actions.user.select_range(start, end)
            actions.edit.cut()
        case "pasteFromClipboard":
            actions.user.select_range(start, end)
            actions.edit.paste()
        case "delete":
            actions.user.select_range(start, end)
            actions.edit.delete()
        case "comment":
            actions.user.select_range(start, end)
            actions.code.toggle_comment()
        case "indentMore":
            actions.user.select_range(start, end)
            actions.edit.indent_more() 
        case "indentLess":
            actions.user.select_range(start, end)
            actions.edit.indent_less() 
        case "swapDown":
            actions.user.select_range(start, end)
            actions.edit.line_swap_down() 
        case "swapUp":
            actions.user.select_range(start, end)
            actions.edit.line_swap_up() 
        case _:
            print(f"{action} not supported by line_command_actions")

@mod.action_class
class Actions:
    def lines_command(start: int, end: int, action: EditAction):
        """Perform edit command"""
        execute_lines_command(start, end, action)
    