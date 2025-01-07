#custom vscode commands go here
app: vscode
os: windows
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.splits
tag(): user.tabs

# TODO: get this working... i need to learn about captures
# switch <phrase>:
#   key('alt-`')
#   sleep(100ms)
#   user.parse_phrase(phrase)
#   key('enter')

switch user:
  key('alt-`')
  sleep(100ms)
  "user"
  key('enter')

# on my windows, i am running dendron in a docker dev environment
switch (docker|dendron):
  key('alt-`')
  sleep(100ms)
  "docker"
  key('enter')
