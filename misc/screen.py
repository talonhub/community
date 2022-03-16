from talon import ui, actions

ui.register('screen_sleep', lambda e: actions.speech.disable())
#ui.register('screen_wake', lambda e: actions.speech.enable())
