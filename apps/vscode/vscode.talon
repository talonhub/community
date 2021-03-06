#custom vscode commands go here
app: vscode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.snippets
tag(): user.splits
tag(): user.tabs

action(edit.select_line):
	key(ctrl-e cmd-shift-left)

action(edit.delete_line):
	user.vscode("editor.action.deleteLines")

settings():
  key_wait = 0

#talon app actions
action(app.tab_close): user.vscode("workbench.action.closeActiveEditor")
action(app.tab_next): user.vscode("workbench.action.nextEditorInGroup")
action(app.tab_previous): user.vscode("workbench.action.previousEditorInGroup")
action(app.tab_reopen): user.vscode("workbench.action.reopenClosedEditor")
action(app.window_close): user.vscode("workbench.action.closeWindow")
action(app.window_open): user.vscode("workbench.action.newWindow")
go last: user.vscode_by_id("workbench.action.openPreviousRecentlyUsedEditorInGroup")
go next: user.vscode_by_id("workbench.action.openNextRecentlyUsedEditorInGroup")

#talon code actions
action(code.toggle_comment): user.vscode("editor.action.commentLine")

#talon edit actions
action(edit.indent_more): user.vscode("editor.action.indentLines")
action(edit.indent_less): user.vscode("editor.action.outdentLines")
action(edit.save_all): user.vscode("workbench.action.files.saveAll")

# splits.py support begin
action(user.split_clear_all):
	user.vscode("workbench.action.editorLayoutSingle")
action(user.split_clear):
	user.vscode("workbench.action.joinTwoGroups")
action(user.split_flip):
	user.vscode("workbench.action.toggleEditorGroupLayout") 
action(user.split_last):
	user.vscode("workbench.action.focusLeftGroup")
action(user.split_next): 
	user.vscode("workbench.action.focusRightGroup")
action(user.split_window_down):
	user.vscode("workbench.action.moveEditorToBelowGroup")
action(user.split_window_horizontally):
	user.vscode("workbench.action.splitEditorOrthogonal")
action(user.split_window_left):
	user.vscode("workbench.action.moveEditorToLeftGroup")
action(user.split_window_right):
	user.vscode("workbench.action.moveEditorToRightGroup")
action(user.split_window_up):
	user.vscode("workbench.action.moveEditorToAboveGroup")
action(user.split_window_vertically):
	user.vscode("workbench.action.splitEditor")
action(user.split_window):
	user.vscode("workbench.action.splitEditor")
splint:
	user.vscode("vscode-neovim.escape")
	sleep(25ms)
	user.split_next()
	key(a)
# splits.py support end

#multiple_cursor.py support begin
#note: vscode has no explicit mode for multiple cursors
action(user.multi_cursor_add_above):
	user.vscode("editor.action.insertCursorAbove")
action(user.multi_cursor_add_below):
	user.vscode("editor.action.insertCursorBelow")
action(user.multi_cursor_add_to_line_ends):
	user.vscode("editor.action.insertCursorAtEndOfEachLineSelected")
action(user.multi_cursor_disable): key(escape)
action(user.multi_cursor_enable): skip()
action(user.multi_cursor_select_all_occurrences):
	user.vscode("editor.action.selectHighlights")
action(user.multi_cursor_select_fewer_occurrences):
	user.vscode("cursorUndo")
action(user.multi_cursor_select_more_occurrences):
	user.vscode("editor.action.addSelectionToNextFindMatch")
#multiple_cursor.py support end

please [<user.text>]: 
  user.vscode("workbench.action.showCommands")
  insert(user.text or "")

# Sidebar
bar explore: user.vscode("workbench.view.explorer")
bar extensions: user.vscode("workbench.view.extensions")
bar outline: user.vscode("outline.focus")
bar run: user.vscode("workbench.view.debug")
bar search: user.vscode("workbench.view.search")
bar source: user.vscode_by_id("workbench.view.scm")
bar dog: user.vscode("workbench.action.toggleSidebarVisibility")
search [<user.text>]: 
  user.vscode_by_id("workbench.action.findInFiles")
  sleep(50ms)
  insert(text or "")
search next: user.vscode("search.action.focusNextSearchResult")
search last: user.vscode("search.action.focusPreviousSearchResult")

symbol hunt [<user.text>]:
  user.vscode("workbench.action.gotoSymbol")
  sleep(50ms)
  insert(text or "")

symbol last: user.vscode("gotoNextPreviousMember.previousMember")
symbol next: user.vscode("gotoNextPreviousMember.nextMember")
go symbol: user.vscode("semantic-movement.jumpToContainingSymbol")
go funk: user.vscode("semantic-movement.jumpToContainingFunction")
go named funk: user.vscode("semantic-movement.jumpToContainingNamedFunction")
go class: user.vscode("semantic-movement.jumpToContainingClass")
take symbol: user.vscode("semantic-movement.selectContainingSymbol")
take funk: user.vscode("semantic-movement.selectContainingFunction")
take named funk: user.vscode("semantic-movement.selectContainingNamedFunction")
take class: user.vscode("semantic-movement.selectContainingClass")

