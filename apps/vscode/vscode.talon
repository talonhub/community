#custom vscode commands go here
app: vscode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.splits
tag(): user.tabs
tag(): user.git
tag(): terminal

console log:
  "console.log(\"\");"
  key(left)
  key(left)
  key(left)

use effect log:
  "useEffect(()=> {"
  key(return)
  "console.log(thing);"
  key(return)
  "},[thing])"

log template:
  "console.log(\"thing\", thing);"

log object:
  "console.log({});"
  key(left)
  key(left)
  key(left)

toggle vim:
  key(cmd-i)
  key(cmd-v)

quick docks:
  key(cmd-k)
  key(cmd-i)

arrow funk:
    "() => {}"
    sleep(30ms)
    key(left)
    key(enter)

arrow short:
    "() => "

comment: key(cmd-/)

toggle hats:
  user.vscode("workbench.action.showCommands")
  insert("Cursorless: Toggle Decorations")
  key(enter)

doc string:
  "/** "

findy:
  key(cmd-f)

find all:
  key(cmd-shift-f)

node run (start | dev | development):
  "npm run dev"
  key(enter)

node run test:
  "npm run test"
  key(enter)

node run build:
  "npm run build"
  key(enter)

node run test watch:
  "npm run test:watch"
  key(enter)

node run test integration:
  "npm run test:integration:watch"
  key(enter)

node run test unit:
  "npm run test:unit:watch"
  key(enter)

node run storybook:
  "npm run storybook"
  key(enter)

node install:
  "npm i"
  key(enter)

node install all:
  "npm run install-all"
  key(enter)

close:
  key(escape)
  sleep(20ms)
  edit.line_end()
  insert(";")

use node fourteen:
  "nvm use 14.19.0"
  key(enter)

use node eighteen:
  "nvm use 18.16.1"
  key(enter)

#talon app actions
action(app.tab_close): user.vscode("workbench.action.closeActiveEditor")
action(app.tab_next): user.vscode("workbench.action.nextEditorInGroup")
action(app.tab_previous): user.vscode("workbench.action.previousEditorInGroup")
action(app.tab_reopen): user.vscode("workbench.action.reopenClosedEditor")
action(app.window_close): user.vscode("workbench.action.closeWindow")
action(app.window_open): user.vscode("workbench.action.newWindow")

#talon code actions
action(code.toggle_comment): user.vscode("editor.action.commentLine")

#talon edit actions
action(edit.indent_more): user.vscode("editor.action.indentLines")
action(edit.indent_less): user.vscode("editor.action.outdentLines")
action(edit.save_all): user.vscode("workbench.action.files.saveAll")

# splits.py support begin
action(user.split_clear_all): user.vscode("View: Single Column Editor Layout")
action(user.split_clear): user.vscode("View: Join Editor Group with Next Group")
action(user.split_flip): user.vscode("View: Toggle Vertical/Horizontal Editor Layout")
action(user.split_last): user.vscode("View: Focus Previous Editor Group")
action(user.split_next):  user.vscode("View: Focus Next Editor Group")
action(user.split_window_down): user.vscode("workbench.action.moveEditorToBelowGroup")
action(user.split_window_horizontally): user.vscode("View: Split Editor Orthogonal")
action(user.split_window_left): user.vscode("workbench.action.moveEditorToLeftGroup")
action(user.split_window_right): user.vscode("workbench.action.moveEditorToRightGroup")
action(user.split_window_up): user.vscode("workbench.action.moveEditorToAboveGroup")
action(user.split_window_vertically): user.vscode("View: Split Editor")
action(user.split_window): user.vscode("View: Split Editor")
# splits.py support end

#multiple_cursor.py support begin
#note: vscode has no explicit mode for multiple cursors
action(user.multi_cursor_add_above): user.vscode("Add Cursor Above")
action(user.multi_cursor_add_below): user.vscode("Add Cursor Below")
action(user.multi_cursor_add_to_line_ends): user.vscode("Add Cursor to Line Ends")
action(user.multi_cursor_disable): key(escape)
action(user.multi_cursor_enable): skip()
action(user.multi_cursor_select_all_occurrences): user.vscode("Select All Occurrences of Find Match")
action(user.multi_cursor_select_fewer_occurrences): user.vscode("Cursor Undo")
action(user.multi_cursor_select_more_occurrences): user.vscode("Add Selection To Next Find Match")
#multiple_cursor.py support end

please [<user.text>]:
    user.vscode("workbench.action.showCommands")
    insert(user.text or "")

