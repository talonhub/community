"""
Map noises (like pop) to actions so they can have contextually differing behavior
"""

from talon import Module, actions, cron, noise

mod = Module()
hiss_cron = None


@mod.action_class
class Actions:
    def noise_trigger_pop():
        """
        Called when the user makes a 'pop' noise. Listen to
        https://noise.talonvoice.com/static/previews/pop.mp3 for an
        example.
        """
        actions.skip()

    def noise_trigger_hiss(active: bool):
        """
        Called when the user makes a 'hiss' noise. Listen to
        https://noise.talonvoice.com/static/previews/hiss.mp3 for an
        example.
        """
        actions.skip()


def noise_trigger_hiss_debounce(active: bool):
    """Since the hiss noise triggers while you're talking we need to debounce it"""
    global hiss_cron
    if active:
        hiss_cron = cron.after("100ms", lambda: actions.user.noise_trigger_hiss(active))
    else:
        cron.cancel(hiss_cron)
        actions.user.noise_trigger_hiss(active)


noise.register("pop", lambda _: actions.user.noise_trigger_pop())
noise.register("hiss", noise_trigger_hiss_debounce)
