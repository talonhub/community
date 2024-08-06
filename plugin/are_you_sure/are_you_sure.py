from typing import Callable

from talon import Context, Module, actions, imgui

mod = Module()
mod.tag("are_you_sure", desc="Activates are you sure commands")


class ConfirmationState:
    def __init__(self):
        self.context = Context()

    def request_confirmation(self, message: str, on_confirmation, on_disconfirmation):
        self.on_confirmation = on_confirmation
        self.on_cancel = on_disconfirmation
        self.message = message
        self.context.tags = ["user.are_you_sure"]
        gui.show()

    def confirm(self):
        self.on_confirmation()
        self.cleanup()

    def cancel(self):
        if self.on_cancel:
            self.on_cancel()
        self.cleanup()

    def cleanup(self):
        self.context.tags = []
        self.on_confirmation = None
        self.on_cancel = None
        self.message = None
        gui.hide()

    def get_message(self) -> str:
        return self.message


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
