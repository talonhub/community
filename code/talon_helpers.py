from talon import Context, actions, ui, Module, app, clip
import os

mod = Module()


@mod.action_class
class Actions:
    def talon_add_context_clipboard():
        """Adds os-specific context info to the clipboard"""
        friendly_name = actions.app.name()
        executable = actions.app.executable().split(os.path.sep)[-1]
        if app.platform != "windows":
            result = "os: {}\napp: {}\ntitle: {}".format(
                app.platform, friendly_name, actions.win.title()
            )

        # on windows, it's best to include both the friendly name and executable name in case the muicache breaks....
        else:
            result = "os: {}\napp: {}\napp: {}\ntitle: {}".format(
                app.platform, friendly_name, executable, actions.win.title()
            )

        clip.set(result)
