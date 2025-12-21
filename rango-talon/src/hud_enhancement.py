from talon import actions, scope, app, cron, ui
import os

# Add the rango toggle button to the status bar if requested
class RangoPoller:
    content = None
    enabled = False
    button_added = False
    mode_direct = False
    scope_check_job = None

    def toggle_rango(self):
        ui.active_window().focus()
        actions.user.rango_toggle_hints()

    def scope_check(self):
        if "browser" in scope.get("tag"):
            mode_direct = "user.rango_direct_clicking" in scope.get("tag")        
            if not self.button_added or self.mode_direct != mode_direct:
                self.mode_direct = mode_direct
                dir_path = os.path.dirname(os.path.realpath(__file__))
                self.button_added = True
                image_name = "rango-direct.png" if mode_direct else "rango.png"

                toggle_function = lambda _, _2, self=self: self.toggle_rango()
                status_icon = self.content.create_status_icon("rango_toggle", os.path.join(dir_path, "images", image_name), None, "Rango toggle", toggle_function )
                self.content.publish_event("status_icons", status_icon.topic, "replace", status_icon)
        elif self.button_added:
            self.button_added = False
            self.content.publish_event("status_icons", "rango_toggle", "remove")

    def enable(self):
        if not self.enabled:
           self.enabled = True
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
    if "user.talon_hud_available" in scope.get("tag") and \
        scope.get("user.talon_hud_version") != None and scope.get("user.talon_hud_version") >= TALON_HUD_RELEASE_PERSISTENCE:
        actions.user.hud_add_poller('rango', RangoPoller(), True)
        actions.user.hud_activate_poller('rango')

app.register("ready", talon_hud_ready)
