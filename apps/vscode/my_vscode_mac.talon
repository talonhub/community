#custom vscode commands go here
app: vscode
os: mac
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.snippets
tag(): user.splits
tag(): user.tabs

# note: change vscode preferences window title to `[${rootName}] ${activeEditorShort}${separator}${profileName}`
#       so that project name is first and inside [].
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
