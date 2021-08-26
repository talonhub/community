os: mac
--
spotlight [<user.text>]:
    key(cmd-alt-space)
    sleep(50ms)
    insert(text or "")


talon additional:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/settings/additional_words.csv")
    sleep(1000ms)
    key(cmd-down)
    key(enter)

talon code:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/apps/vscode/vscode.talon")
    sleep(1000ms)
    key(cmd-down)
    key(enter)
talon command line:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/maciek/commandline.talon")
    sleep(1000ms)
    key(cmd-down)
    key(enter)
        
talon replace:
    user.run_in_fish_shell("code /Users/maciek/projects/knausj_talon/settings/words_to_replace.csv")
    sleep(1000ms)
    key(cmd-down)
    key(enter)
talon anki code:
    user.run_in_fish_shell("code /Users/maciek/obsidian/maciek-knowledge/vscode\ talon\ anki.md")
    sleep(1000ms)
    key(cmd-down)
    key(enter)
talon anki basic:
    user.run_in_fish_shell("code /Users/maciek/obsidian/maciek-knowledge/talon\ basic\ anki.md")
    sleep(1000ms)
    key(cmd-down)
    key(enter)
    
    