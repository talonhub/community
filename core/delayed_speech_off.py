from talon import Module, actions, speech_system

delay_mod = Module()

delayed_enabled = False


def do_disable(e):
    speech_system.unregister("post:phrase", do_disable)
    actions.speech.disable()


@delay_mod.action_class
class DelayedSpeechOffActions:
    def delayed_speech_on():
        """Activates a "temporary speech" mode that can be disabled lazily,
        so that the actual disable command happens after whatever phrase
        finishes next."""
        global delayed_enabled
        if not actions.speech.enabled():
            delayed_enabled = True
            actions.speech.enable()

    def delayed_speech_off():
        """Disables "temporary speech" mode lazily, meaning that the next
        phrase that finishes will turn speech off."""
        global delayed_enabled
        if delayed_enabled:
            delayed_enabled = False
            speech_system.register("post:phrase", do_disable)
