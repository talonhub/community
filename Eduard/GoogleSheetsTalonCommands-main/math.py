from talon import actions, Module, Context

def insert_function(function: str):
    actions.insert(function)
    surround_cursor_with_parentheses()

def surround_cursor_with_parentheses():
    actions.insert('()')
    actions.edit.left()

module = Module()

module.list('google_sheets_math_functions', desc = 'Google sheets math functions')
context = Context()
context.lists['user.google_sheets_math_functions'] = {
    'max': 'MAX'
}
@module.capture(rule = '{user.google_sheets_math_functions}')
def google_sheets_math_function(m) -> str:
    return m.google_sheets_math_functions

@module.action_class
class Actions:
    def google_sheets_insert_function(function: str):
        '''Inserts the specified function into google sheets'''
        insert_function(function)