"""
Map noises (like pop) to actions so they can have contextually differing behavior
"""

from talon import Module, actions, cron, noise, settings

mod = Module()
hiss_cron = None

mod.setting(
    "hiss_scroll_debounce_time",
    type=int,
    default=100,
    desc="How much time a hiss must last for to be considered a hiss rather than part of speech, in ms",
)


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
        hiss_cron = cron.after(
            str(f"{settings.get('user.hiss_scroll_debounce_time')}ms"),
            lambda: actions.user.noise_trigger_hiss(active),
        )
    else:
        cron.cancel(hiss_cron)
        actions.user.noise_trigger_hiss(active)


noise.register("pop", lambda _: actions.user.noise_trigger_pop())
noise.register("hiss", noise_trigger_hiss_debounce)
