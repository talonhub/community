user.windows_hinting_active: True
-
^<user.hinting>$: 
    key(user.hinting)
    key(enter)

^<user.hinting> left$:
    key(shift-l)
    key(user.hinting)
    key(enter)

^<user.hinting> troll$:
    key(shift-c)
    key(user.hinting)
    key(enter)

^<user.hinting> shift$:
    key(shift-s)
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
