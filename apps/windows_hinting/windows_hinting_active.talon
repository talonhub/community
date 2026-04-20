user.windows_hinting_active: True
-
^<user.hinting>$: 
    key(user.hinting)
    key(enter)

^<user.hinting> connie$: 
    key(shift-r)
    sleep(100ms)
    key(user.hinting)
    key(enter)

^<user.hinting> duke$: 
    key(shift-d)
    sleep(100ms)
    key(user.hinting)
    key(enter)

^<user.hinting> hover$: 
    key(shift-m)
    sleep(100ms)
    key(user.hinting)
    key(enter)

scrape: key(escape)
