# the actual behavior of "cancel cancel" is implemented in code/cancel.py
# it allows you to prevent a command from executing by ending it with "cancel cancel"
cancel cancel$: skip()

# allows you to say something (eg to a human) that you don't want talon to hear, eg "ignore hey Jerry"
ignore [<phrase>]$: app.notify("Command ignored")
