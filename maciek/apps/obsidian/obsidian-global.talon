os: mac
-
park$:
    key("ctrl-4") 
    # user.maciek_switch_to_app("obsidian")
    user.switcher_focus("obsidian")

park doc [<user.text>]$:
    key("ctrl-4") 
    user.switcher_focus("obsidian")
    user.obsidian_open_note(text or "", 0)

park daily: 
    key("ctrl-4") 
    user.switcher_focus("obsidian")
    user.obsidian_run_command("daily today daily")