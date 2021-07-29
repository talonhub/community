# allows you to cancel a command that you realize you are flubbing, eg "air bat crap cancel"
^[<phrase>] cancel$: app.notify("Command canceled")

# allows you to say something (eg to a human) that you don't want talon to hear, eg "ignore hey Jerry"
ignore [<phrase>]$: app.notify("Command ignored")
