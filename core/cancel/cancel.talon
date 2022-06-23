# allows you to prevent a command executing by ending it with "cancel cancel"
cancel cancel$: skip()
# the actual behavior of "cancel cancel" is implemented in code/cancel.py; if you want to use a different phrase you must also change cancel_phrase there.

# allows you to say something (eg to a human) that you don't want talon to hear, eg "ignore hey Jerry"
ignore [<phrase>]$: app.notify("Command ignored")
