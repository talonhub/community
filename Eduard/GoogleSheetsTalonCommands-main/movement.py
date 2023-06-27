from talon import Module, actions
from .clipboard import *

module = Module()

@module.capture(rule = '<user.letter>+ <number>')
def google_sheets_cell_location(m) -> str:
    '''A google sheets cell location'''
    location: str = ''
    for element in m:
        location += str(element)
    return location

@module.capture(rule = '<user.letter>+')
def google_sheets_cell_column(m) -> str:
    '''A google sheets column'''
    column: str = ''
    for letter in m:
        column += letter.upper()
    return column

@module.action_class
class Actions:
    def google_sheets_toggle_movement_tool():
        '''Activates the google sheets movement tool'''
        actions.key('ctrl-j')
    
    def google_sheets_go_to_cell(cell_location: str):
        '''Moves to the specified cell assuming that the movement tool is not currently active'''
        actions.user.google_sheets_toggle_movement_tool()
        actions.insert(cell_location)
        actions.key('enter')

    def google_sheets_go_to_row(number: int):
        '''Moves to the specified row'''
        actions.user.google_sheets_toggle_movement_tool()
        current_cell: CellLocation = CellLocation(get_selected_text_using_clipboard())
        current_column: str = current_cell.get_column()
        actions.insert(current_column + str(number))
        actions.key('enter')
    
    def google_sheets_go_to_column(column: str):
        '''Moves to the specified column'''
        actions.user.google_sheets_toggle_movement_tool()
        current_cell: CellLocation = CellLocation(get_selected_text_using_clipboard())
        current_row: str = current_cell.get_row()
        actions.insert(column + current_row)
        actions.key('enter')


class CellLocation:
    def __init__(self, location: str):
        row_start_index: int = 0
        for character in location:
            if character.isdigit():
                break
            row_start_index += 1
        self.column: str = location[:row_start_index]
        self.row: str = location[row_start_index:]
    
    def get_column(self) -> str:
        return self.column
    
    def get_row(self) -> str:
        return self.row