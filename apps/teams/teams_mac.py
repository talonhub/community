from talon import Context, Module, actions, app, cron, ctrl, scope, ui

mod = Module()
mod.tag("meeting_teams", desc="Tag to indicate that the user is in a Teams meeting")

ctx = Context()
ctx.matches = r"""
tag: user.meeting_teams
os: mac
"""

TEAMS_BUNDLE_ID = "com.microsoft.teams"


def is_teams(app):
    return app.bundle == TEAMS_BUNDLE_ID


def teams_app():
    if apps := ui.apps(bundle=TEAMS_BUNDLE_ID):
        return apps[0]
    return None


def teams_window_is_meeting_window(window):
    if not window.title:
        return False

    for identifier in (
        "hangup-button",  # Hang up button in a meeting
        "prejoin-join-button",  # "Join now" button
        "share_meeting_invite_dialog_subtitle",  # "Invite people to join you"
    ):
        try:
            if window.element.children.find_one(AXDOMIdentifier=identifier):
                return True
        except ui.UIErr:
            pass
    return False


def teams_meeting_window():
    if teams := teams_app():
        for window in teams.windows():
            if teams_window_is_meeting_window(window):
                return window
    return None


def is_teams_meeting_window(window):
    return is_teams(window.app) and teams_window_is_meeting_window(window)


def teams_toggle_mute():
    if teams := teams_app():
        ctrl.key_press("m", super=True, shift=True, app=teams)


def on_win_open(window):
    if not is_teams(window.app):
        return

    attempts = 10

    def set_tag_if_teams_meeting_window():
        nonlocal attempts
        # wait for the DOM to be constructed inside the window
        attempts -= 1
        if attempts >= 0:
            if window.title == "Teams":
                return
            try:
                # Use "at least one button exists inside the web area" as a proxy for "finished loading"
                web_area = window.element.children.find_one(
                    AXRole="AXWebArea", max_depth=0
                )
                button = web_area.children.find_one(AXRole="AXButton")
            except ui.UIErr:
                return
            if teams_window_is_meeting_window(window):
                actions.user.meeting_started("teams", window)
        cron.cancel(job)

    job = cron.interval("100ms", set_tag_if_teams_meeting_window)


def on_win_close(window):
    if not is_teams(window.app):
        return

    for teams_window in window.app.windows():
        if teams_window_is_meeting_window(teams_window):
            return

    if "user.meeting_teams" in scope["tag"]:
        actions.user.meeting_ended("teams", window)


def on_ready():
    if meeting_window := teams_meeting_window():
        actions.user.meeting_started("teams", meeting_window)

    ui.register("win_open", on_win_open)
    ui.register("win_close", on_win_close)


@ctx.action_class("user")
class UserActions:
    def meeting_is_muted() -> bool:
        if meeting_window := teams_meeting_window():
            try:
                mic_button = meeting_window.element.children.find_one(
                    AXRole="AXButton", AXDOMIdentifier="microphone-button"
                )
                mic_button_label = mic_button.AXDescription
                # XXX Replace by words for "mute"/"unmute" if Teams UI is not in English
                if mic_button_label.startswith("Unmute"):
                    return True
                if mic_button_label.startswith("Mute"):
                    return False
            except ui.UIErr:
                pass
            app.notify(
                title="Teams",
                body="Can’t determine whether Teams is muted. "
                + "If Teams isn’t running in English, edit teams_mac.py.",
            )
        else:
            app.notify(
                title="Teams", body="Can’t find a Teams meeting window. Try again?"
            )

        return False

    def meeting_mute():
        if actions.user.meeting_is_muted():
            return
        teams_toggle_mute()

    def meeting_unmute():
        if not actions.user.meeting_is_muted():
            return
        teams_toggle_mute()

    def meeting_exit():
        if teams := teams_app():
            ctrl.key_press("h", super=True, shift=True, app=teams)


app.register("ready", on_ready)
