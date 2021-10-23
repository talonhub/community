os: mac
tag: user.fish
-
tag(): user.brew
tag(): user.poetry

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

cancel|fucker: key(ctrl-c)

go dir:
    key(cmd-d)
    
go dir home:
    key(cmd-shift-d)
podo: 
    key(cmd-g)  


(wipe|clear) lord:
    user.delete_big_word()

# (clear board|clear big word):
#     fzf.delete_big_word()