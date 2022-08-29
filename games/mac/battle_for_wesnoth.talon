os: mac
app: The Battle for Wesnoth
-
# face
face(scrunch_nose): user.mouse_toggle_control_mouse()
face(pucker_lips_right): 
    key(cmd-r:down)
    sleep(64ms)
    key(cmd-r:up)
#face(eye_blink):
#    key(alt-space:down)
#    sleep(64ms)
#    key(alt-space:up) 
face(raise_eyebrows): key("n")

# actions
planner: key("p")
unit next: key("n")
unit (before|previous): key("shift-n")
unit rename: key("cmd-n")
unit hold: key("shift-space")
speak: key("m")
unit recruit: 
   key(cmd-r:down)
   sleep(64ms)
   key(cmd-r:up)
repeat recruit: 
   key(cmd-alt-r:down)
   sleep(64ms)
   key(cmd-alt-r:down)
unit recall: key("alt-r")
unit describe: key("d")

show enemy moves: key("cmd-v")
show enemy best: 
  key(cmd-b:down)
  sleep(64ms)
  key(cmd-b:up)
continue move: key("t")
redo that: key("r")
undo that: key("u")
go on: key("space")
end turn: 
  key(alt-space:down)
  sleep(64ms)
  key(alt-space:up)
speed up: key(shift:down)
release shift: key(shift:up)

# menu options
show objectives: 
   key(cmd-j:down)
   sleep(64ms)
   key(cmd-j:up)
show status: key("alt-s")
show statistics: key("s")
show units: key("alt-u")
show chat: key("alt-c")
show preferences: key("cmd-,")
show help: key("f1")

load game: 
   key(cmd-o:down)
   sleep(64ms)
   key(cmd-o:up)
save game: 
   key(cmd-s:down)
   sleep(64ms)
   key(cmd-s:up)
quit this: key("cmd-q")
quit to menu: 
 key("cmd-w")
 key("esc")   

# visuals
zoom in: key("+")
zoom out: key("-")
zoom reset: key("0")
center leader: key("l")
update fog: key("shift-s")


# toggles
toggle accelerate: key("cmd-a")
toggle ellipses: key("cmd-e")
toggle screen: key("cmd-f")
toggle sound: key("cmd-alt-m")



