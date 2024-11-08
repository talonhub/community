^flow mode:
    mode.disable("command")
    mode.disable("dictation")
    mode.enable("user.flow")
    key('fn-space')
    sleep(500ms)
    mouse_click()

flow paste (last | previous):
    key('cmd-ctrl-v')