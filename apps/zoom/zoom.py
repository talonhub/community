from talon import Context, Module, app, ui

mod = Module()
mod.tag("meeting_zoom", desc="Tag to indicate that the user is in a zoom meeting")

global_ctx = Context()

ctx = Context()
ctx.matches = r"""
tag: user.meeting_zoom
"""


def is_zoom(app):
    return app.bundle == "us.zoom.xos"


def is_zoom_meeting(win):
    return is_zoom(win.app) and win.title == "Zoom Meeting"


def on_win_open(win):
    if is_zoom_meeting(win):
        global_ctx.tags = ["user.meeting_zoom"]


def on_win_close(win):
    if is_zoom_meeting(win):
        global_ctx.tags = []


@ctx.action_class("user")
class UserActions:
    def meeting_mute():
        app.notify("Mute meeting")

    def meeting_unmute():
        app.notify("Unmute meeting")

    def meeting_exit():
        app.notify("Exit meeting")


ui.register("win_open", on_win_open)
ui.register("win_close", on_win_close)
