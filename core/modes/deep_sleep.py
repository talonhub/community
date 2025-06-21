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
        Deep sleep requires a longer wakeup command to exit sleep mode (defined in `sleep_mode_deep.talon`), which can help prevent unintended wakeups from conversations, meetings, listening to videos, etc. Instead of invoking this action directly, consider enabling the `user.deep_sleep` tag in applications where unwanted wakeups are more likely or problematic, such as meeting apps. With this tag active, any sleep command triggers deep sleep.
        Users can also manually activate deep sleep by defining a custom voice command using this action.
        Note that when activating the tag on a per application basis, you must remember to explicitly match sleep mode, as command mode is implicitly matched by default.
        Note: If waking up is not done with the user.deep_sleep_disable action, then the deep sleep tag will stay active.
        """
        ctx.tags = ["user.deep_sleep"]
        actions.speech.disable()

    def deep_sleep_disable():
        """Disable deep sleep"""
        ctx.tags = []
        actions.speech.enable()
