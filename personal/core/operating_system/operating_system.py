from talon import Context, Module, actions, ui, app
import os

#


mod = Module()
mod.list("system_setting", desc="List of system level configuration setting to launch")
mod.list("system_directories", desc="List of system directories. By default, these are generated on start per-OS")
mod.list("user_directories", desc="List of user-defined directories. Empty by default, used to expand the available paths")


portal_name = mod.setting(
    "system_portal_name",
    type=str,
    default="chrome",
    desc="The default portal to switch to",
)
email_web_address = mod.setting(
    "email_web_address",
    type=str,
    default="https://mail.google.com/",
    desc="the default web mail client",
)
coder_name = mod.setting(
    "system_coder_name",
    type=str,
    default="code",
    desc="The default coder to switch to",
)
messaging_application = mod.setting(
    "system_messaging_application_name",
    type=str,
    default="teams",
    desc="The default messaging application to switch to",
)

settings_application = mod.setting(
    "system_settings_application_name",
    type=str,
    default="settings",
    desc="The default messaging application to switch to",
)

ctx = Context()
ctx.lists["self.system_setting"] = {}
ctx.lists["self.system_directories"] = {}

@mod.capture(rule="{user.system_directories}")
def system_diretory(m) -> str:
    return m.system_directories

@mod.capture(rule="{user.user_directories}")
def user_directory(m) -> str:
    return m.user_directories

@mod.capture(rule="<user.user_directory> | <user.system_diretory>")
def directory(m) -> str:
    return str(m)

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

    def system_kill_focused_application():
        """Kills the focused application"""

    def system_show_settings():
        """opens the systems default settings applications"""
        actions.user.switcher_focus(settings_application.get())

    def system_show_portal(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        actions.user.switcher_focus(portal_name.get())
        actions.sleep("250ms")
        if phrase:
            actions.user.parse_phrase(phrase or "")

    def system_show_coder(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        is_running = actions.user.switcher_focus(coder_name.get())
        actions.sleep("250ms")

        actions.user.parse_phrase(phrase or "")

    def system_show_messenger():
        """Opens the default browser for the up operating system and performs the phrase command"""
        # is_running = actions.user.switcher_focus(messaging_application.get())
        success = actions.user.switcher_focus_window_by_name(
            portal_name.get(), "https://teams.microsoft.com/"
        )
        if not success:
            actions.user.open_new_url("https://teams.microsoft.com/")

    def system_show_slacker():
        """Opens the default browser for the up operating system and performs the phrase command"""
        success = actions.user.switcher_focus_window_by_name(
            portal_name.get(), "https://app.slack.com/"
        )
        if not success:
            actions.user.open_url("https://app.slack.com/")
        # is_running = actions.user.switcher_focus("slack")
        # actions.sleep("250ms")
        # if is_running:
        #     actions.user.parse_phrase(phrase or "")

    def system_show_email():
        """Opens the defaul6t browser for the up operating system and performs the phrase command"""
        success = actions.user.switcher_focus_window_by_name(
            portal_name.get(), email_web_address.get()  # "https://outlook.office.com/"
        )
        if not success:
            actions.user.open_new_url(email_web_address.get())
            # is_running = actions.user.switcher_focus("gmail")

        # is_running = actions.user.switcher_focus("outlook")
        # actions.sleep("250ms")
        # if is_running:
        #     actions.user.parse_phrase(phrase or "")

    def system_show_gitter(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        is_running = actions.user.switcher_focus("git hub")
        actions.sleep("250ms")
        if is_running:
            actions.user.parse_phrase(phrase or "")

    def system_show_taskmanager(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        is_running = actions.user.switcher_focus("task manager")
        actions.sleep("250ms")
        if is_running:
            actions.user.parse_phrase(phrase or "")

    def system_taskmanager_find_focused_application(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        current_application = actions.app.executable().split("\\")[-1]

        is_running = actions.user.switcher_focus("task manager")
        actions.sleep("250ms")
        actions.key("ctrl-f")
        actions.sleep("250ms")
        actions.user.paste(current_application)
