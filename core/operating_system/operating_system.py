from talon import Context, Module, actions, ui, app
import os
import platform

mod = Module()
mod.list("system_setting", desc="List of system level configuration setting to launch")
mod.list(
    "system_directories",
    desc="List of system directories. By default, these are generated on start per-OS",
)
mod.list(
    "user_directories",
    desc="List of user-defined directories. Empty by default, used to expand the available paths",
)

@mod.scope
def scope():
    operating_system = f"{platform.system()} {platform.release()}".lower()
    print(operating_system)
    return {
        "operating_system": operating_system, 
        }

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

    def system_setting(system_setting: str):
        """Launches a system setting app"""

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

    def system_show_portal(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""

    def system_show_coder(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""

    def system_show_messenger(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""

    def system_show_slacker(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""

    def system_show_email(phrase: str = None):
        """Opens the defaul6t browser for the up operating system and performs the phrase command"""

    def system_show_gitter(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""


    def system_taskmanager_find_focused_application(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
