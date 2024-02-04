from talon import Context, Module, app, actions, speech_system, scope

mod = Module()

ctx_sleep = Context()
ctx_awake = Context()

tags = {
    # "admin": "enable extra administration commands terminal (docker, etc)",
    # "debug": "a way to force debugger commands to be loaded",
    # "gdb": "a way to force gdb commands to be loaded",
    # "ida": "a way to force ida commands to be loaded",
    # "presentation": "a more strict form of sleep where only a more strict wake up command works",
}

for key, value in tags.items():
    mod.tags(key, value)

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
        actions.user.microphone_preferred()
        engine = speech_system.engine.name
        # app.notify(engine)
        if "dragon" in engine:
            if app.platform == "mac":
                actions.user.engine_sleep()
            elif app.platform == "windows":
                actions.user.engine_wake()
                # note: this may not do anything for all versions of Dragon. Requires Pro.
                actions.user.engine_mimic("switch to command mode")
        else:
            actions.mode.disable("sleep")
            actions.mode.disable("dictation")
            actions.mode.enable("command")
            actions.user.code_clear_language_mode()

    def dragon_mode():
        """For windows and Mac with Dragon, disables Talon commands and exits Dragon's command mode"""
        engine = speech_system.engine.name
        # app.notify(engine)

        if "dragon" in engine:
            # app.notify("dragon mode")
            actions.speech.disable()
            if app.platform == "mac":
                actions.user.engine_wake()
            elif app.platform == "windows":
                actions.user.engine_wake()
                # note: this may not do anything for all versions of Dragon. Requires Pro.
                actions.user.engine_mimic("start normal mode")
        else:
            actions.mode.disable("sleep")
            actions.mode.enable("dictation")
            actions.mode.disable("command")
            actions.user.code_clear_language_mode()

    def wake_or_sleep():
        """toggles wake or sleep"""
        modes = scope.get("mode")
        # print(str(modes))
        if not actions.speech.enabled():
            actions.user.welcome_back()
            actions.user.microphone_preferred()
            actions.user.connect_ocr_eye_tracker()
        else:
            actions.user.sleep_all()
            actions.sound.set_microphone("None")
            actions.user.disconnect_ocr_eye_tracker()

    def dictation_or_command_toggle():
        """toggles dictation or command"""
        modes = scope.get("mode")
        # print(str(modes))
        if "command" in modes:
            actions.mode.enable("dictation")
            actions.mode.disable("command")
            actions.user.hide_gaze_ocr_options()
        else:
            actions.mode.enable("command")
            actions.mode.disable("dictation")

    def welcome_back():
        """Enables all things"""
        actions.user.mouse_wake()
        if "user.talon_hud_available" in scope.get("tag"):
            if "rust" != app.branch:
                actions.user.hud_enable()
        # user.history_enable()
        actions.user.talon_mode()
        actions.mode.enable("noise")

    def sleep_all():
        """Disables all things"""
        actions.user.switcher_hide_running()
        # todo: remove when the talon_hud perf is fixed on rust branch
        if "user.talon_hud_available" in scope.get("tag"):
            actions.user.hud_disable()
        # user.history_disable()
        actions.user.homophones_hide()
        actions.user.help_hide()
        actions.user.mouse_sleep()
        actions.speech.disable()
        actions.user.engine_sleep()
        actions.mode.disable("noise")
        actions.sound.set_microphone("None")
        actions.user.disconnect_ocr_eye_tracker()
