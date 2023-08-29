os: mac
app: dev.warp.Warp-Stable
-
tag(): terminal
# todo: filemanager support
#tag(): user.file_manager
tag(): user.generic_unix_shell
tag(): user.git
tag(): user.kubectl
tag(): user.tabs
tag(): user.readline

^last speck:
  key(cmd-l)
  "spec"
  key(ctrl-r)

# ^last <phrase>:
#   key(cmd-l)
#   mimic(phrase)
#   key(ctrl-r)

# ^command [<phrase>]:
#   key(cmd-l)
#   mimic(phrase or "")
#   # user.parse_phrase(phrase or "")

last one:
  key(cmd-l)
  key(up)
  key(enter)
