from talon import actions, scope, app, cron, ui
import os

# Add the rango toggle button to the status bar if requested
class EyeZoomMousePoller:
    content = None
    enabled = False
    button_added = False
    scope_check_job = None
    zoom_mouse_status = False
    control_mouse_status = False

    def toggle_eye_zoom_mouse(self):
        actions.tracking.control_zoom_toggle()

    def scope_check(self):
        control_mouse_enabled = (
            actions.tracking.control_enabled() or actions.tracking.control1_enabled()
        )
        zoom_mouse_enabled = actions.tracking.control_zoom_enabled()
        if zoom_mouse_enabled or control_mouse_enabled:
            if (
                not self.button_added
                or self.zoom_mouse_status != zoom_mouse_enabled
                or control_mouse_enabled != self.control_mouse_status
            ):
                self.zoom_mouse_status = zoom_mouse_enabled
                self.control_mouse_status = control_mouse_enabled
                dir_path = os.path.dirname(os.path.realpath(__file__))
                self.button_added = True
                image_name = (
                    "eye_zoom.png"
                    if actions.tracking.control_zoom_enabled()
                    else "eye_control.png"
                )

                # toggle_function = lambda _, _2, self=self: self.toggle_eye_zoom_mouse()
                status_icon = self.content.create_status_icon(
                    "eye_zoom_mouse_toggle",
                    os.path.join(dir_path, image_name),
                    None,
                    "eye zoom mouse toggle",
                    None,
                )
                self.content.publish_event(
                    "status_icons", status_icon.topic, "replace", status_icon
                )
        elif self.button_added:
            print("removing icon")
            self.button_added = False
            self.content.publish_event(
                "status_icons", "eye_zoom_mouse_toggle", "remove"
            )

    def enable(self):
        if not self.enabled:
            self.enabled = True
            print("enabled")
            self.scope_check_job = cron.interval("300ms", self.scope_check)
            self.scope_check()

    def disable(self):
        if self.enabled:
            self.enabled = False
            self.button_added = False
            cron.cancel(self.scope_check_job)
            self.scope_check_job = None

    def destroy(self):
        self.disable()


def talon_hud_ready():
    # Check if Talon HUD is available to the user
    TALON_HUD_RELEASE_PERSISTENCE = 6
    if (
        "user.talon_hud_available" in scope.get("tag")
        and scope.get("user.talon_hud_version") != None
        and scope.get("user.talon_hud_version") >= TALON_HUD_RELEASE_PERSISTENCE
    ):
        actions.user.hud_add_poller("eye_zoom_mouse", EyeZoomMousePoller(), True)
        actions.user.hud_activate_poller("eye_zoom_mouse")


app.register("ready", talon_hud_ready)
