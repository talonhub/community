from talon import tap
from talon import ctrl

def on_move(e):
    buttons = ctrl.mouse_buttons_down()
    # print(str(ctrl.mouse_buttons_down()))                                                                                                                                                                                                                                   
    if not e.flags & tap.DRAG and buttons:
        e.flags |= tap.DRAG
        # buttons is a set now                                                                                                                                                                                                                                                
        e.button = list(buttons)[0]
        e.modify()

tap.register(tap.MMOVE | tap.HOOK, on_move)