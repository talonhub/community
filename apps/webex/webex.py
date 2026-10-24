from talon import Context, Module, actions, app, ctrl, ui

mod = Module()
mod.tag("meeting_webex", desc="Tag to indicate that the user is in a Webex meeting")

ctx = Context()
ctx.matches = r"""
tag: user.meeting_webex
os: mac
"""

WEBEX_MEETINGS_BUNDLE_ID = "com.webex.meetingmanager"


def is_webex_meetings(app):
    return app.bundle == WEBEX_MEETINGS_BUNDLE_ID


def webex_meetings_app():
    if apps := ui.apps(bundle=WEBEX_MEETINGS_BUNDLE_ID):
        return apps[0]
    return None


def webex_meetings_window_is_meeting_window(window):
    return window.title == "Webex" or window.element.get("AXIdentifier") in (
        "Acc_FIT_Win",
        "Acc_FloatingWidget_Win",
    )


def webex_meetings_window():
    if webex_meetings := webex_meetings_app():
        for window in webex_meetings.windows():
            if webex_meetings_window_is_meeting_window(window):
                return window
    return None


def is_webex_meeting_window(window):
    return is_webex_meetings(window.app) and webex_meetings_window_is_meeting_window(
        window
    )


def webex_toggle_mute():
    if webex_meetings := webex_meetings_app():
        ctrl.key_press("m", super=True, shift=True, app=webex_meetings)


def on_win_open(window):
    if is_webex_meeting_window(window):
        actions.user.meeting_started("webex", window)


def on_win_close(window):
    if is_webex_meeting_window(window):
        actions.user.meeting_ended("webex", window)


def on_ready():
    if meeting_window := webex_meetings_window():
        actions.user.meeting_started("webex", meeting_window)

    ui.register("win_open", on_win_open)
    ui.register("win_close", on_win_close)


@ctx.action_class("user")
class UserActions:
    def meeting_is_muted() -> bool:
        if webex_meetings := webex_meetings_app():
            try:
                mute_menu_item = webex_meetings.element.children.find_one(
                    AXRole="AXMenuBar", max_depth=0
                ).children.find_one(
                    AXRole="AXMenuItem", AXMenuItemCmdChar="M", AXMenuItemCmdModifiers=1
                )
                return not mute_menu_item.AXEnabled
            except ui.UIErr:
                pass

        app.notify(
            title="Webex",
            body="Can’t determine whether Webex is muted. Is the meeting started?",
        )
        return False

    def meeting_mute():
        if actions.user.meeting_is_muted():
            return
        webex_toggle_mute()

    def meeting_unmute():
        if not actions.user.meeting_is_muted():
            return
        webex_toggle_mute()

    def meeting_exit():
        if webex_meetings := webex_meetings_app():
            webex_meetings.quit()


app.register("ready", on_ready)
