# Microsoft - Visual Studio Code
# see app/vscode.talon for voice commands

os: windows
app: Visual Studio Code
app: Code.exe
-


tag(): git
# TODO When tags are supported
# tag(): ide

# General
action(user.ide_command_palette):
  key(ctrl-shift-p)

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

action(user.ide_refactor):
  key(ctrl-a)
  key(ctrl-shift-i)
  key(ctrl-s)

action(user.ide_refactor_in_line):
  key(ctrl-shift-i)
  key(ctrl-s)

action(user.ide_refactor_rename):
  key(f2)

action(user.ide_follow):
  key(f12)

action(user.ide_go_back):
  key(alt-left)

action(user.ide_go_forward):
  key(alt-right)

action(user.ide_up_cursor):
  key(ctrl-shift-up)

action(user.ide_down_cursor):
  key(ctrl-shift-down)

action(user.ide_toggle_terminal):
  key(ctrl-`)

action(user.ide_terminal_new):
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
  key(shift-pgdown)

action(user.ide_terminal_scroll_up):
  key(shift-pgup)

action(user.ide_toggle_comment):
  key(ctrl-/)

action(user.ide_smart):
  #user.ide_intellisense_suggest_parameters
  key(ctrl-space)

action(user.ide_intellisense_suggest_parameters):
  key(ctrl-shift-space)

action(user.ide_done):
  key(tab)

action(user.ide_toggle_project):
  key(ctrl-shift-e)

action(user.ide_toggle_find):
  key(ctrl-shift-f)
action(user.ide_find_everywhere):
  key(ctrl-shift-f)
action(user.ide_replace_everywhere):
  key(ctrl-shift-h)
action(user.ide_replace_local):
  key(ctrl-h)
action(user.ide_replace_confirm_current):
  key(ctrl-shift-1)
action(user.ide_replace_confirm_all):
  key(ctrl-alt-enter)


action(user.ide_find_match_by_case):
  key(alt-c)
action(user.ide_find_match_by_word):
  key(alt-w)
action(user.ide_find_match_by_regex):
  key(alt-r)

action(user.ide_toggle_git):
  key(ctrl-shift-g)

action(user.ide_toggle_run):
  key(ctrl-shift-d)
action(user.ide_toggle_debug):
  key(ctrl-shift-d)

action(user.ide_toggle_breakpoint):
  key(f9)
action(user.ide_step_over):
  key(f10)
action(user.ide_step_into):
  key(f11)
action(user.ide_step_out):
  key(shift-f11)

action(user.ide_toggle_extensions):
  key(ctrl-shift-x)

action(app.window_open):
  key(ctrl-shift-n)

action(user.ide_create_file):
  key(ctrl-n)

action(user.ide_reveal_in_file_manager):
  key(ctrl-k r)