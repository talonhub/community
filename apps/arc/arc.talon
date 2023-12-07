app: arc
-
tag(): browser
tag(): user.tabs

profile switch: user.arc_mod("shift-m")

tab search: user.arc_mod("shift-a")

tab search <user.text>$:
    user.arc_mod("shift-a")
    sleep(200ms)
    insert("{text}")
    key(down)
