app: Runelite

# inventory tabs
style: key(f1)
skill: key(f2)
quest: key(f3)
invent: key(esc)
equip: key(f4)
pray: key(f5)
magic: key(f6)
friends: key(f8)
clan: key(f7)
music: key(f12)
world hop: key(f14)

skip dialogue:
    user.toggle_key_repeater('space')

under:
    #user.zoom_close()
    key("shift:down")
    sleep(200ms)
    mouse_click(0)
    sleep(200ms)
    key("shift:up")