# Requires https://plugins.jetbrains.com/plugin/10504-voice-code-idea

app: /.*jetbrains.*/
-
# Auto complete
complete: user.knausj_talon.code.jetbrains.idea("action CodeCompletion")
perfect: user.knausj_talon.code.jetbrains.idea("action CodeCompletion,action CodeCompletion")
smart: user.knausj_talon.code.jetbrains.idea("action SmartTypeCompletion")
finish:  user.knausj_talon.code.jetbrains.idea("action EditorCompleteStatement")
done:  user.knausj_talon.code.jetbrains.idea("action EditorCompleteStatement")
toggle tools:  user.knausj_talon.code.jetbrains.idea("action HideAllWindows")

# Movement
drag up:  user.knausj_talon.code.jetbrains.idea("action MoveLineUp")
drag down:  user.knausj_talon.code.jetbrains.idea("action MoveLineDown")

# Copying
clone this:  user.knausj_talon.code.jetbrains.idea("action EditorDuplicate")
clone line:  user.knausj_talon.code.jetbrains.idea("action EditorDuplicate")
clone <number>: user.knausj_talon.code.jetbrains.idea_num("clone %s", number)
grab <number>: user.knausj_talon.code.jetbrains.idea_grab(number)

# Actions
(action | please): user.knausj_talon.code.jetbrains.idea("action GotoAction")
(action | please) <dgndictation>:
  user.knausj_talon.code.jetbrains.idea("action GotoAction")
  insert(dictate.join_words(dgndictation))
extend <number>: user.knausj_talon.code.jetbrains.extend_action(number)

# Refactoring
refactor: user.knausj_talon.code.jetbrains.idea("action Refactorings.QuickListPopupAction")
refactor <dgndictation>:
  user.knausj_talon.code.jetbrains.idea("action Refactorings.QuickListPopupAction")
  insert(dictate.join_words(dgndictation))
extract variable: user.knausj_talon.code.jetbrains.idea("action IntroduceVariable")
extract field: user.knausj_talon.code.jetbrains.idea("action IntroduceField")
extract constant: user.knausj_talon.code.jetbrains.idea("action IntroduceConstant")
extract parameter: user.knausj_talon.code.jetbrains.idea("action IntroduceParameter")
extract interface: user.knausj_talon.code.jetbrains.idea("action ExtractInterface")
extract method: user.knausj_talon.code.jetbrains.idea("action ExtractMethod")
refactor in line: user.knausj_talon.code.jetbrains.idea("action Inline")
refactor move: user.knausj_talon.code.jetbrains.idea("action Move")
refactor rename: user.knausj_talon.code.jetbrains.idea("action RenameElement")
rename file: user.knausj_talon.code.jetbrains.idea("action RenameFile")

# Quick Fix / Intentions

