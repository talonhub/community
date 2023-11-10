#custom vscode commands go here
app: vscode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.snippets
tag(): user.splits
tag(): user.tabs
tag(): user.cursorless_experimental_snippets

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


# Bookmarks. Requires Bookmarks plugin
go marks: user.vscode("workbench.view.extension.bookmarks")
toggle mark: user.vscode("bookmarks.toggle")
go next mark: user.vscode("bookmarks.jumpToNext")
go last mark: user.vscode("bookmarks.jumpToPrevious")

# alternatives to Bookmarks in vscode.talon
# go marks
bar mark: user.vscode("workbench.view.extension.bookmarks")
# go next mark
mark next: user.vscode("bookmarks.jumpToNext")
# go last mark
mark previous: user.vscode("bookmarks.jumpToPrevious")
# toggle mark
mark toggle: user.vscode("bookmarks.toggle")
(toggle mark|mark toggle) label:
  key(alt-cmd-h)

(tab pin|pin toggle):
  key(cmd-k)
  key(shift-enter)

# requires the extension: https://marketplace.visualstudio.com/items?itemName=testdouble.vscode-alternate-alternate-file
pop sibling:
  user.vscode("workbench.action.showCommands")
  insert("alternate file")
  sleep(100ms)
  key(enter)

tab hunt <user.text>:
  user.vscode("workbench.action.quickOpen")
  insert("edt ")
  insert(user.text or "")


suggest:
  user.vscode("editor.action.inlineSuggest.trigger")
