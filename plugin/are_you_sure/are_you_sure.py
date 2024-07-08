from talon import Module, Context, imgui
from typing import Callable

mod = Module()
mod.tag('are_you_sure', desc = 'Activates are you sure commands')

class ConfirmationState:
    def __init__(self):
        self.context = Context()
    
    def request_confirmation(self, message: str, on_confirmation, on_disconfirmation):
        self.on_confirmation = on_confirmation
        self.on_disconfirmation = on_disconfirmation
        self.message = message
        self.context.tags = ['user.are_you_sure']
        gui.show()
    
    def confirm(self):
        self.on_confirmation()
        self.cleanup()
    
    def disconfirm(self):
        if self.on_disconfirmation: self.on_disconfirmation()
        self.cleanup()

    def cleanup(self):
        self.context.tags = []
        self.on_confirmation = None
        self.on_disconfirmation = None
        self.message = None
        gui.hide()

    def get_message(self) -> str:
        return self.message

confirmation = ConfirmationState()

@imgui.open(y=0)
def gui(gui: imgui.GUI):
    gui.text(confirmation.get_message())
    gui.line()
    gui.text('Yes I am sure')
    gui.text('No')

@mod.action_class
class Actions:
    def are_you_sure_confirm():
        '''Performs the registered are you sure action'''
        confirmation.confirm()
    
    def are_you_sure_cancel():
        '''Cancels the registered are you sure action'''
        confirmation.disconfirm()

    def are_you_sure_register(message: str, on_confirmation: Callable, on_disconfirmation: Callable = None):
        '''Registers an action to be performed if the user confirms it'''
        confirmation.request_confirmation(message, on_confirmation, on_disconfirmation)