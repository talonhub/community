app: Code
os: mac
-
# TODO When tags are supported
# tag(): ide

# General
action(user.ide_command_palette):
  key(cmd-shift-p)

action(app.tab_next):
  key(cmd-k)
  key(alt-cmd-right)
  
action(app.tab_previous):
    key(cmd-k)
    key(alt-cmd-left)
    
# Folding
action(user.ide_expand_deep):
  key(cmd-k cmd-])
action(user.ide_expand_all):
  key(cmd-k cmd-j)
action(user.ide_expand_region):
  key(alt-cmd-])
action(user.ide_collapse_deep):
  key(cmd-k cmd-[)
action(user.ide_collapse_all):
  key(cmd-k cmd-0)
action(user.ide_collapse_region):
  key(alt-cmd-[)

# Splits
action(user.ide_split_right):
  user.ide_command_palette()
  insert("View: Split Editor Right")
  key(enter)

action(user.ide_split_left):
  user.ide_command_palette()
  insert("View: Split Editor Left")
  key(enter)

action(user.ide_split_up):
  user.ide_command_palette()
  insert("View: Split Editor Up")
  key(enter)

action(user.ide_split_down):
  user.ide_command_palette()
  insert("View: Split Editor Down")
  key(enter)

#Refactor

action(user.ide_refactor):
  key(cmd-a)
  # Format Document
  key(shift-alt-f)
  key(cmd-s) 
action(user.ide_refactor_in_line):
  # Format Document
  key(shift-alt-f)
  #TODO are we happy to save everytime ?
  key(cmd-s) 

action(user.ide_refactor_rename):
  # Rename Symbol
  key(f2)


# Navigate
action(user.ide_follow):
  # Go to Definition
  key(f12)

action(user.ide_go_back):
  key(ctrl-minus)

action(user.ide_go_forward):
  key(ctrl-shift-minus)

action(user.ide_up_cursor):
  # cursorUpSelect
  key(shift-up)

action(user.ide_down_cursor):
  # cursorDownSelect
  key(shift-down)

# Terminal
action(user.ide_toggle_terminal):
  # View:Toggle Integrated Terminal
  key(ctrl-`)

action(user.ide_terminal_new):
  # Terminal: Created New Integrated Terminal
  key(ctrl-shift-`)

action(user.ide_terminal_focus_previous):
  # Terminal: Focus Previous Pane
  key(alt-cmd-left)

action(user.ide_terminal_focus_next):
  # Terminal: Focus Next Pane
  key(alt-cmd-right)

action(user.ide_terminal_trash):
    user.ide_command_palette()
    insert("Terminal:Kill")
    key(enter)
  
action(user.ide_terminal_scroll_down):
  key(shift-pgdown)

action(user.ide_terminal_scroll_up):
  key(shift-pgup)

# Code Editor
action(user.ide_toggle_comment):
  key(cmd-/)

action(user.ide_smart):
  # Trigger Suggest, editor.action.triggerSuggest
  key(ctrl-space)

action(user.ide_intellisense_suggest_parameters):
  # Trigger Parameter Hints, editor.action.triggerParameterHints
  key(shift-cmd-space)

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
  key(shift-cmd-e)

action(user.ide_toggle_git):
  # View: Show SCM, workbench.view.scm
  key(shift-cmd-g)

action(user.ide_toggle_extensions):
  # View: Show Extensions, workbench.view.extensions
  key(shift-cmd-x)


action(user.ide_toggle_run):
  # View: Show Run and Debug, workbench.view.debug
  key(shift-cmd-d)
action(user.ide_toggle_debug):
  # View: Show Run and Debug, workbench.view.debug
  key(shift-cmd-d)

# Find and Replace
action(user.ide_toggle_find):
  # Search: Find in Files, workbench.action.findInFiles
  key(shift-cmd-f)
action(user.ide_find_everywhere):
  # Search: Find in Files, workbench.action.findInFiles
  key(shift-cmd-f)
action(user.ide_replace_everywhere):
  # Search: Replace in Files, workbench.action.replaceInFiles
  key(shift-cmd-h)

action(user.ide_replace_local):
  # Replace, editor.action.startFindReplaceAction
  key(alt-cmd-f)
action(user.ide_replace_confirm_current):
  # ,editor.action.replaceOne
  key(shift-cmd-1)
action(user.ide_replace_confirm_all):
  # ,editor.action.replaceAll
  key(cmd-enter)

action(user.ide_find_match_by_case):
  # Terminal: Toggle Find Using Case Sensitive, workbench.action.terminal.toggleFindCaseSensitive
  key(alt-cmd-c)
action(user.ide_find_match_by_word):
  # Terminal: Toggle Find Using Whole Word, toggleFindWholeWord
  key(alt-cmd-w)
action(user.ide_find_match_by_regex):
  # Terminal: Toggle Find Using Regex, workbench.action.terminal.toggleFindRegex
  key(alt-cmd-r)



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
  key(shift-cmd-n)

action(user.ide_create_file):
  # File: New and Titled File, workbench.action.files.newUntitledFile
  key(cmd-n)

action(user.ide_reveal_in_file_manager):
  # , workbench.action.files.revealActiveFileInWindows
  key(cmd-k r)

action(user.ide_find_file):
  # Go to File... , workbench.action.quickOpen
  key(cmd-p)
