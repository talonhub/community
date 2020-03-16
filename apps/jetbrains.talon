# Requires https://plugins.jetbrains.com/plugin/10504-voice-code-idea

app: /.*jetbrains.*/
-
action(app.tab_next):
  key(ctrl-tab)

# Auto complete
action(user.ide_complete): user.idea("action CodeCompletion")
action(user.ide_perfect): user.idea("action CodeCompletion,action CodeCompletion")
action(user.ide_smart): user.idea("action SmartTypeCompletion")
action(user.ide_done):  user.idea("action EditorCompleteStatement")
action(user.ide_toggle_tools):  user.idea("action HideAllWindows")

# Movement
action(user.drag_up):  user.idea("action MoveLineUp")
action(user.drag_down):  user.idea("action MoveLineDown")
action(user.multi_cursor): key(shift-alt-insert)
action(user.multi_cursor_stop): key(escape)
action(user.up_cursor): user.idea("action EditorCloneCaretAbove")
action(user.down_cursor): user.idea("action EditorCloneCaretBelow")

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
action(user.ide_refactor): user.idea("action Refactorings.QuickListPopupAction")
refactor <dgndictation>:
  user.idea("action Refactorings.QuickListPopupAction")
  insert(dictate.join_words(dgndictation))
action(user.ide_extract_variable): user.idea("action IntroduceVariable")
action(user.ide_extract_field): user.idea("action IntroduceField")
action(user.ide_extract_constant): user.idea("action IntroduceConstant")
action(user.ide_extract_parameter): user.idea("action IntroduceParameter")
action(user.ide_extract_interface): user.idea("action ExtractInterface")
action(user.ide_extract_method): user.idea("action ExtractMethod")
action(user.ide_refactor_in_line): user.idea("action Inline")
action(user.ide_refactor_move): user.idea("action Move")
action(user.ide_refactor_rename): user.idea("action RenameElement")
action(user.ide_rename_file): user.idea("action RenameFile")

action(user.ide_fix_format): user.idea("action ReformatCode")
action(user.ide_fix_imports): user.idea("action OptimizeImports")

action(user.ide_follow): user.idea("action GotoDeclaration")
action(user.ide_go_implementation): user.idea("action GotoImplementation")
action(user.ide_go_usage): user.idea("action FindUsages")
action(user.ide_go_type): user.idea("action GotoTypeDeclaration")
action(user.ide_go_test): user.idea("action GotoTest")
action(user.ide_go_back): user.idea("action Back")
action(user.ide_go_forward): user.idea("action Forward")

# Special Selects
action(user.select_less): user.idea("action EditorUnSelectWord")
action(user.select_more): user.idea("action EditorSelectWord")
action(user.multi_select_fewer): user.idea("action UnselectPreviousOccurrence")
action(user.multi_select_more): user.idea("action SelectNextOccurrence")
action(user.multi_select_all): user.idea("action SelectAllOccurrences")

# Search
action(edit.find): user.idea("action Find")
action(user.ide_find_everywhere): user.idea("action SearchEverywhere")
find (everywhere | all) <phrase> [over]:
  user.idea("action SearchEverywhere")
  sleep(500ms)
  insert(phrase)

action(user.ide_find_class): user.idea("action GotoClass")
action(user.ide_find_file): user.idea("action GotoFile")
action(user.ide_recent): user.idea("action RecentFiles")
action(edit.find_next): user.idea("action FindNext")
action(edit.find_previous): user.idea("action FindPrevious")
action(user.ide_find_in_path): user.idea("action FindInPath")

# Select verb/object

<user.select_verbs> this: user.idea_select(select_verbs, "action EditorSelectWord")
<user.select_verbs> whole line <number>: user.idea_select(select_verbs, "goto {number} 0, action EditorSelectLine")
<user.select_verbs> way left: user.idea_select(select_verbs, "action EditorLineStartWithSelection")
<user.select_verbs> way right: user.idea_select(select_verbs, "action EditorLineEndWithSelection")
<user.select_verbs> way up: user.idea_select(select_verbs, "action EditorTextStartWithSelection")
<user.select_verbs> way down: user.idea_select(select_verbs, "action EditorTextEndWithSelection")
<user.select_verbs> camel left: user.idea_select(select_verbs, "action EditorPreviousWordInDifferentHumpsModeWithSelection")
<user.select_verbs> camel right: user.idea_select(select_verbs, "action EditorNextWordInDifferentHumpsModeWithSelection")

<user.select_verbs> all: user.idea_select(select_verbs, "action $SelectAll")
<user.select_verbs> left: user.idea_select(select_verbs, "action EditorLeftWithSelection")
<user.select_verbs> right: user.idea_select(select_verbs, "action EditorRightWithSelection")
<user.select_verbs> up: user.idea_select(select_verbs, "action EditorUpWithSelection")
<user.select_verbs> down: user.idea_select(select_verbs, "action EditorDownWithSelection")
<user.select_verbs> word left: user.idea_select(select_verbs, "action EditorPreviousWordWithSelection")
<user.select_verbs> word right: user.idea_select(select_verbs, "action EditorNextWordWithSelection")

<user.select_verbs> until line <number>: user.idea_select(select_verbs, "extend {number}")
<user.select_verbs> <number> until <number>: user.idea_select(select_verbs, "range {number_1} {number_2}")
<user.select_verbs> line <number>: user.idea_select(select_verbs, "goto {number} 0, action EditorLineStart, action EditorLineEndWithSelection")
<user.select_verbs> line: user.idea_select(select_verbs, "action EditorLineStart, action EditorLineEndWithSelection")
<user.select_verbs> next <phrase> [over]: user.idea_select(select_verbs, "find next {phrase}")
<user.select_verbs> last <phrase> [over]: user.idea_select(select_verbs, "find prev {phrase}")

# Movement
<user.movement_verbs> this: user.idea_movement(movement_verbs, "")
<user.movement_verbs> next (error | air): user.idea_movement(movement_verbs, "action GotoNextError")
<user.movement_verbs> last (error | air): user.idea_movement(movement_verbs, "action GotoPreviousError")
<user.movement_verbs> camel left: user.idea_movement(movement_verbs, "action EditorPreviousWordInDifferentHumpsMode")
<user.movement_verbs> camel right: user.idea_movement(movement_verbs, "action EditorNextWordInDifferentHumpsMode")
<user.movement_verbs> line <number>: user.idea_movement(movement_verbs, "goto {number} 0")
<user.movement_verbs> line <number> end: user.idea_movement(movement_verbs, "goto {number} 9999")
<user.movement_verbs> next <phrase> [over]: user.idea_movement(movement_verbs, "find next {phrase}, action EditorRight")
<user.movement_verbs> last <phrase> [over]: user.idea_movement(movement_verbs, "find prev {phrase}, action EditorRight")
