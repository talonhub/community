os: mac
tag: user.fish
-
tag(): user.brew
tag(): user.poetry
fuzzy [<user.text>]:
    key(cmd-e)
    sleep(100ms)
    insert(text or "")
    
fuzzy root [<user.text>]:
    insert("/")
    key(cmd-e)
    sleep(100ms)
    insert(text or "")
fuzzy home [<user.text>]:
    insert("~/")
    key(cmd-e)
    sleep(100ms)
    insert(text or "")
    
    
    # star is here because of misrecognition
(history|story) [<user.text>]:
    key(cmd-r)
    sleep(100ms)
    insert(text or "")
    
fuzzy var: key(ctrl-v)

cancel|fucker: key(ctrl-c)

go dir:
    user.fzf_cd_directory_multi_level()
    
go dir home:
    key(cmd-shift-d)
    # podo:
    # user.fzf_cd_directory_single_level()
    
    
(wipe|clear) lord:
    user.delete_big_word()
    
    # (clear board|clear big word):
    #     fzf.delete_big_word()
