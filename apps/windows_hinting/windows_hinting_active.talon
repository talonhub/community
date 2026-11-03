user.windows_hinting_active: True
-
^<user.hinting>$: user.windows_hinting_select(hinting)
^<user.hinting> left$: user.windows_hinting_select(hinting, "left")
^<user.hinting> troll$: user.windows_hinting_select(hinting, "ctrl")
^<user.hinting> shift$: user.windows_hinting_select(hinting, "shift")
^<user.hinting> connie$: user.windows_hinting_select(hinting, "right")
^<user.hinting> duke$: user.windows_hinting_select(hinting, "double")
^<user.hinting> hover$: user.windows_hinting_select(hinting, "move")
scrape: user.windows_hinting_deactivate()
