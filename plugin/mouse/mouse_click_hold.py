from talon import Context, Module, actions, ctrl, settings

mod = Module()

mod.setting(
    "mouse_click_hold",
    type=int,
    default=0,
    desc="Duration to hold mouse clicks in milliseconds. 0 means no hold. In some full-screen applications, particularly games, mouse clicks may not be recognized unless held for a short duration. If this occurs, try starting with setting this to 16.",
)

ctx = Context()


@ctx.action_class("main")
class MainActions:
    def mouse_click(button: int = 0):
        hold_duration = settings.get("user.mouse_click_hold")

        if hold_duration < 1:
            actions.next(button)
        else:
            ctrl.mouse_click(button=button, hold=hold_duration * 1000)
