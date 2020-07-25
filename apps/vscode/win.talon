# Microsoft - Visual Studio Code
# see app/vscode.talon for voice commands
os: windows
app: Visual Studio Code
app: Code.exe
-
tag(): tabs
tag(): ide
tag(): line_commands
tag(): splits
tag(): snippets
tag(): multiple_cursors
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

# Toggleable views
action(user.ide_toggle_fullscreen): 
  user.ide_command_palette()
  insert("View: Toggle Full Screen")
  key(enter)
#action(user.ide_toggle_distraction_free): user.idea("action ToggleDistractionFreeMode")
#action(user.ide_toggle_presentation_mode): user.idea("action TogglePresentationMode")

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

#Refactor
action(user.ide_refactor): key(ctrl-shift-r)
action(user.ide_refactor_in_line): key(ctrl-shift-r)
action(user.ide_refactor_rename): key(f2)
action(user.ide_rename_file): 
  user.ide_command_palette()
  insert("File: Reveal Active File In Side Bar")
  key(enter f2)
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

action(user.ide_create_sibling):
  user.ide_command_palette()
  insert("File: New File")
  key(enter)

action(user.ide_create_file):
  # File: New and Titled File, workbench.action.files.newUntitledFile
  key(ctrl-n)

action(user.ide_reveal_in_file_manager):
  # , workbench.action.files.revealActiveFileInWindows
  key(ctrl-k r)

action(user.ide_find_file):
  # Go to File... , workbench.action.quickOpen
  key(ctrl-p)
  
# splits.py support begin
action(user.split_window_right):
  user.ide_command_palette()
  insert("workbench.action.moveEditorToRightGroup")
  key(enter)
action(user.split_window_left):
  user.ide_command_palette()
  insert("workbench.action.moveEditorToLeftGroup")
  key(enter)
action(user.split_window_up):
  user.ide_command_palette()
  insert("workbench.action.moveEditorToAboveGroup")
  key(enter)
action(user.split_window_down):
  user.ide_command_palette()
  insert("workbench.action.moveEditorToBelowGroup")
  key(enter)
action(user.split_window_vertically): 
  user.ide_command_palette()
  insert("View: Split Editor")
  key(enter)
action(user.split_window_horizontally): 
  user.ide_command_palette()
  insert("View: Split Editor Orthogonal")
  key(enter)
action(user.split_flip): key(alt-shift-0)
action(user.split_window): key(ctrl-\)
action(user.split_clear): user.split_clear_all()
action(user.split_clear_all): 
  user.ide_command_palette()
  insert("View: Single Column Editor Layout")
  key(enter)
action(user.split_next): key(ctrl-k ctrl-right)
action(user.split_last): key(ctrl-k ctrl-left)
# splits.py support end

#multiple_cursor.py support begin
#note: vscode has no explicit mode for multiple cursors
action(user.multi_cursor_enable): skip()
action(user.multi_cursor_disable): key(escape)
action(user.multi_cursor_add_above):key(ctrl-alt-up)
action(user.multi_cursor_add_below): key(ctrl-alt-down)
action(user.multi_cursor_select_fewer_occurrences): key(ctrl-u)
action(user.multi_cursor_select_more_occurrences): key(ctrl-d)
action(user.multi_cursor_select_all_occurrences): key(ctrl-shift-l)
#multiple_cursor.py support end