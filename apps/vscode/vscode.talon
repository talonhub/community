app: vscode
-
tag(): user.multiple_cursors

tag(): user.snippets
tag(): user.splits
tag(): user.tabs
#talon app actions


action(app.tab_close): user.vscode("workbench.action.closeActiveEditor")
action(app.tab_next): user.vscode("workbench.action.nextEditorInGroup")
action(app.tab_previous): user.vscode("workbench.action.previousEditorInGroup")
action(app.tab_reopen): user.vscode("workbench.action.reopenClosedEditor")
action(app.window_close): user.vscode("workbench.action.closeWindow")
action(app.window_open): user.vscode("workbench.action.newWindow")
window reload: user.vscode("workbench.action.reloadWindow")
window close: user.vscode("workbench.action.closeWindow")

#talon code actRight
action(code.toggle_comment): user.vscode("editor.action.commentLine")

#talon edit actions
action(edit.indent_more): user.vscode("editor.action.indentLines")
action(edit.indent_less): user.vscode("editor.action.outdentLines")
action(edit.save_all): user.vscode("workbench.action.files.saveAll")

# splits.py support begin
action(user.split_clear_all): user.vscode("workbench.action.editorLayoutSingle")
action(user.split_clear): user.vscode("workbench.action.joinTwoGroups")
action(user.split_flip): user.vscode("workbench.action.toggleEditorGroupLayout") 
action(user.split_last): user.vscode("workbench.action.focusLeftGroup")
action(user.split_next): user.vscode_and_wait("workbench.action.focusRightGroup")
action(user.split_window_down): user.vscode("workbench.action.moveEditorToBelowGroup")
action(user.split_window_horizontally): user.vscode("workbench.action.splitEditorOrthogonal")
action(user.split_window_left): user.vscode("workbench.action.moveEditorToLeftGroup")
action(user.split_window_right): user.vscode("workbench.action.moveEditorToRightGroup")
action(user.split_window_up): user.vscode("workbench.action.moveEditorToAboveGroup")
action(user.split_window_vertically): user.vscode("workbench.action.splitEditor")
action(user.split_window): user.vscode("workbench.action.splitEditor")
# splits.py support end

#multiple_cursor.py support begin
#note: vscode has no explicit mode for multiple cursors
action(user.multi_cursor_add_above): user.vscode("editor.action.insertCursorAbove")
action(user.multi_cursor_add_below): user.vscode("editor.action.insertCursorBelow")
action(user.multi_cursor_add_to_line_ends): user.vscode("editor.action.insertCursorAtEndOfEachLineSelected")
action(user.multi_cursor_disable): key(escape)
action(user.multi_cursor_enable): skip()
action(user.multi_cursor_select_all_occurrences): user.vscode("editor.action.selectHighlights")
action(user.multi_cursor_select_fewer_occurrences): user.vscode("cursorUndo")
action(user.multi_cursor_select_more_occurrences): user.vscode("editor.action.addSelectionToNextFindMatch")
#multiple_cursor.py support end

please [<user.text>]$: 
  user.vscode("workbench.action.showCommands")
  insert(user.text or "")

# Sidebar

# what is the difference with workbench.view.explorer vs action.focusFilesExplorer?
[go] explore: user.vscode("workbench.view.explorer")
focus explore: user.vscode("workbench.files.action.focusFilesExplorer")
bar extensions: user.vscode("workbench.view.extensions")
[go] outline: user.vscode("outline.focus")
go debug: user.vscode("workbench.view.debug")

go git: user.vscode("workbench.view.scm")
bar switch: user.vscode("workbench.action.toggleSidebarVisibility")

# show recent: user.vscode("work55bench.action.showAllEditorsByMostRecentlyUsed")
go search [<user.text>]$: 
    user.vscode("workbench.action.findInFiles")
    sleep(50ms)
    insert(text or "")
    
go find [<user.word>]$: 
    user.vscode("actions.find")
    sleep(50ms)
    insert(word or "")

go replace: user.vscode("editor.action.startFindReplaceAction")
    
go symbol [<user.text>]$:
  user.vscode("workbench.action.gotoSymbol")
  sleep(50ms)
  insert(text or "")

search symbol [<user.text>]$:
  user.vscode("workbench.action.showAllSymbols")
  sleep(50ms)
  insert(text or "")

