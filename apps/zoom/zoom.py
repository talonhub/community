from talon import Context, Module, actions, app, ctrl, ui
from talon.types.size import Size2d

mod = Module()
mod.tag("meeting_zoom", desc="Tag to indicate that the user is in a Zoom meeting")

ctx = Context()
ctx.matches = r"""
tag: user.meeting_zoom
os: mac
"""

ZOOM_BUNDLE_ID = "us.zoom.xos"


def is_zoom(app):
    return app.bundle == ZOOM_BUNDLE_ID


def zoom_app():
    if apps := ui.apps(bundle=ZOOM_BUNDLE_ID):
        return apps[0]
    return None


def zoom_meeting_window_talon_workaround():
    # Workaround for Talon bug: https://github.com/talonvoice/talon/issues/606
    if meeting_window := zoom_meeting_window():
        return meeting_window
    active_app = ui.active_app()
    if active_app.bundle == ZOOM_BUNDLE_ID:
        ui.apps(bundle="com.apple.loginwindow")[0].focus()
        active_app.focus()
    elif zoom := zoom_app():
        zoom.focus()
        active_app.focus()
    return zoom_meeting_window()


def zoom_window_is_meeting_window(window):
    # Window title is not "Zoom Meeting" in all languages
    # but always starts with "Zoom" (empirically)
    return (
        window.title
        and window.title != "Zoom"
        and (window.title == "Zoom Meeting" or window.title.startswith("Zoom"))
    )


def zoom_meeting_window():
    if zoom := zoom_app():
        for window in zoom.windows():
            if zoom_window_is_meeting_window(window):
                return window
    return None


def is_zoom_meeting_window(window):
    return is_zoom(window.app) and zoom_window_is_meeting_window(window)


def zoom_toggle_mute():
    if zoom := zoom_app():
        ctrl.key_press("a", super=True, shift=True, app=zoom)


def on_win_open(window):
    if is_zoom_meeting_window(window):
        actions.user.meeting_started("zoom", window)


def on_win_close(window):
    if is_zoom_meeting_window(window):
        actions.user.meeting_ended("zoom", window)


def on_ready():
    if meeting_window := zoom_meeting_window():
        actions.user.meeting_started("zoom", meeting_window)

    ui.register("win_open", on_win_open)
    ui.register("win_close", on_win_close)


@ctx.action_class("user")
class UserActions:
    def meeting_is_muted() -> bool:
        if zoom := zoom_app():
            try:
                mute_menu_item = zoom.element.children.find_one(
                    AXRole="AXMenuBar", max_depth=0
                ).children.find_one(
                    AXRole="AXMenuItem", AXMenuItemCmdChar="A", AXMenuItemCmdModifiers=1
                )
                # XXX Replace by word for "unmute" if Zoom UI is not in English
                return mute_menu_item.AXTitle == "Unmute Audio"
            except ui.UIErr:
                pass

        app.notify(
            title="Zoom",
            body="Can’t determine whether Zoom is muted. "
            + "If Zoom isn’t running in English, edit zoom.py.",
        )
        return False

    def meeting_mute():
        if actions.user.meeting_is_muted():
            return
        zoom_toggle_mute()

    def meeting_unmute():
        if not actions.user.meeting_is_muted():
            return
        zoom_toggle_mute()

    def meeting_exit():
        if meeting_window := zoom_meeting_window_talon_workaround():
            meeting_window.focus()
            meeting_window.app.focus()
            meeting_window.close()


app.register("ready", on_ready)
