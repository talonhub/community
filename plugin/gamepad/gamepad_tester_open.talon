tag: user.gamepad_tester
-

# D-pad buttons
gamepad(dpad_up:up):        user.gamepad_tester_button("dpad_up", false)
gamepad(dpad_up:down):      user.gamepad_tester_button("dpad_up", true)
gamepad(dpad_right:up):     user.gamepad_tester_button("dpad_right", false)
gamepad(dpad_right:down):   user.gamepad_tester_button("dpad_right", true)
gamepad(dpad_down:up):      user.gamepad_tester_button("dpad_down", false)
gamepad(dpad_down:down):    user.gamepad_tester_button("dpad_down", true)
gamepad(dpad_left:up):      user.gamepad_tester_button("dpad_left", false)
gamepad(dpad_left:down):    user.gamepad_tester_button("dpad_left", true)

# Compass buttons
gamepad(north:up):          user.gamepad_tester_button("north", false)
gamepad(north:down):        user.gamepad_tester_button("north", true)
gamepad(east:up):           user.gamepad_tester_button("east", false)
gamepad(east:down):         user.gamepad_tester_button("east", true)
gamepad(south:up):          user.gamepad_tester_button("south", false)
gamepad(south:down):        user.gamepad_tester_button("south", true)
gamepad(west:up):           user.gamepad_tester_button("west", false)
gamepad(west:down):         user.gamepad_tester_button("west", true)

# Select/start buttons
gamepad(select:up):         user.gamepad_tester_button("select", false)
gamepad(select:down):       user.gamepad_tester_button("select", true)
gamepad(start:up):          user.gamepad_tester_button("start", false)
gamepad(start:down):        user.gamepad_tester_button("start", true)

# Bumper buttons
gamepad(l1:up):             user.gamepad_tester_button("l1", false)
gamepad(l1:down):           user.gamepad_tester_button("l1", true)
gamepad(r1:up):             user.gamepad_tester_button("r1", false)
gamepad(r1:down):           user.gamepad_tester_button("r1", true)

# Stick click buttons
gamepad(l3:up):             user.gamepad_tester_button("l3", false)
gamepad(l3:down):           user.gamepad_tester_button("l3", true)
gamepad(r3:up):             user.gamepad_tester_button("r3", false)
gamepad(r3:down):           user.gamepad_tester_button("r3", true)

# Trigger buttons
gamepad(l2:change):         user.gamepad_tester_trigger("l2", value)
gamepad(r2:change):         user.gamepad_tester_trigger("r2", value)

# Sticks axis
gamepad(left_xy):           user.gamepad_tester_stick("left", x, y*-1)
gamepad(right_xy):          user.gamepad_tester_stick("right", x, y*-1)