# Panels
panel debug: user.vscode("workbench.panel.repl.view.focus")
panel output: user.vscode("workbench.panel.output.focus")
panel problems: user.vscode("workbench.panel.markers.view.focus")
panel switch: user.vscode("workbench.action.togglePanel")
panel terminal: user.vscode("workbench.panel.terminal.focus")
panel close: user.vscode("workbench.action.closePanel")

console: user.vscode("workbench.action.terminal.toggleTerminal")
deploy:
    user.vscode("workbench.action.terminal.toggleTerminal")
    sleep(150ms)
    key("ctrl-c")
    insert("task deploy\n")

# terminal: user.vscode("workbench.action.terminal.toggleTerminal")
# toggle terminal: user.vscode("workbench.action.terminal.toggleTerminal")

go editor: user.vscode("workbench.action.focusActiveEditorGroup")
group one: user.vscode("workbench.action.focusFirstEditorGroup")
group two: user.vscode("workbench.action.focusSecondEditorGroup")

focus side: user.vscode("workbench.action.focusSideBar")

# focus editor: user.vscode("workbench.action.focusActiveEditorGroup")

# Settings
go settings ui: user.vscode("workbench.action.openGlobalSettings")
go settings: user.vscode("workbench.action.openSettingsJson")
default settings: user.vscode("workbench.action.openRawDefaultSettings")
go shortcuts: user.vscode("workbench.action.openGlobalKeybindings")
go snippets: user.vscode("editing-snippets-by-yaml.configureUserSnippets")

# Displaythe.minnow
centered switch: user.vscode("workbench.action.toggleCenteredLayout")
fullscreen switch: user.vscode("workbench.action.toggleFullScreen")
theme switch: user.vscode("workbench.action.selectTheme")
wrap switch: user.vscode("editor.action.toggleWordWrap")
zen switch: user.vscode("workbench.action.toggleZenMode")

# File Commands
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
lion [<user.text>]:  
  user.vscode("workbench.action.quickOpen")
  sleep(50ms)
  insert(text or "")

file duplicate: user.vscode("fileutils.duplicateFile")
file copy path: user.vscode("copyFilePath") 
file copy relative: user.vscode("copyRelativeFilePath") 
file copy link: user.vscode("gitlens.copyRemoteFileUrlToClipboard") 
file create sibiling: user.vscode_and_wait("fileutils.newFile")
file new: user.vscode_and_wait("explorer.newFile")
folder new: user.vscode_and_wait("explorer.newFolder")
file create: user.vscode("workbench.action.files.newUntitledFile")
# Why do I have  all this sleeps here
file rename:
    user.vscode("fileutils.renameFile")
	sleep(150ms)
file move:
	user.vscode("fileutils.moveFile")
	sleep(150ms)
file remove:
    user.vscode("fileutils.removeFile")    
file open folder: user.vscode("revealFileInOS")
(file reveal|show in tree): user.vscode("workbench.files.action.showActiveFileInExplorer") 
save ugly: user.vscode("workbench.action.files.saveWithoutFormatting")

# Language Features
sense [<user.word>] : 
    insert(user.word or "")
    sleep(10ms)
    user.vscode("editor.action.triggerSuggest")

hint: user.vscode("editor.action.triggerParameterHints")

(show|bishop|def show|dev show): user.vscode("editor.action.revealDefinition")


(peek|def peek): user.vscode("editor.action.peekDefinition") 
# refs peek: user.vscode("editor.action.referenceSearch.trigger") 

(dev side|def side): user.vscode("editor.action.revealDefinitionAside")
type show: user.vscode("editor.action.peekTypeDefinition")
refs: user.vscode("editor.action.goToReferences")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# open side: user.vscode("search.action.openResultToSide")
open side: key(ctrl-enter)
format that: user.vscode("editor.action.formatDocument") 
format selection: user.vscode("editor.action.formatSelection")
imports fix: user.vscode("editor.action.organizeImports")
problem next: user.vscode("editor.action.marker.nextInFiles")
problem last: user.vscode("editor.action.marker.prevInFiles")
problem fix: user.vscode("problems.action.showQuickFixes")
rename that: user.vscode("editor.action.rename")


whitespace trim: user.vscode("editor.action.trimTrailingWhitespace")
language switch: user.vscode("workbench.action.editor.changeLanguageMode")

