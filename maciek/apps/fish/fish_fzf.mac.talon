os: 
tag: user.fish_fzf
-
fuzzy [<user.text>]: 
    key(ctrl-t)
    sleep(100ms) 
    insert(text or "")

(history|story) [<user.text>]: 
    key(ctrl-r)
    sleep(100ms) 
    insert(text or "")

buzzy [<user.text>]: 
    insert("~/")
    key(ctrl-t)
    sleep(100ms) 
    insert(text or "")
    
fuzzy var: key(ctrl-v) 

cancel [that]: key(ctrl-c)
fucker: key(ctrl-c)