app: RemNote

make blank:
    key(cmd-alt-q)

make concept:
    key(cmd-alt-c)
    sleep(100ms)

concept:
    "::"
    sleep(100ms)

prop:
    ";;"
    sleep(100ms)

props:
    ";;;"
    sleep(100ms)

biprop:
    ";;"
    sleep(100ms)
    "<"
    sleep(100ms)

definition:
    "<>"
    sleep(100ms)

equation:
    "$$"
    sleep(100ms)

text:
    key(\)
    key(t)
    key(e)
    key(x)
    key(t)
    key({)
    key(})
    key(left)

frac:
    key(\)
    key(f)
    key(r)
    key(a)
    key(c)
    key({)
    key(})
    key({)
    key(})
    key(left)
    key(left)
    key(left)

enter:
    key(enter)
    sleep(150ms)

indent:
    key(tab)
    sleep(100ms)

dedent:
    key(shift-tab)
    sleep(100ms)

padded:
    key(space)
    key(space)
    key(left)

done:
    key(enter)
    sleep(150ms)
    key(right)

lecture toggle:
    user.switcher_focus("firefox")
    key(space)
    user.switcher_focus("RemNote")

lecture (back | previous):
    user.switcher_focus("firefox")
    key(left)
    user.switcher_focus("RemNote")

lecture (back | previous) <number_small>:
    user.switcher_focus("firefox")
    key(left)
    repeat(number_small)
    user.switcher_focus("RemNote")

lecture (forward | next):
    user.switcher_focus("firefox")
    key(right)
    user.switcher_focus("RemNote")

lecture (forward | next) <number_small>:
    user.switcher_focus("firefox")
    key(right)
    repeat(number_small)
    user.switcher_focus("RemNote")

screenshot:
    key(cmd-shift-4)
