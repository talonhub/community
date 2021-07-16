os:mac
-
horse [<phrase>]$: 
    key("ctrl-1") 
    sleep(1000ms)
    user.rephrase(phrase or "")
    
panda [<phrase>]$: 
    key("ctrl-2") 
    sleep(1000ms)
    user.rephrase(phrase or "")

puppy [<phrase>]$: 
    key("ctrl-3") 
    sleep(1000ms)
    user.rephrase(phrase or "")

goat [<phrase>]$: 
    key("ctrl-4") 
    sleep(1000ms)
    user.rephrase(phrase or "")

hold shift:
    key(shift:down)

release shift:
    key(shift:up)


  