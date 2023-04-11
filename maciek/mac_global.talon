os: mac
-


horse [<phrase>]: 
    key("ctrl-1") 
    user.switcher_focus_and_wait("google chrome")
    sleep(100ms)    
    user.rephrase(phrase or "")
    
coder [<phrase>]: 
    key("ctrl-2") 
    user.switcher_focus_and_wait("code", 0.5)
    sleep(100ms)
    user.rephrase(phrase or "")

puppy [<phrase>]$:
    user.focus_puppy()
    user.rephrase(phrase or "")




code search:
    user.open_url("https://sourcegraph.com/search")


# switcher_focus_and_wait wait u, 0.5ntil ui.active_app() == app, 
# But does this mean that talon made the context switch,  so that we can use rephrase?
# park [<phrase>]$:
#     key("ctrl-4") 
#     # user.maciek_switch_to_app("obsidian")
#     user.switcher_focus_and_wait("obsid, 0.5ian")
#     user.rephrase(phrase or "")


  

###############################################################################
### general editing commands
###############################################################################

notes toggle:key(cmd-shift-f6)
coder <user.vscode_project_names>: 
    user.switcher_focus_and_wait("code", 0.5)
    sleep(100ms)
    user.vscode_open_project(vscode_project_names)
wipe|thrash: key(alt-backspace)
(clear|wipe|thrash) all:
    edit.select_all()
    edit.delete()


down: key(down)
menu help: key(cmd-shift-/)
menu show:
    key(ctrl-shift-f2)
    sleep(100ms)
    key(enter)
    
spotlight [<user.text>]:
    key(cmd-alt-space)
    sleep(50ms)
    insert(text or "")
(raycast|spot) [<user.text>]:
    key(alt-space)
    sleep(50ms)
    insert(text or "")

spot clipboard: user.raycast_clipboard()
spot close: key(cmd-w)

talon play:user.run_in_fish_shell("talon-play-pre-last")    
talon restart: user.run_in_fish_shell("talon-restart")
puppy talon: user.focus_talon_window()

###########################################    
# Open specific files in knausj_talon
###########################################
polo mac o s:
    user.vscode_open_project("knausj_talon")
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/maciek/macOS.talon")
    user.switcher_focus_and_wait("code", 0.5)
    key(cmd-down)
    key(enter)
polo obsidian:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/maciek/apps/obsidian/obsidian.mac.talon")
    user.switcher_focus_and_wait("code", 0.5)
    key(cmd-down)
    key(enter)
#punctuation_words
    
    

polo additional:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/settings/additional_words.csv")
    user.switcher_focus_and_wait("code", 0.5)
    sleep(500ms)
    key(cmd-down)
    key(enter)

coder file code:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/apps/vscode/vscode.talon")
    user.switcher_focus_and_wait("code", 0.5)
    key(cmd-down)
    key(enter)

polo coder command line:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/maciek/commandline.talon")
    user.switcher_focus_and_wait("code", 0.5)
    key(cmd-down)
    key(enter)
polo coder chrome:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/maciek/chrome_mac.talon")
    user.switcher_focus_and_wait("code", 0.5)
    key(cmd-down)
    key(enter)
polo coder websites:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/settings/websites.csv")
    user.switcher_focus_and_wait("code", 0.5)
    key(cmd-down)
    key(enter)
    
        
polo replace:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/settings/words_to_replace.csv")
    user.switcher_focus_and_wait("code", 0.5)
    user.engine_mimic("pour file")
# anki
anki vscode:
    user.run_in_fish_shell("code /Users/maciek/obsidian/maciek-knowledge/vscode\ talon\ anki.md")
    user.switcher_focus_and_wait("anki", 0.5)
    key(cmd-down)
    key(enter)
anki basic:
    user.run_in_fish_shell("code /Users/maciek/obsidian/maciek-knowledge/talon\ basic\ anki.md")
    user.switcher_focus_and_wait("anki", 0.5)
    key(cmd-down)
    key(enter)

insert email: insert("maciej.klimek@gmail.com")
insert fake email: insert("waldemar.bajka@gmail.com")
insert full name: insert("Maciej Klimek")

windows: key(ctrl-down)
all windows: key(ctrl-up)
    
# input method
input maciek:
    user.system_command("/opt/homebrew/bin/im-select casadelmaciek.inputmethod.MaciekInputMethod")    
input polish:
    user.system_command("/opt/homebrew/bin/im-select com.apple.keylayout.PolishPro")
# vimac
links: key(cmd-alt-shift-f1)


# I have problems with these words
(truce|moon|choice) <number_small>:
    key(down)
    repeat(number_small-2)
    key(enter)

click up task$:
    user.switcher_focus_and_wait("click", 0.5)
    key(t)
    
raindrop search [<user.text>]:
   user.raycast_raindrop_search(text or "") 
raindrop recent:
    key(cmd-shift-f5)     

polo help coder: user.raycast_talon_search("vscode")
^coder project [<user.text>]$: user.raycast_coder_project(text or "")
^polo search [<user.text>]$: user.raycast_talon_search(text or "")
github repo [<user.text>]:
    


lend|(line end): key(cmd-right)

zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
post$:
    sleep(1ms)    



    
    





    