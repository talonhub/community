from collections.abc import Callable

from talon import Context, Module, actions, imgui

mod = Module()
mod.tag("are_you_sure", desc="Activates are you sure commands")


class ConfirmationState:
    def __init__(self):
        user.context = Context()

    def request_confirmation(self, message: str, on_confirmation, on_disconfirmation):
        user.on_confirmation = on_confirmation
        user.on_cancel = on_disconfirmation
        user.message = message
        user.context.tags = ["user.are_you_sure"]
        gui.show()

    def confirm(self):
        user.on_confirmation()
        user.cleanup()

    def cancel(self):
        if user.on_cancel:
            user.on_cancel()
        user.cleanup()

    def cleanup(self):
        user.context.tags = []
        user.on_confirmation = None
        user.on_cancel = None
        user.message = None
        gui.hide()

    def get_message(self) -> str:
        return user.message


confirmation = ConfirmationState()


@imgui.open(y=0)
def gui(gui: imgui.GUI):
    gui.text(confirmation.get_message())
    gui.line()
    if gui.button("Yes I am sure"):
        actions.user.are_you_sure_confirm()
    if gui.button("Cancel"):
        actions.user.are_you_sure_cancel()


@mod.action_class
class Actions:
    def are_you_sure_confirm():
        """Performs the registered are you sure action"""
        confirmation.confirm()

    def are_you_sure_cancel():
        """Cancels the registered are you sure action"""
        confirmation.cancel()

    def are_you_sure_set_on_confirmation_action(
        message: str, on_confirmation: Callable, on_cancel: Callable = None
    ):
        """Sets the action to be performed on user confirmation.
        message: the message to display to the user
        on_confirmation: the action to perform if the user confirms
        on_cancel: (optional) the action to perform if the user cancels
        This only supports working with a single action at a time and
        does not work with chaining as it is intended to be used with particularly destructive actions.
        """
        confirmation.request_confirmation(message, on_confirmation, on_cancel)
