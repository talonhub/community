from talon import Context, Module, actions, app, imgui, scope, settings, speech_system

mod = Module()
ctx = Context()
ctx_sleep = Context()
ctx_awake = Context()
ctx_deep_sleep_asleep = Context()
ctx_deep_sleep_awake = Context()

modes = {
    "presentation": "a more strict form of sleep where only a more strict wake up command works",
}

for key, value in modes.items():
    mod.mode(key, value)

mod.tag(
    "deep_sleep",
    desc="This requires using the standard wakeup action multiple times to exit sleep mode",
)

mod.setting(
    "deep_sleep_wake_ups_required",
    type=int,
    default=3,
    desc="The number of consecutive wake ups required to exit deep sleep mode",
)

wake_ups_remaining_to_exit_deep_sleep: int = 0

ctx_deep_sleep_asleep.matches = r"""
tag: user.deep_sleep
mode: sleep
"""

ctx_deep_sleep_awake.matches = r"""
tag: user.deep_sleep
not mode: sleep
"""

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


def cleanup_deep_sleep_state():
    """Resets deep sleep related state. Intended to be used after waking up from deep sleep."""
    actions.user.sleep_reset_deep_sleep_counter()
    if deep_sleep_gui.showing:
        deep_sleep_gui.hide()
    ctx.tags = []

def setup_deep_sleep_state():
    """Sets up deep sleep related state. Intended to be used when entering deep sleep. This must be called after sleep mode is enabled because the graphics will try to clean up the deep sleep state if talon is awake while it is showing."""
    ctx.tags = ["user.deep_sleep"]
    actions.user.sleep_reset_deep_sleep_counter()
    deep_sleep_gui.show()

@mod.action_class
class Actions:
    def talon_mode():
        """For windows and Mac with Dragon, enables Talon commands and Dragon's command mode."""
        actions.user.sleep_wake_up_immediately()

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

    def sleep_wake_up():
        """Wakes up Talon from sleep mode"""
        actions.speech.enable()

    def sleep_reset_deep_sleep_counter():
        """Resets the deep sleep wake up counter"""
        global wake_ups_remaining_to_exit_deep_sleep
        wake_ups_remaining_to_exit_deep_sleep = settings.get(
            "user.deep_sleep_wake_ups_required"
        )

    def sleep_wake_up_immediately():
        """Wakes up Talon from sleep mode bypassing the deep sleep wake up counter"""
        cleanup_deep_sleep_state()
        actions.speech.enable()

    def sleep_enable():
        """Puts Talon to sleep mode"""
        actions.speech.disable()

    def sleep_enable_deep_sleep():
        """Puts Talon to sleep mode with deep sleep enabled"""
        actions.user.sleep_enable()
        setup_deep_sleep_state()

@ctx_deep_sleep_asleep.action_class("user")
class ActionsDeepSleep:
    def sleep_wake_up():
        global wake_ups_remaining_to_exit_deep_sleep
        wake_ups_remaining_to_exit_deep_sleep -= 1
        if wake_ups_remaining_to_exit_deep_sleep <= 0:
            actions.user.sleep_wake_up_immediately()

@ctx_deep_sleep_awake.action_class("user")
class ActionsDeepAwake:
    def sleep_enable():
        actions.next()
        setup_deep_sleep_state()

# Going to sleep with the deep sleep tag active will require the user to wake up multiple times to exit sleep mode, but if they use speech.disable() without this, the graphical interface will not display and the counter may be in a bad state
@ctx_deep_sleep_awake.action_class("speech")
class ActionsDeepAwakeSpeech:
    def disable():
        actions.next()
        setup_deep_sleep_state()

@imgui.open(y=0)
def deep_sleep_gui(gui: imgui.GUI):
    global wake_ups_remaining_to_exit_deep_sleep
    gui.text("Deep sleep")
    gui.text(
        f"Consecutive Wake Ups Needed to Exit Deep Sleep: {wake_ups_remaining_to_exit_deep_sleep}"
    )
    #This allows cleaning deep sleep state if the user wakes up talon through some other means than the actions defined here:
    if actions.speech.enabled():
        cleanup_deep_sleep_state()
    elif gui.button("Wake Up Now"):
        actions.user.sleep_wake_up_immediately()