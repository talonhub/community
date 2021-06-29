os: linux
tag: terminal
-
tag(): user.file_manager
 
sudo: insert("sudo ")
add sudo: 
    key(home)
    insert("sudo ")
add help: insert(" --help ")
run last:
  key(up)
  key(enter)
rerun <user.text>:
  key(ctrl-r)
  insert(text)
rerun search:
  key(ctrl-r)
kill all:
  key(ctrl-c)

# XXX - these are specific to certain terminals only and should move into their
# own <term name>.talon file
action(edit.word_left):
  key(ctrl-w left)
action(edit.word_right):
  key(ctrl-w right)
action(app.window_open):
  key(ctrl-shift-n)
go tab <number>:
  key("alt-{number}")
