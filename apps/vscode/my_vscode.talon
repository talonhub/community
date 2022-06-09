#custom vscode commands go here
app: vscode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.snippets
tag(): user.splits
tag(): user.tabs

switch arc:
  key('ctrl-w')
  sleep(100ms)
  "archimedes"
  key('enter')

switch talon:
  key('ctrl-w')
  sleep(100ms)
  "talon"
  key('enter')

switch dendron:
  key('ctrl-w')
  sleep(100ms)
  "dendron"
  key('enter')

switch user:
  key('ctrl-w')
  sleep(100ms)
  "user"
  key('enter')

file (search|forage):
  user.vscode("workbench.action.findInFiles")

file path:
  user.vscode("copyRelativeFilePath")

# from https://talonvoice.slack.com/archives/C026KPTJE6T/p1649511384551359?thread_ts=1649423777.038099&cid=C026KPTJE6T
search next: user.vscode("search.action.focusNextSearchResult")
search last: user.vscode("search.action.focusPreviousSearchResult")
search file remove: user.vscode("search.searchEditor.action.deleteFileResults")
search remove: user.vscode("search.action.remove")
# search include:
#   user.mouse_helper_position_save()
#   user.mouse_helper_move_image_relative("2022-04-07_10.37.15.839419.png", 0, 0, 35)
#   sleep(0.05)
#   mouse_click(0)
#   sleep(0.05)
#   user.mouse_helper_position_restore()
#   key(cmd-a)
# search exclude:
#   user.mouse_helper_position_save()
#   user.mouse_helper_move_image_relative("2022-04-07_10.41.48.462607.png", 0, 0, 35)
#   sleep(0.05)
#   mouse_click(0)
#   sleep(0.05)
#   user.mouse_helper_position_restore()
#   key(cmd-a)
