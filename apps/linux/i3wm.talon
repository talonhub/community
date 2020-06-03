os: linux
# TODO: match a window manager specified in a settings file
# TODO: take `super` from a settings file
# TODO: take vim_arrow vs arrow from a settings file
-

(works|screen) <number>: key("super-{number}")
(works|screen) ten: key(super-0)
(works|screen) (last|back|flip): key(super-u)
(works|screen) (right|next): key(super-o)
(works|screen) (prev|previous|left): key(super-y)

(win|window) left: key(super-h)
(win|window) right: key(super-l)
(win|window) up: key(super-k)
(win|window) down: key(super-j)
(win|window) kill: key(super-shift-q)
kill (win|window): key(super-shift-q)
(win|window) stacking: key(super-s)
(win|window) default: key(super-e)
(win|window) tabbed: key(super-w)
launch: key(super-d)
reload i three config: key(super-shift-c)
restart i three: key(super-shift-r)

full screen: key(super-f)
toggle floating: key(super-shift-space)
focus floating: key(super-space)
center window: key(super-shift-d)
resize mode: key(super-r)
focus parent: key(super-a)
focus child: key(super-shift-a)

# XXX - should include talon sleep maybe
lock screen: key(super-shift-x)

launch (shell|terminal): key(super-enter)
horizontal (shell|terminal):
    key(super-;)
    key(super-enter)

vertical (shell|terminal):
    key(super-v)
    key(super-enter)

move (win|window) [to] workspace <number>: key("super-shift-{number}")
move (win|window) [to] last workspace: key(super-shift-b)
move (win|window) <user.vim_arrow>: key("super-shift-{vim_arrow}")

(win|window) horizontal: key(super-;)
(win|window) vertical: key(super-v)

make scratch: key(super-shift--)
[(show|hide)] scratch: key(super--)
new scratch shell:
    key(super-enter)
    sleep(200ms)
    key(super-shift--)
    key(super--)
next scratch:
    key(super--)
    key(super--)
