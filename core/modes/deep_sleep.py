from talon import Context, Module, actions

mod = Module()
mod.tag(
    "deep_sleep",
    desc="Tag for enabling deep sleep, which requires a longer wake up command",
)

ctx = Context()


@mod.action_class
class Actions:
    def deep_sleep_enable():
        """Enable deep sleep.
        Deep sleep has the advantage of requiring a longer wakeup command to exit sleep mode, which can help prevent unintended wakeups from conversations, meetings, listening to videos, etc.
        Community does not come with a built in command for activating deep sleep. The expected way to use it is enabling the "user.deep_sleep" tag in applications where unwanted wakeups are more likely or problematic like meeting apps. Users can still enable the action with a command by creating a custom command using this action.
        Note that when activating the tag on a per application basis, you must remember to explicitly match sleep mode as command mode is implicitly matched by default.
        Note: If waking up is not done with the user.deep_sleep_disable action, then the deep sleep tag will stay active.
        """
        ctx.tags = ["user.deep_sleep"]
        actions.speech.disable()

    def deep_sleep_disable():
        """Disable deep sleep"""
        ctx.tags = []
        actions.speech.enable()
