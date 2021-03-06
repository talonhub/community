from talon import Module, Context, actions, app

mod = Module()


@mod.action_class
class Actions:
    def alveolar_click():
        """Responds to an alveolar click"""
        app.notify("Alveolar click")

    def postalveolar_click():
        """Responds to an postalveolar click"""
        actions.core.repeat_phrase(1)