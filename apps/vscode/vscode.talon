#custom vscode commands go here
app: vscode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.snippets
tag(): user.splits
tag(): user.tabs

# TODO remove this once implemented in cursorless
cut line:
	key(cmd-x)

action(edit.select_line):
	key(ctrl-e cmd-shift-left)

action(edit.delete_line):
	user.vscode_and_wait("editor.action.deleteLines")

action(user.new_line_below):
	user.vscode_and_wait("editor.action.insertLineAfter")

action(user.new_line_above):
	user.vscode_and_wait("editor.action.insertLineBefore")

settings():
  key_wait = 1

#talon app actions
action(app.tab_close): user.vscode("workbench.action.closeActiveEditor")
action(app.tab_next): user.vscode("workbench.action.nextEditorInGroup")
action(app.tab_previous): user.vscode("workbench.action.previousEditorInGroup")
action(app.tab_reopen): user.vscode("workbench.action.reopenClosedEditor")
action(app.window_close): user.vscode("workbench.action.closeWindow")
action(app.window_open): user.vscode("workbench.action.newWindow")
<user.teleport> last: user.vscode("workbench.action.openPreviousRecentlyUsedEditorInGroup")
<user.teleport> next: user.vscode("workbench.action.openNextRecentlyUsedEditorInGroup")

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
	user.vscode_and_wait("workbench.action.focusRightGroup")
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
cross:
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
bar source: user.vscode("workbench.view.scm")
bar dog: user.vscode("workbench.action.toggleSidebarVisibility")
search next: user.vscode("search.action.focusNextSearchResult")
search last: user.vscode("search.action.focusPreviousSearchResult")

symbol hunt [<user.text>]:
  user.vscode("workbench.action.gotoSymbol")
  sleep(50ms)
  insert(text or "")

symbol last: user.vscode("gotoNextPreviousMember.previousMember")
symbol next: user.vscode("gotoNextPreviousMember.nextMember")
<user.teleport> symbol: user.vscode_and_wait("semantic-movement.jumpToContainingSymbol")
<user.teleport> funk: user.vscode_and_wait("semantic-movement.jumpToContainingFunction")
<user.teleport> named funk: user.vscode_and_wait("semantic-movement.jumpToContainingNamedFunction")
<user.teleport> class: user.vscode_and_wait("semantic-movement.jumpToContainingClass")
<user.select> symbol: user.vscode_and_wait("semantic-movement.selectContainingSymbol")
<user.select> funk: user.vscode_and_wait("semantic-movement.selectContainingFunction")
<user.select> named funk: user.vscode_and_wait("semantic-movement.selectContainingNamedFunction")
<user.select> class: user.vscode_and_wait("semantic-movement.selectContainingClass")

# Panels
panel control: user.vscode("workbench.panel.repl.view.focus")
panel output: user.vscode("workbench.panel.output.focus")
panel problems: user.vscode("workbench.panel.markers.view.focus")
pan dog: user.vscode("workbench.action.togglePanel")
panel terminal: user.vscode("workbench.panel.terminal.focus")
pan edit: user.vscode("workbench.action.focusActiveEditorGroup")

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
<user.find> dock [<user.text>] [{user.file_extension}]: 
  user.vscode("workbench.action.quickOpen")
  sleep(50ms)
  insert(text or "")
  insert(file_extension or "")
  sleep(300ms)
<user.teleport> dock [<user.text>] [{user.file_extension}]: 
  user.vscode("workbench.action.quickOpen")
  sleep(50ms)
  insert(text or "")
  insert(file_extension or "")
  sleep(300ms)
  key(enter)
file copy path:
	user.vscode("copyFilePath") 
file create sibling <user.format_text>* [<user.word>] [{user.file_extension}]: 
  user.vscode_and_wait("explorer.newFile")
  sleep(500ms)
  user.insert_many(format_text_list or "")
  user.insert_formatted(user.word or "", "NOOP")
  insert(file_extension or "")
file create: user.vscode("workbench.action.files.newUntitledFile")
file rename:
	user.vscode("fileutils.renameFile")
	sleep(150ms)
