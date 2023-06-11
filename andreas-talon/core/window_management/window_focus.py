from talon import Module, Context, ui, actions
from talon.grammar import Phrase


mod = Module()
ctx = Context()


def focus_name(name: str):
    app = actions.user.get_app(name)
    # Focus next window on same app
    if app == ui.active_app():
        actions.app.window_next()
    # Focus app
    else:
        actions.user.focus_app(app)
    actions.user.help_running_apps_hide()


@mod.action_class
class Actions:
    def window_focus_last():
        """Switch focus to last window"""
        actions.key("alt-tab")

    def window_focus_name(name: str, phrase: Phrase = None):
        """Focus application named <name>"""
        focus_name(name)

        if phrase:
            actions.sleep("300ms")
            actions.user.rephrase(phrase)

    def focus_number(number: int):
        """Focus application number <number>"""
        names = list(actions.user.get_running_applications().values())
        if number > 0 and number <= len(names):
            focus_name(names[number - 1])
