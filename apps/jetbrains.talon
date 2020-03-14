# Requires https://plugins.jetbrains.com/plugin/10504-voice-code-idea

app: /.*jetbrains.*/
-
# Auto complete
action(user.complete): user.idea("action CodeCompletion")
action(user.perfect): user.idea("action CodeCompletion,action CodeCompletion")
action(user.smart): user.idea("action SmartTypeCompletion")
action(user.done):  user.idea("action EditorCompleteStatement")
action(user.toggle_tools):  user.idea("action HideAllWindows")

# Movement
action(user.drag_up):  user.idea("action MoveLineUp")
action(user.drag_down):  user.idea("action MoveLineDown")
action(user.multi_cursor): key(shift-alt-insert)
action(user.multi_cursor_stop): key(escape)
action(user.up_cursor): key(shift-up)
action(user.down_cursor): key(shift-down)

# Copying
action(user.clone_line):  user.idea("action EditorDuplicate")
clone <number>: user.idea("clone {number}")
grab <number>: user.idea_grab(number)

# Actions
(action | please): user.idea("action GotoAction")
(action | please) <dgndictation>:
  user.idea("action GotoAction")
  insert(dictate.join_words(dgndictation))
extend <number>: user.extend_action(number)

# Refactoring
#refactor: user.idea("action Refactorings.QuickListPopupAction")
#refactor <dgndictation>:
#  user.idea("action Refactorings.QuickListPopupAction")
#  insert(dictate.join_words(dgndictation))
action(user.extract_variable): user.idea("action IntroduceVariable")
action(user.extract_field): user.idea("action IntroduceField")
action(user.extract_constant): user.idea("action IntroduceConstant")
action(user.extract_parameter): user.idea("action IntroduceParameter")
action(user.extract_interface): user.idea("action ExtractInterface")
action(user.extract_method): user.idea("action ExtractMethod")
action(user.refactor_in_line): user.idea("action Inline")
action(user.refactor_move): user.idea("action Move")
action(user.refactor_rename): user.idea("action RenameElement")
action(user.rename_file): user.idea("action RenameFile")

# Quick Fix / Intentions

