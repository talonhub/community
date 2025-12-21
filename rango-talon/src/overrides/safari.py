from talon import Context, actions
from .safari_version import get_safari_version

ctx = Context()
ctx.matches = r"""
tag: browser
app: safari
"""

_hotkey = (
    "ctrl-shift-keypad_3" if get_safari_version().startswith("18.") else "ctrl-shift-3"
)


@ctx.action_class("user")
class UserActions:
    def rango_type_hotkey():
        actions.key(_hotkey)
