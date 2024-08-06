tag: user.gamepad
and not tag: user.gamepad_tester
-

# DPAD buttons
gamepad(dpad_left:down):    user.gamepad_button_down("dpad_left")
gamepad(dpad_left:up):      user.gamepad_button_up("dpad_left")
gamepad(dpad_up:down):      user.gamepad_button_down("dpad_up")
gamepad(dpad_up:up):        user.gamepad_button_up("dpad_up")
gamepad(dpad_right:down):   user.gamepad_button_down("dpad_right")
gamepad(dpad_right:up):     user.gamepad_button_up("dpad_right")
gamepad(dpad_down:down):    user.gamepad_button_down("dpad_down")
gamepad(dpad_down:up):      user.gamepad_button_up("dpad_down")

# Compass / ABXY buttons
gamepad(west:down):         user.gamepad_button_down("west")
gamepad(west:up):           user.gamepad_button_up("west")
gamepad(north:down):        user.gamepad_button_down("north")
gamepad(north:up):          user.gamepad_button_up("north")
gamepad(east:down):         user.gamepad_button_down("east")
gamepad(east:up):           user.gamepad_button_up("east")
gamepad(south:down):        user.gamepad_button_down("south")
gamepad(south:up):          user.gamepad_button_up("south")

# Select / Start buttons
gamepad(select:down):       user.gamepad_button_down("select")
gamepad(select:up):         user.gamepad_button_up("select")
gamepad(start:down):        user.gamepad_button_down("start")
gamepad(start:up):          user.gamepad_button_up("start")

# Shoulder buttons
gamepad(l1:down):           user.gamepad_button_down("left_shoulder")
gamepad(l1:up):             user.gamepad_button_up("left_shoulder")
gamepad(r1:down):           user.gamepad_button_down("right_shoulder")
gamepad(r1:up):             user.gamepad_button_up("right_shoulder")

# Stick buttons
gamepad(l3:down):           user.gamepad_button_down("left_stick")
gamepad(l3:up):             user.gamepad_button_up("left_stick")
gamepad(r3:down):           user.gamepad_button_down("right_stick")
gamepad(r3:up):             user.gamepad_button_up("right_stick")

# Analog triggers
gamepad(l2:repeat):         user.gamepad_trigger_left(value)
gamepad(r2:repeat):         user.gamepad_trigger_right(value)

# Analog thumb sticks
gamepad(left_xy:repeat):    user.gamepad_stick_left(x, y*-1)
gamepad(right_xy:repeat):   user.gamepad_stick_right(x, y*-1)
