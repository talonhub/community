tag: user.taskbar_canvas_popup_showing
tag: user.hinting_active
-
^<user.hinting>$: 
    user.hinting_select(0, hinting, 1)

^<user.hinting> connie$: 
    user.hinting_select(1, hinting, 1)

^<user.hinting> duke$: 
    user.hinting_select(0, hinting, 2)

^<user.hinting> hover$: 
    user.hinting_select(0, hinting, 0)

scrape:
    user.hinting_close()