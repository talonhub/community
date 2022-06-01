os:mac
-

# There are two versions of these comments. The problem with the one allowing additional phrase
# is that it conflicts with commands like "coder project".

horse$: 
    key("ctrl-1") 
    user.switcher_focus("google chrome")
    # user.rephrase(phrase or "")
    
coder$: 
    key("ctrl-2") 
    user.switcher_focus("code")
    # user.rephrase(phrase or "")

puppy$:user.focus_puppy()



###############################################################################
### KeyPad
###############################################################################
key(shift-cmd-alt-ctrl-1):
    key("ctrl-1") 
    user.switcher_focus("google chrome")
key(shift-cmd-alt-ctrl-2):
    key("ctrl-2") 
    user.switcher_focus("code")
key(shift-cmd-alt-ctrl-3):
    key("ctrl-3") 
    user.switcher_focus("kitty")
key(shift-cmd-alt-ctrl-p):    
    key("pageup")
key(shift-cmd-alt-ctrl-e):    
    key("pagedown")
code search:
    user.open_url("https://sourcegraph.com/search")


# switcher_focus wait until ui.active_app() == app, 
# But does this mean that talon made the context switch,  so that we can use rephrase?
# park [<phrase>]$:
#     key("ctrl-4") 
#     # user.maciek_switch_to_app("obsidian")
#     user.switcher_focus("obsidian")
#     user.rephrase(phrase or "")


  