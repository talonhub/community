from talon import Context, Module, actions, app, speech_system

mod = Module()
ctx_sleep = Context()
ctx_awake = Context()

modes = {
    "presentation": "a more strict form of sleep where only a more strict wake up command works",
}

for key, value in modes.items():
    mod.mode(key, value)

ctx_sleep.matches = r"""
mode: sleep
"""

ctx_awake.matches = r"""
not mode: sleep
"""


@ctx_sleep.action_class("speech")
class ActionsSleepMode:
    def disable():
        actions.app.notify("Talon is already asleep")


@ctx_awake.action_class("speech")
class ActionsAwakeMode:
    def enable():
        actions.app.notify("Talon is already awake")


@mod.action_class
class Actions:
    def talon_mode():
        """For windows and Mac with Dragon, enables Talon commands and Dragon's command mode."""
        actions.speech.enable()

        engine = speech_system.engine.name
        # app.notify(engine)
        if "dragon" in engine:
            if app.platform == "mac":
                actions.user.dragon_engine_sleep()
            elif app.platform == "windows":
                actions.user.dragon_engine_wake()
                # note: this may not do anything for all versions of Dragon. Requires Pro.
                actions.user.dragon_engine_command_mode()

    def dragon_mode():
        """For windows and Mac with Dragon, disables Talon commands and exits Dragon's command mode"""
        engine = speech_system.engine.name
        # app.notify(engine)

        if "dragon" in engine:
            # app.notify("dragon mode")
            actions.speech.disable()
            if app.platform == "mac":
                actions.user.dragon_engine_wake()
            elif app.platform == "windows":
                actions.user.dragon_engine_wake()
                # note: this may not do anything for all versions of Dragon. Requires Pro.
                actions.user.dragon_engine_normal_mode()
