from talon import actions, ctrl, noise

noise.register(
    "pop",
    lambda m: ctrl.mouse_click()
    if actions.speech.enabled()
    else actions.speech.enable(),
)