go view [<user.text>]:
    user.vscode("workbench.action.openView")
    insert(user.text or "")

# Copilot
bar chat: user.vscode("workbench.panel.chat.view.copilot.focus")
chat new: user.vscode("workbench.action.chat.clear")
chat inline: user.vscode("inlineChat.start")
toggle copilot: user.vscode("github.copilot.toggleCopilot")
chat quick: user.vscode("workbench.action.openQuickChat.copilot")

# Sidebar
bar files: user.vscode("workbench.view.explorer")
bar extensions: user.vscode("workbench.view.extensions")
bar outline: user.vscode("outline.focus")
bar debug: user.vscode("workbench.view.debug")
bar search: user.vscode("workbench.view.search")
bar source: user.vscode("workbench.view.scm")
bar test: user.vscode("workbench.view.testing.focus")
bar switch: user.vscode("workbench.action.toggleSidebarVisibility")

# Symbol search
symbol hunt [<user.text>]:
    user.vscode("workbench.action.gotoSymbol")
    sleep(50ms)
    insert(text or "")

symbol hunt all [<user.text>]:
    user.vscode("workbench.action.showAllSymbols")
    sleep(50ms)
    insert(text or "")

# Panels
panel control: user.vscode("workbench.panel.repl.view.focus")
panel output: user.vscode("workbench.panel.output.focus")
panel problems: user.vscode("workbench.panel.markers.view.focus")
panel switch: user.vscode("workbench.action.togglePanel")
panel terminal: user.vscode("workbench.action.terminal.focus")
focus editor: user.vscode("workbench.action.focusActiveEditorGroup")

# Settings
show settings: user.vscode("workbench.action.openGlobalSettings")
show settings json: user.vscode("workbench.action.openSettingsJson")
show settings folder: user.vscode("workbench.action.openFolderSettings")
show settings folder json: user.vscode("workbench.action.openFolderSettingsFile")
show settings workspace: user.vscode("workbench.action.openWorkspaceSettings")
show settings workspace json: user.vscode("workbench.action.openWorkspaceSettingsFile")
show shortcuts: user.vscode("workbench.action.openGlobalKeybindings")
show shortcuts json: user.vscode("workbench.action.openGlobalKeybindingsFile")
show snippets: user.vscode("workbench.action.openSnippets")

# VSCode Snippets
snip (last | previous): user.vscode("jumpToPrevSnippetPlaceholder")
snip next: user.vscode("jumpToNextSnippetPlaceholder")

# Display
centered switch: user.vscode("workbench.action.toggleCenteredLayout")
fullscreen switch: user.vscode("workbench.action.toggleFullScreen")
theme switch: user.vscode("workbench.action.selectTheme")
# wrap switch: user.vscode("editor.action.toggleWordWrap")
zen switch: user.vscode("workbench.action.toggleZenMode")

# File Commands
search files [<user.text>]:
    user.vscode("workbench.action.quickOpen")
    sleep(50ms)
    insert(text or "")
file hunt (pace | paste):
    user.vscode("workbench.action.quickOpen")
    sleep(50ms)
    edit.paste()
file copy name: user.vscode("fileutils.copyFileName")
file copy path: user.vscode("copyFilePath")
file copy local [path]: user.vscode("copyRelativeFilePath")
file create sibling: user.vscode_and_wait("explorer.newFile")
file create: user.vscode("workbench.action.files.newUntitledFile")
file create relative: user.vscode("fileutils.newFile")
file create root: user.vscode("fileutils.newFileAtRoot")
file rename:
    user.vscode("fileutils.renameFile")
    sleep(150ms)
file move:
    user.vscode("fileutils.moveFile")
    sleep(150ms)
file clone:
    user.vscode("fileutils.duplicateFile")
    sleep(150ms)
file delete:
    user.vscode("fileutils.removeFile")
    sleep(150ms)
file open folder: user.vscode("revealFileInOS")
file reveal: user.vscode("workbench.files.action.showActiveFileInExplorer")
save ugly: user.vscode("workbench.action.files.saveWithoutFormatting")
save all: user.vscode("workbench.action.files.saveAll")

# Language Features
suggest show: user.vscode("editor.action.triggerSuggest")
hint show: user.vscode("editor.action.triggerParameterHints")
definition show: user.vscode("editor.action.revealDefinition")
definition peek: user.vscode("editor.action.peekDefinition")
define aside: user.vscode("editor.action.revealDefinitionAside")
references show: user.vscode("editor.action.goToReferences")
hierarchy peek: user.vscode("editor.showCallHierarchy")
references find: user.vscode("references-view.find")
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

