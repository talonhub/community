from talon import Context, speech_system, actions
from talon_plugins import speech

ctx = Context()

def set_enabled(value):
    ctx.exclusive = not value
    actions.speech.toggle(value)

ctx.commands = {
    'talon sleep': lambda m: set_enabled(False),
    'talon wake': lambda m: set_enabled(True),

    'dragon mode': [lambda m: set_enabled(False), lambda m: speech_system.engine_mimic('wake up'.split())],
    'talon mode': [lambda m: set_enabled(True), lambda m: speech_system.engine_mimic('go to sleep'.split())],
}