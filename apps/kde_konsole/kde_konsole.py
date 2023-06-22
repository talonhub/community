from talon import Context, actions

ctx = Context()
ctx.matches = r"""
app.name: konsole
"""


@ctx.action_class("user")
class user_actions:
    # tabs-tag functions implementations
    def tab_jump(number):
        actions.key(f"alt-{number}")

    # tab_final is not supported by konsole by default
    # but short cut can be configured


@ctx.action_class("app")
class app_actions:
    # tabs-tag functions implementations
    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_previous():
        actions.key("shift-left")

    def tab_next():
        actions.key("shift-right")

    def tab_close():
        actions.key("ctrl-shift-w")

    def tab_reopen():
        # TODO: decide whether this notification is good style
        # (if this function wouldn't be defined here a wrong default would be activated)
        actions.app.notify("tab reopen is not possible in kde konsole")

    def window_open():
        actions.key("ctrl-shift-n")


# this overwrites the unfitting parts of linux/edit.py
@ctx.action_class("edit")
class EditActions:
    def page_down():
        actions.key("shift-pagedown")

    def page_up():
        actions.key("shift-pageup")

    def paste():
        actions.key("ctrl-shift-v")

    def copy():
        actions.key("ctrl-shift-c")

    def find(text: str):
        actions.key("ctrl-shift-f")
        if str:
            actions.insert(text)

    # TODO: fix select line and other selection (like shift-right)
    # see: https://unix.stackexchange.com/questions/485536/kde-konsole-swallows-shift-left-and-shift-right
    #  also fix extend_left and co