#code navigation
#(go declaration | follow): user.vscode("Go to Declaration")
#go back: user.vscode("workbench.action.navigateBack")
#go forward:  user.vscode("workbench.action.navigateForward")
#go implementation: user.vscode("Go to Implementation")
#go recent: user.vscode("File: Open Recent")
#go type: user.vscode("editor.action.goToTypeDefinition")
go type: user.vscode("editor.action.goToTypeDefinition")
go usage: user.vscode("references-view.find")
go recent [<user.text>]:
    user.vscode("workbench.action.openRecent")
    sleep(50ms)
    insert(text or "")
    sleep(250ms)
go edit: user.vscode("workbench.action.navigateToLastEditLocation")

#go usage: user.vscode("References: Find All References")

# Bookmarks. Requires Bookmarks plugin
bar marks: user.vscode("workbench.view.extension.bookmarks")
go marks:
    user.deprecate_command("2023-06-06", "go marks", "bar marks")
    user.vscode("workbench.view.extension.bookmarks")
toggle mark: user.vscode("bookmarks.toggle")
go next mark: user.vscode("bookmarks.jumpToNext")
go last mark: user.vscode("bookmarks.jumpToPrevious")
mark label: user.vscode("bookmarks.toggleLabeled")

close other tabs: user.vscode("workbench.action.closeOtherEditors")
close all tabs: user.vscode("workbench.action.closeAllEditors")
close tabs right: user.vscode("workbench.action.closeEditorsToTheRight")
close tabs left: user.vscode("workbench.action.closeEditorsToTheLeft")
tab close: user.vscode("workbench.action.closeActiveEditor")

# Folding
fold that: user.vscode("editor.fold")
unfold that: user.vscode("editor.unfold")
fold those: user.vscode("editor.foldAllMarkerRegions")
unfold those: user.vscode("editor.unfoldRecursively")
fold all: user.vscode("editor.foldAll")
unfold all: user.vscode("editor.unfoldAll")
fold comments: user.vscode("editor.foldAllBlockComments")
fold level one: user.vscode("editor.foldLevel1")
fold level two: user.vscode("editor.foldLevel2")
fold level three: user.vscode("editor.foldLevel3")
fold level four: user.vscode("editor.foldLevel4")
unfold level four: user.vscode("editor.unfoldLevel4")
fold level five: user.vscode("editor.foldLevel5")
fold level six: user.vscode("editor.foldLevel6")
fold level seven: user.vscode("editor.foldLevel7")



# git status:
  # "git status"
  # key(enter)

# git fetch:
  # "git fetch"
  # key(enter)

# git pull:
  # "git pull"
  # key(enter)

# git checkout:
  # "git checkout "

# git commit all:
  # "git commit -am \""

# git branch:
  # "git checkout -b "

# git push:
  # "git push"


# git set upstream:
  # "git branch --set-upstream-to=origin/"


# git add all:
  # "git add ."
  # key(enter)

# git commit:
  # "git commit -m \""


# git log:
  # "git log --oneline"
  # key(enter)

# git push origin head:
  # "git push origin head"

# git stash:
  # "git stash"

# git stash apply:
  # "git stash apply"

# git clone:
  # "git clone "

# git change name:
  # "git config user.name "

# git change email:
  # "git config user.email "

# Git / Github (not using verb-noun-adjective pattern, mirroring terminal commands.) 
git branch: user.vscode("git.branchFrom")
git branch this: user.vscode("git.branch")
git checkout: user.vscode("git.checkout")
git commit [<user.text>]:
    user.vscode("git.commitStaged")
    sleep(100ms)
    user.insert_formatted(text or "", "CAPITALIZE_FIRST_WORD")
git commit undo: user.vscode("git.undoCommit")
# git commit amend: user.vscode("git.commitStagedAmend")
git diff: user.vscode("git.openChange")
git fetch: user.vscode("git.fetch")
git fetch all: user.vscode("git.fetchAll")
git ignore: user.vscode("git.ignore")
# git merge: user.vscode("git.merge")
git output: user.vscode("git.showOutput")
git pull: user.vscode("git.pullRebase")
git push: user.vscode("git.push")
# git push focus: user.vscode("git.pushForce")
# git rebase abort: user.vscode("git.rebaseAbort")
git reveal: user.vscode("git.revealInExplorer")
# git revert: user.vscode("git.revertChange")
git stash: user.vscode("git.stash")
git stash pop: user.vscode("git.stashPop")
git status: user.vscode("workbench.scm.focus")
git stage: user.vscode("git.stage")
git stage all: user.vscode("git.stageAll")
git sync: user.vscode("git.sync")
git unstage: user.vscode("git.unstage")
git unstage all: user.vscode("git.unstageAll")
pull request: user.vscode("pr.create")
# Use keyboard shortcuts because VSCode relies on when clause contexts to choose the appropriate
# action: https://code.visualstudio.com/api/references/when-clause-contexts
change next: key(alt-f5)
change last: key(shift-alt-f5)

