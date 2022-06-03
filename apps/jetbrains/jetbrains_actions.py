from talon import Context, actions
ctx = Context()
ctx.matches = r"""
# Requires https://plugins.jetbrains.com/plugin/10504-voice-code-idea
app: jetbrains
"""

@ctx.action_class('user')
class UserActions:
    #talon app actions (+custom tab actions)
    def tab_final():                             actions.user.idea('action GoToLastTab')
    
    # splits.py support begin
    def split_clear_all():                       actions.user.idea('action UnsplitAll')
    def split_clear():                           actions.user.idea('action Unsplit')
    def split_flip():                            actions.user.idea('action ChangeSplitOrientation')
    def split_last():                            actions.user.idea('action LastSplitter')
    def split_next():                            actions.user.idea('action NextSplitter')
    def split_window_down():                     actions.user.idea('action MoveTabDown')
    def split_window_horizontally():             actions.user.idea('action SplitHorizontally')
    #action(user.split_window_left): user.idea("action MoveTabLeft")
    def split_window_right():                    actions.user.idea('action MoveTabRight')
    #action(user.split_window_up): user.idea("action MoveTabUp")
    def split_window_vertically():               actions.user.idea('action SplitVertically')
    def split_window():                          actions.user.idea('action EditSourceInNewWindow')
    # splits.py support end
    
    # multiple_cursors.py support begin
    def multi_cursor_add_above():                actions.user.idea('action EditorCloneCaretAbove')
    def multi_cursor_add_below():                actions.user.idea('action EditorCloneCaretBelow')
    def multi_cursor_disable():                  actions.key('escape')
    def multi_cursor_enable():                   actions.key('shift-alt-insert')
    def multi_cursor_select_all_occurrences():   actions.user.idea('action SelectAllOccurrences')
    def multi_cursor_select_fewer_occurrences(): actions.user.idea('action UnselectPreviousOccurrence')
    def multi_cursor_select_more_occurrences():  actions.user.idea('action SelectNextOccurrence')

@ctx.action_class('app')
class AppActions:
    def tab_next():     actions.user.idea('action NextTab')
    def tab_previous(): actions.user.idea('action PreviousTab')
    
    def tab_close():    actions.user.idea('action CloseContent')
    def tab_reopen():   actions.user.idea('action ReopenClosedTab')

@ctx.action_class('code')
class CodeActions:
    #talon code actions
    def toggle_comment(): actions.user.idea('action CommentByLineComment')

@ctx.action_class('edit')
class EditActions:
    #talon edit actions
    def copy():                   actions.user.idea('action EditorCopy')
    def cut():                    actions.user.idea('action EditorCut')
    def delete():                 actions.user.idea('action EditorBackSpace')
    def paste():                  actions.user.idea('action EditorPaste')
    def find_next():              actions.user.idea('action FindNext')
    def find_previous():          actions.user.idea('action FindPrevious')
    def find(text: str=None):     actions.user.idea('action Find')
    def line_clone():             actions.user.idea('action EditorDuplicate')
    def line_swap_down():         actions.user.idea('action MoveLineDown')
    def line_swap_up():           actions.user.idea('action MoveLineUp')
    def indent_more():            actions.user.idea('action EditorIndentLineOrSelection')
    def indent_less():            actions.user.idea('action EditorUnindentSelection')
    def select_line(n: int=None): actions.user.idea('action EditorSelectLine')
    def select_word():            actions.user.idea('action EditorSelectWord')
    def select_all():             actions.user.idea('action $SelectAll')
    def file_start():             actions.user.idea('action EditorTextStart')
    def file_end():               actions.user.idea('action EditorTextEnd')
    def extend_file_start():      actions.user.idea('action EditorTextStartWithSelection')
    def extend_file_end():        actions.user.idea('action EditorTextEndWithSelection')
