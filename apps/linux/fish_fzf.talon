os: linux
tag: user.fish_fzf
-
fuzzy [<user.text>]: 
    key(ctrl-t)
    sleep(100ms) 
    insert(text or "")

buzzy [<user.text>]: 
    insert("~/")
    key(ctrl-t)
    sleep(100ms) 
    insert(text or "")
    
fuzzy var: key(ctrl-v) 