from talon import Context, Module, actions
import os

#


mod = Module()
mod.list("launch_command", desc="List of applications to launch")
mod.list("directories", desc="List of directories")

portal_name = mod.setting(
    "system_portal_name",
    type=str,
    default="firefox",
    desc="The default portal to switch to",
)
coder_name = mod.setting(
    "system_coder_name",
    type=str,
    default="code",
    desc="The default coder to switch to",
)
ctx = Context()
ctx.lists["self.launch_command"] = {}
ctx.lists["self.directories"] = {}


@mod.action_class
class Actions:
    def exec(command: str):
        """Run command"""
        os.system(command)

    def system_shutdown():
        """Shutdown operating system"""

    def system_restart():
        """Restart operating system"""

    def system_hibernate():
        """Hibernate operating system"""

    def system_lock():
        """Locks the OS"""

    def system_show_desktop():
        """Reveals the desktop"""

    def system_task_manager():
        """starts the task manager"""

    def system_task_view():
        """Mission control/super-tab equivalent"""

    def system_switcher():
        """Mission control/ctl-alt-tab equivalent"""

    def system_search():
        """Triggers system search (e.g. spotlight/powerrunner)"""

    def system_last_application():
        """triggers alt-tab"""

    def system_open_directory(path: str):
        """opens directory in default file manager"""

    def system_show_clipboard():
        """opens the systems default clipboard or equivalent"""

    def system_show_portal(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        actions.user.switcher_focus(portal_name.get())
        actions.sleep("250ms")
        actions.user.parse_phrase(phrase or "")

    def system_show_coder(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        actions.user.switcher_focus(coder_name.get())
        actions.sleep("250ms")
        actions.user.parse_phrase(phrase or "")