# Panels
panel control: user.vscode("workbench.panel.repl.view.focus")
panel output: user.vscode("workbench.panel.output.focus")
panel problems: user.vscode("workbench.panel.markers.view.focus")
pan dog: user.vscode("workbench.action.togglePanel")
panel terminal: user.vscode("workbench.panel.terminal.focus")
panel editor: user.vscode_by_id("workbench.action.focusActiveEditorGroup")

# Settings
show settings: user.vscode("workbench.action.openGlobalSettings")
show shortcuts: user.vscode("workbench.action.openGlobalKeybindings")
show snippets: user.vscode("workbench.action.openSnippets")

# Display
centered switch: user.vscode("workbench.action.toggleCenteredLayout")
fullscreen switch: user.vscode("workbench.action.toggleFullScreen")
theme switch: user.vscode("workbench.action.selectTheme")
wrap switch: user.vscode("editor.action.toggleWordWrap")
zen switch: user.vscode("workbench.action.toggleZenMode")

# File Commands
file hunt [<user.text>]: 
  user.vscode("workbench.action.quickOpen")
  sleep(50ms)
  insert(text or "")
file copy path:
	user.vscode_ignore_clipboard("copyFilePath") 
file create sibling: user.vscode("explorer.newFile")  
file create: user.vscode("workbench.action.files.newUntitledFile")
file rename: user.vscode("fileutils.renameFile")
file open folder:
	user.vscode("revealFileInOS")
file reveal: user.vscode("workbench.files.action.showActiveFileInExplorer") 
save ugly:
    user.vscode("workbench.action.files.saveWithoutFormatting")
file clone: user.vscode("fileutils.duplicateFile")

# Language Features
suggest show: user.vscode("editor.action.triggerSuggest")
hint show: user.vscode("editor.action.triggerParameterHints")
def show: user.vscode("editor.action.revealDefinition")
definition peek: user.vscode("editor.action.peekDefinition")
definition side: user.vscode("editor.action.revealDefinitionAside")
references show: user.vscode("editor.action.goToReferences")
ref show: user.vscode("references-view.find")
format that: user.vscode("editor.action.formatDocument")
format selection: user.vscode("editor.action.formatSelection")
imports fix: user.vscode("editor.action.organizeImports")
problem next: user.vscode("editor.action.marker.nextInFiles")
problem last: user.vscode("editor.action.marker.prevInFiles")
problem fix: user.vscode("problems.action.showQuickFixes")
rename that: user.vscode("editor.action.rename")
refactor that: user.vscode("editor.action.refactor")
whitespace trim: user.vscode("editor.action.trimTrailingWhitespace")
language switch: user.vscode("workbench.action.editor.changeLanguageMode")
refactor rename: user.vscode("editor.action.rename")
refactor this: user.vscode("editor.action.refactor")
ref next:
   user.vscode("references-view.tree.focus")
   key(down enter)
ref last:
   user.vscode("references-view.tree.focus")
   key(up enter)

#code navigation
(go declaration | follow):
	user.vscode("editor.action.revealDefinition")
go back:
	user.vscode("workbench.action.navigateBack") 
go forward:  user.vscode("workbench.action.navigateForward")  
go implementation:
	user.vscode("editor.action.goToImplementation")
go type:
	user.vscode("editor.action.goToTypeDefinition")
go usage:
	user.vscode("references-view.find")

# Bookmarks. Requires Bookmarks plugin
session [<user.text>]: 
  user.vscode("workbench.action.openRecent")
  sleep(50ms)
  insert(text or "")

go marks: user.vscode("workbench.view.extension.bookmarks")
toggle mark: user.vscode("bookmarks.toggle")
go next mark: user.vscode("bookmarks.jumpToNext")
go last mark: user.vscode("bookmarks.jumpToPrevious")

# Folding
fold that: user.vscode("editor.fold")
unfold that: user.vscode("editor.unfold")
fold those: user.vscode("editor.foldAllMarkerRegions")
unfold those: user.vscode("editor.unfoldRecursively")
fold all: user.vscode("editor.foldAll")
unfold all: user.vscode("editor.unfoldAll")
fold comments: user.vscode("editor.foldAllBlockComments")

# Git / Github (not using verb-noun-adjective pattern, mirroring terminal commands.)
git branch: user.vscode("git.branchFrom")
git branch this: user.vscode("git.branch")
git checkout [<user.text>]: 
  user.vscode_by_id("git.checkout")
  sleep(50ms)
  insert(text or "")