file move:
	user.vscode("fileutils.moveFile")
	sleep(150ms)
file open folder:
	user.vscode("revealFileInOS")
file reveal: user.vscode("workbench.files.action.showActiveFileInExplorer") 
save ugly:
    user.vscode("workbench.action.files.saveWithoutFormatting")
file clone:
	user.vscode("fileutils.duplicateFile")
	sleep(150ms)
action(edit.save):
	key(cmd-s)
	sleep(50ms)

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
(<user.teleport> declaration | follow):
	user.vscode("editor.action.revealDefinition")
spring back:
	user.vscode("workbench.action.navigateBack") 
spring forward:  user.vscode("workbench.action.navigateForward")  
<user.teleport> implementation:
	user.vscode("editor.action.goToImplementation")
<user.teleport> type:
	user.vscode("editor.action.goToTypeDefinition")
<user.teleport> usage:
	user.vscode("references-view.find")

# Bookmarks. Requires Bookmarks plugin
<user.find> sesh [<user.text>]: 
  user.vscode("workbench.action.openRecent")
  sleep(50ms)
  insert(text or "")
  sleep(250ms)
<user.teleport> sesh [<user.text>]: 
  user.vscode("workbench.action.openRecent")
  sleep(50ms)
  insert(text or "")
  key(enter)
  sleep(250ms)

<user.teleport> marks: user.vscode("workbench.view.extension.bookmarks")
toggle mark: user.vscode("bookmarks.toggle")
<user.teleport> next mark: user.vscode("bookmarks.jumpToNext")
<user.teleport> last mark: user.vscode("bookmarks.jumpToPrevious")

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
  user.vscode("git.checkout")
  sleep(50ms)
  insert(text or "")
git commit [<user.text>]:
  user.vscode("git.commitStaged")
  sleep(100ms)
  user.insert_formatted(text or "", "CAPITALIZE_FIRST_WORD")
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
git status: user.vscode("workbench.scm.focus")
git stage: user.vscode("git.stage")
git stage all: user.vscode("git.stageAll")
git unstage: user.vscode("git.unstage")
git unstage all: user.vscode("git.unstageAll")
pull request: user.vscode("pr.create")
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
term next: user.vscode("workbench.action.terminal.focusNext")
term last:user.vscode("workbench.action.terminal.focusPrevious")
term split: user.vscode("workbench.action.terminal.split")
term zoom: user.vscode("workbench.action.toggleMaximizedPanel")
term trash: user.vscode("workbench.action.terminal.kill")
term dog: user.vscode_and_wait("workbench.action.terminal.toggleTerminal")
term scroll up: user.vscode("workbench.action.terminal.scrollUp")
term scroll down: user.vscode("workbench.action.terminal.scrollDown")
term <number_small>: user.vscode_terminal(number_small)

#TODO: should this be added to linecommands?
copy line down: user.vscode("editor.action.copyLinesDownAction")
copy line up: user.vscode("editor.action.copyLinesUpAction")

#Expand/Shrink AST Selection
<user.select> less: user.vscode("editor.action.smartSelect.shrink")
<user.select> (more|this): user.vscode("editor.action.smartSelect.expand")

minimap: user.vscode("editor.action.toggleMinimap")
maximize: user.vscode("workbench.action.minimizeOtherEditors")
restore: user.vscode("workbench.action.evenEditorWidths")

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
close window: user.vscode("workbench.action.closeWindow")

curse undo: user.vscode("cursorUndo")

<user.select> word: user.vscode("editor.action.addSelectionToNextFindMatch")
skip word: user.vscode("editor.action.moveSelectionToNextFindMatch")

Github open: user.vscode("openInGithub.openInGitHubFile")

stage on:
	user.vscode_and_wait("git.stage")
	key(cmd-w)
	user.vscode_and_wait("workbench.scm.focus")
	key(down:100)
	sleep(100ms)
	key(enter)

# jupyter
cell next: user.vscode("jupyter.gotoNextCellInFile")
cell last: user.vscode("jupyter.gotoPrevCellInFile")
cell run above: user.vscode("jupyter.runallcellsabove.palette")
cell run: user.vscode("jupyter.runcurrentcell")