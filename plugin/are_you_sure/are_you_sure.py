from collections.abc import Callable
from typing import Optional

from talon import Context, Module, actions

from ...core.gui.gui import create_italic_text, open_gui

mod = Module()
mod.tag("are_you_sure", desc="Activates are you sure commands")


class ConfirmationState:
    message: str = ""
    on_confirmation: Optional[Callable[[], None]] = None
    on_cancel: Optional[Callable[[], None]] = None

    def __init__(self):
        self.context = Context()

    def request_confirmation(
        self,
        message: str,
        on_confirmation: Callable[[], None],
        on_disconfirmation: Optional[Callable[[], None]] = None,
    ):
        self.on_confirmation = on_confirmation
        self.on_cancel = on_disconfirmation
        self.message = message
        self.context.tags = ["user.are_you_sure"]
        if gui.showing:
            gui.auto_size_next_frame()
            gui.refresh()
        gui.show()

    def confirm(self):
        if self.on_confirmation:
            self.on_confirmation()
        self.cleanup()

    def cancel(self):
        if self.on_cancel:
            self.on_cancel()
        self.cleanup()

    def cleanup(self):
        self.context.tags = []
        self.message = ""
        self.on_confirmation = None
        self.on_cancel = None
        gui.hide()

    def get_message(self) -> str:
        return self.message


confirmation = ConfirmationState()


@open_gui(y=0)
async def gui(ui, ui_wrapper):
    ui_wrapper.title(confirmation.get_message())
    accept_command_text = create_italic_text("Yes I am sure")
    if ui_wrapper.button(accept_command_text):
        actions.user.are_you_sure_confirm()
    cancel_command_text = create_italic_text("Cancel")
    if ui_wrapper.button(cancel_command_text):
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
        message: str,
        on_confirmation: Callable[[], None],
        on_cancel: Optional[Callable[[], None]] = None,
    ):
        """Sets the action to be performed on user confirmation.
        message: the message to display to the user
        on_confirmation: the action to perform if the user confirms
        on_cancel: (optional) the action to perform if the user cancels
        This only supports working with a single action at a time and
        does not work with chaining as it is intended to be used with particularly destructive actions.
        """
        confirmation.request_confirmation(message, on_confirmation, on_cancel)
