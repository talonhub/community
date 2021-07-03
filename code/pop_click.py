from talon import ctrl, noise, actions

noise.register(
    "pop",
    lambda m: ctrl.mouse_click()
    if actions.speech.enabled()
    else actions.speech.enable(),
)