refactor (this|that): user.vscode("editor.action.refactor")


#code navigation
# (go declaration | follow): user.vscode("editor.action.revealDefinition")
go back: user.vscode("workbench.action.navigateBack") 
go forward:  user.vscode("workbench.action.navigateForward")  
go implementation: user.vscode("editor.action.goToImplementation")
go type: user.vscode("editor.action.goToTypeDefinition")
go usage: user.vscode("references-view.find")
folder open: user.vscode("workbench.action.files.openFileFolder")


# It will show  folders  to open,  not recent open files.
go recent [<user.text>]: 
  user.vscode("workbench.action.openRecent")
  sleep(50ms)
  insert(text or "")
  sleep(250ms)

# Bookmarks. Requires Bookmarks plugin
# go marks: user.vscode("workbench.view.extension.bookmarks")
# toggle mark: user.vscode("bookmarks.toggle")
# go next mark: user.vscode("bookmarks.jumpToNext")
# go last mark: user.vscode("bookmarks.jumpToPrevious")

# Folding
# fold that: user.vscode("editor.fold")
# unfold that: user.vscode("editor.unfold")
# fold those: user.vscode("editor.foldAllMarkerRegions")
# unfold those: user.vscode("editor.unfoldRecursively")
# fold all: user.vscode("editor.foldAll")
# unfold all: user.vscode("editor.unfoldAll")
# fold comments: user.vscode("editor.foldAllBlockComments")

# Git / Github (not using verb-noun-adjective pattern, mirroring terminal commands.)
lense branches: user.vscode("gitlens.showBranchesView")
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
git commit amend: user.vscode("git.commitStagedAmend")
git diff: user.vscode("git.openChange")
(git discard|go discard): user.vscode("git.clean")
git discard all: user.vscode("git.cleanAll")
git ignore: user.vscode("git.ignore")
git merge: user.vscode("git.merge")
git output: user.vscode("git.showOutput")
git pull: user.vscode("git.pullRebase")
git push: user.vscode("git.push")
git push focus: user.vscode("git.pushForce")
git rebase: user.vscode("git.rebase")
git fetch all: user.vscode("git.fetchAll")
git rebase abort: user.vscode("git.rebaseAbort")
git reveal: user.vscode("git.revealInExplorer")
git revert: user.vscode("git.revertChange")
revert range: user.vscode("git.revertSelectedRanges")
git stash: user.vscode("git.stash")
git stash pop: user.vscode("git.stashPop")
git status: user.vscode("workbench.scm.focus")
(git stage|stage this): user.vscode("git.stage")
# git stage all: user.vscode("git.stageAll")
git unstage: user.vscode("git.unstage")
git unstage all: user.vscode("git.unstageAll")
pull request: user.vscode("pr.create")
change next: key(alt-f5)
change last: key(shift-alt-f5)

#Debugging
break point remove all: user.vscode("workbench.debug.viewlet.action.removeAllBreakpoints")
break point: user.vscode("editor.debug.action.toggleBreakpoint")
step over: user.vscode("workbench.action.debug.stepOver")
debug step into: user.vscode("workbench.action.debug.stepInto")
debug step out [of]: user.vscode("workbench.action.debug.stepOut")
debug start: user.vscode("workbench.action.debug.start")
debug pause: user.vscode("workbench.action.debug.pause")
debug stop: user.vscode("workbench.action.debug.stop")
debug continue: user.vscode("workbench.action.debug.continue")
debug restart: user.vscode("workbench.action.debug.restart")
debug console: user.vscode("workbench.debug.action.toggleRepl")

# Terminal
terminal external: user.vscode("workbench.action.terminal.openNativeConsole")
terminal new: user.vscode("workbench.action.terminal.new")
terminal next: user.vscode("workbench.action.terminal.focusNext")
terminal last:user.vscode("workbench.action.terminal.focusPrevious")
terminal split: user.vscode("workbench.action.terminal.split")
terminal zoom: user.vscode("workbench.action.toggleMaximizedPanel")
terminal trash: user.vscode("workbench.action.terminal.kill")
terminal toggle: user.vscode_and_wait("workbench.action.terminal.toggleTerminal")
terminal scroll up: user.vscode("workbench.action.terminal.scrollUp")
terminal scroll down: user.vscode("workbench.action.terminal.scrollDown")
terminal <number_small>: user.vscode_terminal(number_small)

