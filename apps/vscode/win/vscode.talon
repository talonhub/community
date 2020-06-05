# Microsoft - Visual Studio Code
# see app/vscode.talon for voice commands

os: windows
app: Visual Studio Code
app: Code.exe
-

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
  key(alt-left)

action(user.ide_terminal_focus_next):
  key(alt-right)

action(user.ide_terminal_trash):
  key(ctrl-shift-delete)

action(user.ide_terminal_scroll_down):
  key(shift-pgdown)

action(user.ide_terminal_scroll_up):
  key(shift-pgup)

action(user.ide_toggle_comment):
  key(ctrl-/)

action(user.ide_smart):
  key(ctrl-space)

action(user.ide_parameter_hints):
  key(ctrl-shift-space)

action(user.ide_done):
  key(tab)

action(user.ide_show_explorer):
  key(ctrl-shift-e)

action(user.ide_show_search):
  key(ctrl-shift-f)

action(user.ide_show_source_control):
  key(ctrl-shift-g)

action(user.ide_show_debug):
  key(ctrl-shift-d)

action(user.ide_show_extensions):
  key(ctrl-shift-x)
