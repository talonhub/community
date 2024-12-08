os: mac
app: finder
-
tag(): user.address
tag(): user.file_manager
tag(): user.navigation
tag(): user.tabs
preferences: key(cmd-,)
options: key(cmd-j)
search: key(cmd-alt-f)

# bit of a mouthful, but it's probably not the kind of thing you'd be saying frequently
sort by none: key(ctrl-alt-cmd-0)
sort by name: key(ctrl-alt-cmd-1)
sort by kind: key(ctrl-alt-cmd-2)
sort by date opened: key(ctrl-alt-cmd-3)
sort by date added: key(ctrl-alt-cmd-4)
sort by date modified: key(ctrl-alt-cmd-5)
sort by size: key(ctrl-alt-cmd-6)

icon view: key(cmd-1)
column view: key(cmd-3)
list view: key(cmd-2)
gallery view: key(cmd-4)

trash it: key(cmd-backspace)

hide [finder]: key(cmd-h)
hide others: app.window_hide_others()
