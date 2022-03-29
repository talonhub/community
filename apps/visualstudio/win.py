from talon import Context, actions, app
ctx = Context()

ctx.matches = r"""
os: windows
app: visual_studio
"""

@ctx.action_class('app')
class AppActions:
    #talon app actions
    def tab_close():    actions.key('ctrl-f4')
    def tab_next():     actions.key('ctrl-tab')
    def tab_previous(): actions.key('ctrl-shift-tab')
    def tab_reopen():   actions.key('ctrl-1 ctrl-r enter')

@ctx.action_class('code')
class CodeActions:
    #talon code actions
    def toggle_comment(): actions.key('ctrl-k ctrl-/')

@ctx.action_class('edit')
class EditActions:
    #talon edit actions
    def indent_more(): actions.key('tab')
    def indent_less(): actions.key('shift-tab')
    def save_all():    actions.key('ctrl-shift-s')

@ctx.action_class('user')
class UserActions:
    #multiple_cursor.py support begin
    #note: visual studio has no explicit mode for multiple cursors; requires https://marketplace.visualstudio.com/items?itemName=VaclavNadrasky.MultiCaretBooster
    def multi_cursor_add_above():                actions.key('shift-alt-up')
    def multi_cursor_add_below():                actions.key('shift-alt-down')
    #action(user.multi_cursor_add_to_line_ends): does not exist :(
    def multi_cursor_disable():                  actions.key('escape')
    def multi_cursor_enable():                   actions.skip()
    def multi_cursor_select_all_occurrences():   actions.key('shift-alt-;')
    def multi_cursor_select_fewer_occurrences(): actions.key('shift-alt-k')
    def multi_cursor_select_more_occurrences():  actions.key('shift-alt->')