#TODO: should this be added to linecommands?
copy line down: user.vscode("editor.action.copyLinesDownAction") 
copy line up: user.vscode("editor.action.copyLinesUpAction") 

#Expand/Shrink AST Selection
select less: user.vscode("editor.action.smartSelect.shrink")
select (more|this): user.vscode("editor.action.smartSelect.expand")
# tina: user.vscode("editor.action.smartSelect.expand")


minimap: user.vscode("editor.action.toggleMinimap")
maximize: user.vscode("workbench.action.minimizeOtherEditors")
restore: user.vscode("workbench.action.evenEditorWidths")
keep editor: user.vscode("workbench.action.keepEditor")
replace here:
	user.replace("")
	key(cmd-alt-l)

hover [show]: user.vscode("editor.action.showHover")

join lines: user.vscode("editor.action.joinLines")

full screen: user.vscode("workbench.action.toggleFullScreen")

curse undo: user.vscode("cursorUndo")

select word: user.vscode("editor.action.addSelectionToNextFindMatch")
skip word: user.vscode("editor.action.moveSelectionToNextFindMatch")

# jupyter   
# cell next: user.vscode("jupyter.gotoNextCellInFile")
# cell last: user.vscode("jupyter.gotoPrevCellInFile")
# cell run above: user.vscode("jupyter.runallcellsabove.palette")
# cell run: user.vscode("jupyter.runcurrentcell")

install local: user.vscode("workbench.extensions.action.installVSIX")

comment: code.toggle_comment()  


close everything: user.vscode("workbench.action.closeAllGroups")
close others: user.vscode("workbench.action.closeOtherEditors") 
close all others: 
    user.vscode("workbench.action.closeOtherEditors") 
    user.vscode("workbench.action.closeEditorsInOtherGroups")

# move editor
move left: user.vscode("workbench.action.moveEditorLeftInGroup")
move right: user.vscode("workbench.action.moveEditorRightInGroup")

move last: user.vscode("workbench.action.moveEditorToPreviousGroup")
move next: user.vscode("workbench.action.moveEditorToNextGroup")
   
focus group: user.vscode("workbench.action.toggleEditorWidths")
close group: user.vscode("workbench.action.closeEditorsInGroup")
one group: user.vscode("workbench.action.closeEditorsInOtherGroups")
group next: user.vscode("workbench.action.focusNextGroup")
group last: user.vscode("workbench.action.focusPreviousGroup")

# next: app.tab_next()
# last: app.tab_previous()

# copied from line_commands.talon
go <number>: edit.jump_line(number)
go <number> end: 
    edit.jump_line(number)
    edit.line_end()

lend: edit.line_end()
bend: edit.line_start()
take <number> line:
    user.select_next_lines(number)

cut <number> line:
    user.select_next_lines(number)
    sleep(10ms)
    key(cmd-x)

copy <number> line:
    user.select_next_lines(number)
    key(cmd-c)
    sleep(100ms)
    key(esc)

clone <number> line:
        user.select_next_lines(number)
        key(cmd-c)
        sleep(10ms)
        key(right cmd-v)
        
indent <number> line:
    user.select_next_lines(number)
    edit.indent_more()
    
dis dent <number> line:
    user.select_next_lines(number)
    edit.indent_less()
    
comment <number> line:
    user.select_next_lines(number)
    sleep(10ms)
    user.vscode("editor.action.commentLine")   
            
clone that:
    key(cmd-c)
    sleep(10ms)
    key(right enter cmd-v)

(clear|wipe) <number> line:
        user.select_next_lines(number)
        key(delete)

    
# is it better to use vscode commands or just keyboard shortcuts?
# Or I could hide these details and create talon actions and only call these here.
take this$:
    key(cmd-d)  

search this$:
    key(cmd-d)     
    key(cmd-shift-f) 
    key(enter)
find this$:
    key(cmd-d)     
    key(cmd-f) 
    key(enter)
folders collapse:
    user.vscode("workbench.files.action.collapseExplorerFolders")
fix this: user.vscode("editor.action.quickFix")
justify:
    key(up end)
    insert("\n")
cursorless record: user.vscode("cursorless.recordTestCase")    

code time dashboard: user.vscode("codetime.viewDashboard")
index: 
    insert("[]")
    key(left)
call this: 
    insert("()")
    key(left)
    