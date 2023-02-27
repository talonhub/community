app: chrome
-
tag(): browser
profile switch: user.chrome_mod("shift-m")

tag(): user.tabs
tab search: user.chrome_mod("shift-a")

tab search <user.text>$:
    user.chrome_mod("shift-a")
    sleep(200ms)
    insert("{text}")
    key(down)