# Testing
test run: user.vscode("testing.runAtCursor")
test run file: user.vscode("testing.runCurrentFile")
test run all: user.vscode("testing.runAll")
test run failed: user.vscode("testing.reRunFailTests")
test run last: user.vscode("testing.reRunLastRun")

test debug: user.vscode("testing.debugAtCursor")
test debug file: user.vscode("testing.debugCurrentFile")
test debug all: user.vscode("testing.debugAll")
test debug failed: user.vscode("testing.debugFailTests")
test debug last: user.vscode("testing.debugLastRun")

test cancel: user.vscode("testing.cancelRun")

# Debugging
break point: user.vscode("editor.debug.action.toggleBreakpoint")
debug step over: user.vscode("workbench.action.debug.stepOver")
debug step into: user.vscode("workbench.action.debug.stepInto")
debug step out [of]: user.vscode("workbench.action.debug.stepOut")
debug start: user.vscode("workbench.action.debug.start")
debug pause: user.vscode("workbench.action.debug.pause")
debug stopper: user.vscode("workbench.action.debug.stop")
debug continue: user.vscode("workbench.action.debug.continue")
debug restart: user.vscode("workbench.action.debug.restart")
debug console: user.vscode("workbench.debug.action.toggleRepl")
debug clean: user.vscode("workbench.debug.panel.action.clearReplAction")

# Terminal
terminal external: user.vscode("workbench.action.terminal.openNativeConsole")
terminal new: user.vscode("workbench.action.terminal.new")
terminal next: user.vscode("workbench.action.terminal.focusNext")
terminal last: user.vscode("workbench.action.terminal.focusPrevious")
terminal split: user.vscode("workbench.action.terminal.split")
terminal zoom: user.vscode("workbench.action.toggleMaximizedPanel")
terminal trash: user.vscode("workbench.action.terminal.kill")
toggle terminal : user.vscode_and_wait("workbench.action.terminal.toggleTerminal")
terminal scroll up: user.vscode("workbench.action.terminal.scrollUp")
terminal scroll down: user.vscode("workbench.action.terminal.scrollDown")
terminal <number_small>: user.vscode_terminal(number_small)

task run [<user.text>]:
    user.vscode("workbench.action.tasks.runTask")
    insert(user.text or "")
#TODO: should this be added to linecommands?
(copy line down | shingles): user.vscode("editor.action.copyLinesDownAction")
copy line up: user.vscode("editor.action.copyLinesUpAction")

#Expand/Shrink AST Selection
select less: user.vscode("editor.action.smartSelect.shrink")
select (more | this): user.vscode("editor.action.smartSelect.expand")

minimap: user.vscode("editor.action.toggleMinimap")
maximize: user.vscode("workbench.action.minimizeOtherEditors")
restore: user.vscode("workbench.action.evenEditorWidths")

#breadcrumb
select breadcrumb: user.vscode("breadcrumbs.focusAndSelect")
# Use `alt-left` and `alt-right` to navigate the bread crumb

replace here:
    user.replace("")
    key(cmd-alt-l)

hover show: user.vscode("editor.action.showHover")

join lines: user.vscode("editor.action.joinLines")

full screen: user.vscode("workbench.action.toggleFullScreen")

curse undo: user.vscode("cursorUndo")
curse redo: user.vscode("cursorRedo")

select word: user.vscode("editor.action.addSelectionToNextFindMatch")
skip word: user.vscode("editor.action.moveSelectionToNextFindMatch")

# jupyter
cell next: user.vscode("notebook.focusNextEditor")
cell last: user.vscode("notebook.focusPreviousEditor")
cell run above: user.vscode("notebook.cell.executeCellsAbove")
cell run: user.vscode("notebook.cell.execute")

install local: user.vscode("workbench.extensions.action.installVSIX")
preview markdown: user.vscode("markdown.showPreview")
