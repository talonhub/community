# NOTE: If you want to use i3wm you must enable the tag settings.talon. i.e.: `tag(): user.i3wm`
os: linux
tag: user.i3wm
-
port <number_small>: user.i3msg("workspace number {number_small}")
(port flip | flipper): user.i3msg("workspace back_and_forth")
port right: user.i3msg("workspace next")
port left: user.i3msg("workspace prev")

(win | window) left: user.i3msg("focus left")
(win | window) right: user.i3msg("focus right")
(win | window) up: user.i3msg("focus up")
(win | window) down: user.i3msg("focus down")
(win | window) kill: app.window_close()
(win | window) (stacking | stacked): user.i3wm_layout("stacking")
(win | window) default: user.i3wm_layout()
(win | window) tabbed: user.i3wm_layout("tabbed")

reload i three config: user.i3msg("reload")
restart i three: user.i3msg("restart")

(full screen | scuba): user.i3msg("fullscreen")
toggle floating: user.i3msg("floating toggle")
focus floating: user.i3msg("focus mode_toggle")
center window: user.i3msg("move position center")
resize mode: user.i3msg("mode resize")
focus parent: user.i3msg("focus parent")
focus child: user.i3msg("focus child")

# resize helpers
grow window [<number>]: user.i3wm_grow_window(number or 20)
shrink window [<number>]: user.i3wm_shrink_window(number or 20)

horizontal (shell | terminal):
    user.i3msg("split h")
    user.i3wm_shell()

vertical (shell | terminal):
    user.i3msg("split v")
    user.i3wm_shell()

# XXX - just replace with shuffle eventually?
# XXX - like also need to match the generic talon commands
(shuffle | move (win | window) [to] port) <number_small>:
    user.i3msg("move container to workspace number {number_small}")
(shuffle | move (win | window) [to]) last port:
    user.i3msg("move container to workspace back_and_forth")
(shuffle | move) flipper: 
    user.i3msg("move container to workspace back_and_forth")
(shuffle | move (win | window)) left: user.i3msg("move left")
(shuffle | move (win | window)) right: user.i3msg("move right")
(shuffle | move (win | window)) up: user.i3msg("move up")
(shuffle | move (win | window)) down: user.i3msg("move down")

(win | window) horizontal: user.i3msg("split h")
(win | window) vertical: user.i3msg("split v")

make scratch: user.i3msg("move scratchpad")
[(show | hide)] scratch: user.i3msg("scratchpad show")
next scratch:
    user.i3msg("scratchpad show")
    user.i3msg("scratchpad show")

# these rely on the user settings for the mod key. see i3wm.py Actions class
launch: user.i3wm_launch()
launch <user.text>:
    user.i3wm_launch()
    sleep(100ms)
    insert("{text}")
lock screen: user.i3wm_lock()

(launch (shell | terminal) | koopa): user.i3wm_shell()

new scratch (shell | window):
    user.i3wm_shell()
    sleep(200ms)
    user.i3msg("move scratchpad")
    user.i3msg("scratchpad show")

murder:
    user.deprecate_command("2023-02-04", "murder", "win kill")
    app.window_close()
