from talon import Module, Context, actions

mod = Module()
mod.tag("deep_sleep", desc="Tag for enabling deep sleep, which requires a longer wake up command")

ctx = Context()

@mod.action_class
class Actions:
    def deep_sleep_enable():
        """Enable deep sleep"""
        ctx.tags = ["user.deep_sleep"]
        actions.speech.disable()

    def deep_sleep_disable():
        """Disable deep sleep"""
        ctx.tags = []
        actions.speech.enable()