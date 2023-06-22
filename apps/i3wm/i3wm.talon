# NOTE: If you want to use i3wm you must enable the tag settings.talon. i.e.: `tag(): user.i3wm`
os: linux
tag: user.i3wm
-
port <number_small>: user.i3wm_switch_to_workspace(number_small)
(port flip | flipper): user.i3wm_switch_to_workspace("back_and_forth")
port right: user.i3wm_switch_to_workspace("next")
port left: user.i3wm_switch_to_workspace("prev")

(win | window) left: user.i3wm_focus("left")
(win | window) right: user.i3wm_focus("right")
(win | window) up: user.i3wm_focus("up")
(win | window) down: user.i3wm_focus("down")
(win | window) kill: app.window_close()
(win | window) stacking: user.i3wm_layout("stacking")
(win | window) default: user.i3wm_layout()
(win | window) tabbed: user.i3wm_layout("tabbed")

reload i three config: user.i3wm_reload()
restart i three: user.i3wm_restart()

(full screen | scuba): user.i3wm_fullscreen()
toggle floating: user.i3wm_float()
focus floating: user.i3wm_focus("mode_toggle")
center window: user.i3wm_move_position("center")
resize mode: user.i3wm_mode("resize")
focus parent: user.i3wm_focus("parent")
focus child: user.i3wm_focus("child")

# resize helpers
grow window:
    user.i3wm_mode("resize")
    key(right:10)
    key(down:10)
    # escape resize mode
    key(escape)
    # center window
    sleep(200ms)
    user.i3wm_move_position("center")

# resize helpers
shrink window:
    user.i3wm_mode("resize")
    key(left:10)
    key(up:10)
    # escape resize mode
    key(escape)
    # center window
    sleep(200ms)
    user.i3wm_move_position("center")

horizontal (shell | terminal):
    user.i3wm_split("h")
    user.i3wm_shell()

vertical (shell | terminal):
    user.i3wm_split("v")
    user.i3wm_shell()

# XXX - just replace with shuffle eventually?
# XXX - like also need to match the generic talon commands
(shuffle | move (win | window) [to] port) <number_small>:
    user.i3wm_move_to_workspace(number_small)
(shuffle | move (win | window) [to] last port):
    user.i3wm_move_to_workspace("back_and_forth")
(shuffle | move) flipper: user.i3wm_move_to_workspace("back_and_forth")
(shuffle | move (win | window) left): user.i3wm_move("left")
(shuffle | move (win | window) right): user.i3wm_move("right")
(shuffle | move (win | window) up): user.i3wm_move("up")
(shuffle | move (win | window) down): user.i3wm_move("down")

(win | window) horizontal: user.i3wm_split("h")
(win | window) vertical: user.i3wm_split("v")

make scratch: user.i3wm_move("scratchpad")
[(show | hide)] scratch: user.i3wm_show_scratchpad()
next scratch:
    user.i3wm_show_scratchpad()
    user.i3wm_show_scratchpad()

# these rely on the user settings for the mod key. see i3wm.py Actions class
launch: user.i3wm_launch()
launch <user.text>:
    user.i3wm_launch()
    sleep(100ms)
    insert("{text}")
lock screen: user.i3wm_lock()

(launch shell | koopa): user.i3wm_shell()

new scratch (shell | window):
    user.i3wm_shell()
    sleep(200ms)
    user.i3wm_move("scratchpad")
    user.i3wm_show_scratchpad()

murder:
    user.deprecate_command("2023-02-04", "murder", "win kill")
    app.window_close()
