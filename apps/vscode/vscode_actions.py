from talon import Context, actions
ctx = Context()
ctx.matches = r"""
#custom vscode commands go here
app: vscode
"""

@ctx.action_class('code')
class CodeActions:
    #talon code actions
    def toggle_comment(): actions.user.vscode('editor.action.commentLine')

@ctx.action_class('edit')
class EditActions:
    #talon edit actions
    def indent_more(): actions.user.vscode('editor.action.indentLines')
    def indent_less(): actions.user.vscode('editor.action.outdentLines')
    def save_all(): actions.user.vscode('workbench.action.files.saveAll')
    def jump_line(n: int): actions.user.vscode('workbench.action.gotoLine')
    def delete_word(): actions.actions.edit.select_word()
    def delete_line(): actions.user.vscode('editor.action.deleteLines')
    def line_insert_down(): actions.user.vscode('editor.action.insertLineAfter')
    def line_insert_up(): actions.user.vscode('editor.action.insertLineBefore')
    def line_swap_up(): actions.user.vscode('editor.action.moveLinesUpAction')
    def line_swap_down(): actions.user.vscode('editor.action.moveLinesDownAction')
    # action(edit.select_line): # metago
    # 	user.vscode("expandLineSelection")
    def select_none():
        actions.user.vscode('cancelSelection')
    def select_word():
        actions.user.vscode('editor.action.addSelectionToNextFindMatch')
        # splits.py support begin

@ctx.action_class('user')
class UserActions:
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
