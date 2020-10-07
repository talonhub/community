from talon import ctrl, ui, Module, Context, actions, clip, app

ctx = Context()
mod = Module()

# 1password
mod.apps.microsoft_edge = "app.name: Microsoft Edge"
mod.apps.microsoft_edge = "app.name: MicrosoftEdge.exe"
mod.apps.microsoft_edge = "app.name: msedge.exe"


@ctx.action_class("user")
class user_actions:
    def tab_jump(number: int):
        if number < 9:
            if app.platform == "mac":
                actions.key("cmd-{}".format(number))
            else:
                actions.key("ctrl-{}".format(number))

    def tab_final():
        if app.platform == "mac":
            actions.key("cmd-9")
        else:
            actions.key("ctrl-9")
