os: mac
tag: user.fish_fzf
-
action(edit.delete_word):
	edit.word_right()
	key(ctrl-w)

fuzzy [<user.text>]: 
    key(cmd-e)
    sleep(100ms) 
    insert(text or "")

(history|story) [<user.text>]: 
    key(cmd-r)
    sleep(100ms) 
    insert(text or "")

buzzy [<user.text>]: 
    insert("~/")
    key(cmd-e)
    sleep(100ms) 
    insert(text or "")
    
fuzzy var: key(ctrl-v) 

cancel [that]: key(ctrl-c)
fucker: key(ctrl-c)

# (clear board|clear big word):
#     fzf.delete_big_word()