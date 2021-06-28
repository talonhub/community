from talon import Context, actions
ctx = Context()
ctx.matches = r"""
app: vscode
"""

@ctx.action_class('app')
class AppActions:
    #talon app actions
    def tab_close():    actions.user.vscode('workbench.action.closeActiveEditor')
    def tab_next():     actions.user.vscode('workbench.action.nextEditorInGroup')
    def tab_previous(): actions.user.vscode('workbench.action.previousEditorInGroup')
    def tab_reopen():   actions.user.vscode('workbench.action.reopenClosedEditor')
    def window_close(): actions.user.vscode('workbench.action.closeWindow')
    def window_open():  actions.user.vscode('workbench.action.newWindow')

@ctx.action_class('code')
class CodeActions:
    #talon code actions
    def toggle_comment(): actions.user.vscode('editor.action.commentLine')

@ctx.action_class('edit')
class EditActions:
    #talon edit actions
    def indent_more(): actions.user.vscode('editor.action.indentLines')
    def indent_less(): actions.user.vscode('editor.action.outdentLines')
    def save_all():    actions.user.vscode('workbench.action.files.saveAll')

@ctx.action_class('user')
class UserActions:
    # splits.py support begin
    def split_clear_all():                       actions.user.vscode('workbench.action.editorLayoutSingle')
    def split_clear():                           actions.user.vscode('workbench.action.joinTwoGroups')
    def split_flip():                            actions.user.vscode('workbench.action.toggleEditorGroupLayout')
    def split_last():                            actions.user.vscode('workbench.action.focusLeftGroup')
    def split_next():                            actions.user.vscode_and_wait('workbench.action.focusRightGroup')
    def split_window_down():                     actions.user.vscode('workbench.action.moveEditorToBelowGroup')
    def split_window_horizontally():             actions.user.vscode('workbench.action.splitEditorOrthogonal')
    def split_window_left():                     actions.user.vscode('workbench.action.moveEditorToLeftGroup')
    def split_window_right():                    actions.user.vscode('workbench.action.moveEditorToRightGroup')
    def split_window_up():                       actions.user.vscode('workbench.action.moveEditorToAboveGroup')
    def split_window_vertically():               actions.user.vscode('workbench.action.splitEditor')
    def split_window():                          actions.user.vscode('workbench.action.splitEditor')
    # splits.py support end
    
    #multiple_cursor.py support begin
    #note: vscode has no explicit mode for multiple cursors
    def multi_cursor_add_above():                actions.user.vscode('editor.action.insertCursorAbove')
    def multi_cursor_add_below():                actions.user.vscode('editor.action.insertCursorBelow')
    def multi_cursor_add_to_line_ends():         actions.user.vscode('editor.action.insertCursorAtEndOfEachLineSelected')
    def multi_cursor_disable():                  actions.key('escape')
    def multi_cursor_enable():                   actions.skip()
    def multi_cursor_select_all_occurrences():   actions.user.vscode('editor.action.selectHighlights')
    def multi_cursor_select_fewer_occurrences(): actions.user.vscode('cursorUndo')
    def multi_cursor_select_more_occurrences():  actions.user.vscode('editor.action.addSelectionToNextFindMatch')