git commit: user.vscode("git.commitStaged")
git commit undo: user.vscode("git.undoCommit")
git commit ammend: user.vscode("git.commitStagedAmend")
git diff: user.vscode("git.openChange")
git ignore: user.vscode("git.ignore")
git merge: user.vscode("git.merge")
git output: user.vscode("git.showOutput")
git pull: user.vscode("git.pullRebase")
git push: user.vscode("git.push")
git push focus: user.vscode("git.pushForce")
git rebase abort: user.vscode("git.rebaseAbort")
git reveal: user.vscode("git.revealInExplorer")
git revert: user.vscode("git.revertChange")
git stash: user.vscode("git.stash")
git stash pop: user.vscode("git.stashPop")
git status: user.vscode_by_id("workbench.scm.focus")
git stage: user.vscode("git.stage")
git stage all: user.vscode("git.stageAll")
git unstage: user.vscode("git.unstage")
git unstage all: user.vscode("git.unstageAll")
pull request: user.vscode_by_id("pr.create")
change next: key(alt-f5)
change last: key(shift-alt-f5)

#Debugging
break point: user.vscode("editor.debug.action.toggleBreakpoint")
step over: user.vscode("workbench.action.debug.stepOver")
debug step into: user.vscode("workbench.action.debug.stepInto")
debug step out [of]: user.vscode("workbench.action.debug.stepOut")
debug start: user.vscode("workbench.action.debug.start")
debug pause: user.vscode("workbench.action.debug.pause")
debug stopper: user.vscode("workbench.action.debug.stop")
debug continue: user.vscode("workbench.action.debug.continue")
debug restart: user.vscode("workbench.action.debug.restart")
debug console: user.vscode("workbench.debug.action.toggleRepl")

# Terminal
term external: user.vscode("workbench.action.terminal.openNativeConsole")
term new: user.vscode("workbench.action.terminal.new")
term next: user.vscode("workbench.action.terminal.focusNextPane")
term last:user.vscode("workbench.action.terminal.focusPreviousPane")
term split: user.vscode("workbench.action.terminal.split")
term zoom: user.vscode_by_id("workbench.action.toggleMaximizedPanel")
term trash: user.vscode("workbench.action.terminal.kill")
term dog: user.vscode_by_id("workbench.action.terminal.toggleTerminal")
term scroll up: user.vscode("workbench.action.terminal.scrollUp")
term scroll down: user.vscode("workbench.action.terminal.scrollDown")
term <number_small>: user.vscode_terminal(number_small)

#TODO: should this be added to linecommands?
copy line down: user.vscode("editor.action.copyLinesDownAction")
copy line up: user.vscode("editor.action.copyLinesUpAction")

#Expand/Shrink AST Selection
take less: user.vscode("editor.action.smartSelect.shrink")
take (more|this): user.vscode("editor.action.smartSelect.expand")

minimap: user.vscode_by_id("editor.action.toggleMinimap")
maximize: user.vscode_by_id("workbench.action.minimizeOtherEditors")
restore: user.vscode_by_id("workbench.action.evenEditorWidths")

replace here:
	user.replace("")
	key(cmd-alt-l)

hover show: user.vscode("editor.action.showHover")

edit last: user.vscode("editsHistory.moveCursorToPreviousEdit")
edit next: user.vscode("editsHistory.moveCursorToNextEdit")
edit add: user.vscode("editsHistory.createEditAtCursor")
edit last here: user.vscode("editsHistory.moveCursorToPreviousEditInSameFile")
edit next here: user.vscode("editsHistory.moveCursorToNextEditInSameFile")

join lines: user.vscode("editor.action.joinLines")

commode:
	user.vscode("vscode-neovim.escape")
	sleep(25ms)

insert:
	key(i)
	sleep(25ms)

replace smart:
	key(:)
	sleep(50ms)
	key(S)
	key(/)

swap this: user.vscode("extension.swap")

full screen: user.vscode("workbench.action.toggleFullScreen")
reload window: user.vscode("workbench.action.reloadWindow")

curse undo: user.vscode("cursorUndo")

take word: user.vscode("editor.action.addSelectionToNextFindMatch")

take [{user.symbol_color}] <user.any_alphanumeric_key>:
	user.vscode("decorative-navigation.selectToken", symbol_color or "default", any_alphanumeric_key)

go [{user.symbol_color}] <user.any_alphanumeric_key>:
	user.vscode("decorative-navigation.selectToken", symbol_color or "default", any_alphanumeric_key)
	key(left)

def show [{user.symbol_color}] <user.any_alphanumeric_key>:
	user.vscode("decorative-navigation.selectToken", symbol_color or "default", any_alphanumeric_key)
	user.vscode("editor.action.revealDefinition")

action(user.alveolar_click): user.vscode("decorative-navigation.toggleDecorations")