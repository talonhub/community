# Microsoft - Visual Studio Code
# see app/vscode.talon for custom voice commands
# see ide.talon for common voice commands
app: Code
os: mac
-
tag(): ide
# General
action(user.ide_command_palette):
  key(cmd-shift-p)
action(edit.indent_less):
  key(cmd-[)
action(edit.indent_more):
  key(cmd-])
action(app.tab_next):
  key(cmd-k)
  key(alt-cmd-right)
action(app.tab_previous):
  key(cmd-k)
  key(alt-cmd-left)
# Toggleable views
action(user.ide_toggle_fullscreen): 
  user.ide_command_palette()
  insert("View: Toggle Full Screen")
  key(enter)
#action(user.ide_toggle_distraction_free): user.idea("action ToggleDistractionFreeMode")
#action(user.ide_toggle_presentation_mode): user.idea("action TogglePresentationMode")

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
action(user.ide_split_flip): key(alt-cmd-0)
action(user.ide_split_window): key(cmd-\)
action(user.ide_clear_split): user.ide_clear_all_splits()
action(user.ide_clear_all_splits): 
  user.ide_command_palette()
  insert("View: Single Column Editor Layout")
  key(enter)
action(user.ide_go_next_split): key(cmd-k cmd-right)
action(user.ide_go_last_split): key(cmd-k cmd-left)

#Refactor
action(user.ide_refactor):
  key(cmd-shift-r)
action(user.ide_refactor_in_line):
  key(cmd-shift-r)
action(user.ide_refactor_rename):
  # Rename Symbol
  key(f2)
action(user.ide_rename_file): 
  user.ide_command_palette()
  insert("File: Reveal Active File In Side Bar")
  key(enter)
action(user.ide_fix_format): 
    # Format Document
    key(alt-shift-f)
# Navigate
action(user.ide_follow):
  # Go to Definition
  key(f12)

action(user.ide_go_back): key(ctrl-minus)
action(user.ide_go_forward): key(ctrl-shift-minus)
action(user.ide_recent): key(ctrl-r)

action(user.ide_multi_cursor_stop): key(escape)
action(user.ide_up_cursor):key(cmd-alt-up)
action(user.ide_down_cursor): key(cmd-alt-down)
action(user.ide_multi_select_more): key(cmd-d)
action(user.ide_multi_select_all): key(cmd-shift-l)

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

action(user.ide_toggle_status_bar):
  user.ide_command_palette()
  insert("View: Toggle Status Bar Visibility")
  key(enter)
#action(user.ide_toggle_power_save): user.idea("action TogglePowerSave")
action(user.ide_toggle_whitespace): 
  user.ide_command_palette()
  insert("View: Toggle Render Whitespace")
  key(enter)
action(user.ide_toggle_indents): user.ide_toggle_whitespace()
#requires an extension
#action(user.ide_toggle_line_numbers):
action(user.ide_toggle_breadcrumbs): 
  user.ide_command_palette()
  insert("View: Toggle Breadcrumbs")
  key(enter)
#action(user.ide_toggle_gutter_icons): user.idea("action EditorToggleShowGutterIcons")
action(user.ide_toggle_wrap): 
  user.ide_command_palette()
  insert("View: Toggle Word Wrap")
  key(enter)
#action(user.ide_toggle_parameters): user.idea("action ToggleInlineHintsAction")

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

action(user.ide_create_sibling):
  user.ide_command_palette()
  insert("File: New File")
  key(enter)

action(user.ide_create_file):
  # File: New and Titled File, workbench.action.files.newUntitledFile
  key(cmd-n)

action(user.ide_reveal_in_file_manager):
  # , workbench.action.files.revealActiveFileInWindows
  key(cmd-k r)

action(user.ide_find_file):
  # Go to File... , workbench.action.quickOpen
  key(cmd-p)

#tabs 
action(user.ide_go_first_tab): key(ctrl-1)
action(user.ide_go_second_tab): key(ctrl-2)
action(user.ide_go_third_tab): key(ctrl-3)
action(user.ide_go_fourth_tab): key(ctrl-4)
action(user.ide_go_fifth_tab): key(ctrl-5)
action(user.ide_go_sixth_tab): key(ctrl-6)
action(user.ide_go_seventh_tab): key(ctrl-7)
action(user.ide_go_eighth_tab): key(ctrl-8)
action(user.ide_go_ninth_tab): key(ctrl-9)
action(user.ide_clear_tab): key(cmd-w)