from talon import Context, actions, ui, Module, app
import time

mod = Module()


@mod.action_class
class Actions:
    def focus_puppy():
        """this is out as description"""
        window = actions.user.find_window(
            bundle="net.kovidgoyal.kitty",
            window_name_regex="Talon-Kitty-Window",
            negate_regex=True,
        )
        print(window)
        if window is not None:
            actions.user.switcher_focus_window(window)

    def focus_talon_window():
        """this is out as description"""
        window = actions.user.find_window(
            bundle="net.kovidgoyal.kitty",
            window_name_regex="Talon-Kitty-Window",
            negate_regex=False,
        )
        print(window)
        if window is not None:
            actions.user.switcher_focus_window(window)

    def maciek_speech_toggle():
        """
        Vanilla actions.speech.toggle() does not handle well situations
        where we are in the polish dictation mode. This fixes that.
        """
        if actions.speech.enabled():
            actions.user.command_mode()
            actions.speech.disable()
        else:
            actions.speech.enable()
