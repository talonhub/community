mode: user.flow
--

parrot(cluck):
    key('fn-space')
    mouse_click()
    mode.disable("user.flow")
    mode.enable("command")