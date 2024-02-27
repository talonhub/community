os: windows

-

focus <number_small>: key("super-ctrl-{number_small}")

exit <number_small>:
    key("super-alt-{number_small}")
    sleep(1000ms)
    key(up)
    sleep(500ms)
    key(enter)

right screen: key("super-shift-right")

left screen: key("super-shift-left")