# Microsoft - Visual Studio Code
# see app/vscode.talon for voice commands
os: windows
app: Visual Studio Code
app: Code.exe
-
tag(): ide
# General
action(user.ide_command_palette):
  key(ctrl-shift-p)
action(edit.indent_less):
  key(ctrl-[)
action(edit.indent_more):
  key(ctrl-])
action(app.tab_next):
  key(ctrl-k)
  key(ctrl-pagedown)
action(app.tab_previous):
  key(ctrl-k)
  key(ctrl-pageup)
# Folding
action(user.ide_expand_deep):
  key(ctrl-k ctrl-])
action(user.ide_expand_all):
  key(ctrl-k ctrl-j)
action(user.ide_expand_region):
  key(ctrl-shift-])
action(user.ide_collapse_deep):
  key(ctrl-k ctrl-[)
action(user.ide_collapse_all):
  key(ctrl-k ctrl-0)
action(user.ide_collapse_region):
  key(ctrl-shift-[)

# Splits
action(user.ide_split_right):
  user.ide_command_palette()
  insert("workbench.action.splitEditorRight")
  key(enter)

action(user.ide_split_left):
  user.ide_command_palette()
  insert("workbench.action.splitEditorLeft")
  key(enter)

action(user.ide_split_up):
  user.ide_command_palette()
  insert("workbench.action.splitEditorUp")
  key(enter)

action(user.ide_split_down):
  user.ide_command_palette()
  insert("workbench.action.splitEditorDown")
  key(enter)

#Refactor

action(user.ide_refactor): key(ctrl-shift-r)
action(user.ide_refactor_in_line): key(ctrl-shift-r)
action(user.ide_refactor_rename): key(f2)
action(user.ide_fix_format): 
  # Format Document
  key(alt-shift-f)
# Navigate
action(user.ide_follow):
  # Go to Definition
  key(f12)

action(user.ide_go_back):  key(alt-left)
action(user.ide_go_forward): key(alt-right)
action(user.ide_recent): key(ctrl-r)

#there is no separate "mode" for VSCode
#action(user.ide_multi_cursor): skip()
action(user.ide_multi_cursor_stop): key(escape)
action(user.ide_up_cursor):key(ctrl-alt-up)
action(user.ide_down_cursor): key(ctrl-alt-down)
action(user.ide_multi_select_more): key(ctrl-d)
action(user.ide_multi_select_all): key(ctrl-shift-l)

action(user.ide_select_less): key(shift-alt-left)
action(user.ide_select_more): key(shift-alt-right)

# Terminal
action(user.ide_toggle_terminal):
  # View:Toggle Integrated Terminal
  key(ctrl-`)

action(user.ide_terminal_new):
  # Terminal: Created New Integrated Terminal
  key(ctrl-shift-`)

action(user.ide_terminal_focus_previous):
  user.ide_command_palette()
  insert("Terminal:Focus Previous Terminal")
  key(enter)

action(user.ide_terminal_focus_next):
  user.ide_command_palette()
  insert("Terminal:Focus Next Terminal")
  key(enter)

action(user.ide_terminal_trash):
  user.ide_command_palette()
  insert("Terminal:Kill")
  key(enter)

action(user.ide_terminal_scroll_down):
  key(pgdown)

action(user.ide_terminal_scroll_up):
  key(pgup)

# Code Editor
action(user.ide_toggle_comment):
  key(ctrl-/)

action(user.ide_smart):
  # Trigger Suggest, editor.action.triggerParameterHints
  key(ctrl-space)

action(user.ide_intellisense_suggest_parameters):
  key(ctrl-shift-space)

action(user.ide_done):
  key(tab)

# Editing
action(user.ide_editor_copylines_down):
  # Copy Line Down, editor.action.copyLinesDownAction
  key(shift-alt-down)

action(user.ide_editor_copylines_up):
    # Copy Line Up, editor.action.copyLinesUpAction
    key(shift-alt-up)


# Workbench Focus Areas
action(user.ide_toggle_project):
  # View: Show Explorer, workbench.view.explorer
  key(ctrl-shift-e)
                  
action(user.ide_toggle_git):
  # View: Show SCM, workbench.view.scm
  key(ctrl-shift-g)

action(user.ide_toggle_extensions):
  # View: Show Extensions, workbench.view.extensions
  key(ctrl-shift-x)

action(user.ide_toggle_status_bar):
  user.ide_command_palette()
  insert("View: Toggle Status Bar Visibility")
  key(enter)

action(user.ide_toggle_run):
  # View: Show Run and Debug, workbench.view.debug
  key(ctrl-shift-d)
action(user.ide_toggle_debug):
  # View: Show Run and Debug, workbench.view.debug
  key(ctrl-shift-d)

# Find and Replace
action(user.ide_toggle_find):
  # Search: Find in Files, workbench.action.findInFiles
  key(ctrl-shift-f)
action(user.ide_find_everywhere):
  # Search: Find in Files, workbench.action.findInFiles
  key(ctrl-shift-f)
action(user.ide_replace_everywhere):
  # Search: Replace in Files, workbench.action.replaceInFiles
  key(ctrl-shift-h)

action(user.ide_replace_local):
  # Replace, editor.action.startFindReplaceAction
  key(ctrl-h)
action(user.ide_replace_confirm_current):
  # ,editor.action.replaceOne
  key(ctrl-shift-1)
action(user.ide_replace_confirm_all):
  # ,editor.action.replaceAll
  key(ctrl-alt-enter)

action(user.ide_find_match_by_case):
  # Terminal: Toggle Find Using Case Sensitive, workbench.action.terminal.toggleFindCaseSensitive
  key(alt-c)
action(user.ide_find_match_by_word):
  # Terminal: Toggle Find Using Whole Word, toggleFindWholeWord
  key(alt-w)
action(user.ide_find_match_by_regex):
  # Terminal: Toggle Find Using Regex, workbench.action.terminal.toggleFindRegex
  key(alt-r)



action(user.ide_toggle_breakpoint):
  # Debug: Toggle Breakpoint, editor.debug.action.toggleBreakpoint
  key(f9)
action(user.ide_step_over):
  # Debug: Step Over, workbench.action.debug.stepOver
  key(f10)
action(user.ide_step_into):
  # Debug: Step Into, workbench.action.debug.stepInto
  key(f11)
action(user.ide_step_out):
  # Debug: Step Out, workbench.action.debug.stepOut
  key(shift-f11)

# Window and File Management
action(app.window_open):
  # New Window, workbench.action.newWindow
  key(ctrl-shift-n)

action(user.ide_create_file):
  # File: New and Titled File, workbench.action.files.newUntitledFile
  key(ctrl-n)

action(user.ide_reveal_in_file_manager):
  # , workbench.action.files.revealActiveFileInWindows
  key(ctrl-k r)

action(user.ide_find_file):
  # Go to File... , workbench.action.quickOpen
  key(ctrl-p)

#tabs 
action(user.ide_go_first_tab): key(alt-1)
action(user.ide_go_second_tab): key(alt-2)
action(user.ide_go_third_tab): key(alt-3)
action(user.ide_go_fourth_tab): key(alt-4)
action(user.ide_go_fifth_tab): key(alt-5)
action(user.ide_go_sixth_tab): key(alt-6)
action(user.ide_go_seventh_tab): key(alt-7)
action(user.ide_go_eighth_tab): key(alt-8)
action(user.ide_go_ninth_tab): key(alt-9)