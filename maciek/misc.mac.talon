os:mac
-
horse [<phrase>]$: 
    key("ctrl-1") 
    user.switcher_focus("google chrome")
    user.rephrase(phrase or "")
    
panda [<phrase>]$: 
    key("ctrl-2") 
    user.switcher_focus("code")
    user.rephrase(phrase or "")

puppy [<phrase>]$:
    key("ctrl-3") 
    user.switcher_focus("kitty")
    user.rephrase(phrase or "")

# switcher_focus wait until ui.active_app() == app, 
# But does this mean that talon made the context switch,  so that we can use rephrase?
park [<phrase>]$:
    key("ctrl-4") 
    user.rephrase(phrase or "")

# this doesn't work. I have asked on slack about it and got some sensible answer why it doesn't work.
# hold shift:
#     key(shift:down)

# release shift:
#     key(shift:up)


  