import os
import platform
import pprint
import re
from itertools import islice
from typing import Union

from talon import Module, actions, app, clip, registry, scope, speech_system, ui
from talon.grammar import Phrase

pp = pprint.PrettyPrinter()


mod = Module()
pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")


def create_name(text, max_len=20):
    return "_".join(list(islice(pattern.findall(text), max_len))).lower()


@mod.action_class
class Actions:
    def talon_add_context_clipboard_python():
        """Adds os-specific context info to the clipboard for the focused app for .py files. Assumes you've a Module named mod declared."""
        friendly_name = actions.app.name()
        # print(actions.app.executable())
        executable = actions.app.executable().split(os.path.sep)[-1]
        app_name = create_name(friendly_name.replace(".exe", ""))
        if app.platform == "mac":
            result = 'mod.apps.{} = """\nos: {}\nand app.bundle: {}\n"""'.format(
                app_name, app.platform, actions.app.bundle()
            )
        elif app.platform == "windows":
            result = 'mod.apps.{} = """\nos: windows\nand app.name: {}\nos: windows\nand app.exe: {}\n"""'.format(
                app_name, friendly_name, executable
            )
        else:
            result = 'mod.apps.{} = """\nos: {}\nand app.name: {}\n"""'.format(
                app_name, app.platform, friendly_name
            )

        clip.set_text(result)

    def talon_add_context_clipboard():
        """Adds os-specific context info to the clipboard for the focused app for .talon files"""
        friendly_name = actions.app.name()
        # print(actions.app.executable())
        executable = actions.app.executable().split(os.path.sep)[-1]
        if app.platform == "mac":
            result = f"os: {app.platform}\nand app.bundle: {actions.app.bundle()}\n"
        elif app.platform == "windows":
            result = (
                "os: windows\nand app.name: {}\nos: windows\nand app.exe: {}\n".format(
                    friendly_name, executable
                )
            )
        else:
            result = f"os: {app.platform}\nand app.name: {friendly_name}\n"

        clip.set_text(result)

    def talon_sim_phrase(phrase: Union[str, Phrase]):
        """Sims the phrase in the active app and dumps to the log"""
        print("**** Simulated Phrse **** ")
        print(speech_system._sim(str(phrase)))
        print("*************************")

    def talon_action_find(action: str):
        """Runs action.find for the provided action and dumps to the log"""
        print(f"**** action.find{action} **** ")
        print(actions.find(action))
        print("***********************")

    def talon_debug_list(name: str):
        """Dumps the contents of list to the console"""
        print(f"**** Dumping list {name} **** ")

        print(str(registry.lists[name]))
        print("***********************")

    def talon_debug_tags():
        """Dumps the active tags to the console"""
        print("**** Dumping active tags *** ")
        print(str(registry.tags))
        print("***********************")

    def talon_debug_modes():
        """Dumps active modes to the console"""
        print("**** Active modes ****")
        print(scope.get("mode"))
        print("***********************")

    def talon_debug_scope(name: str):
        """Dumps the active scope information to the console"""
        print(f"**** Dumping {name} scope ****")
        print(scope.get(name))
        print("***********************")

    def talon_copy_list(name: str):
        """Dumps the contents of list to the console"""
        print(f"**** Copied list {name} **** ")
        clip.set_text(pp.pformat(registry.lists[name]))
        print("***********************")

    def talon_debug_setting(name: str):
        """Dumps the current setting to the console"""
        print(f"**** Dumping setting {name} **** ")
        print(registry.settings[name])
        print("***********************")

    def talon_debug_all_settings():
        """Dumps all settings to the console"""
        print("**** Dumping settings **** ")
        print(str(registry.settings))
        print("***********************")

    def talon_get_active_context() -> str:
        """Returns active context info"""
        name = actions.app.name()
        executable = actions.app.executable()
        bundle = actions.app.bundle()
        title = actions.win.title()
        hostname = scope.get("hostname")
        result = f"Name: {name}\nExecutable: {executable}\nBundle: {bundle}\nTitle: {title}\nhostname: {hostname}"
        return result

    def talon_get_hostname() -> str:
        """Returns the hostname"""
        hostname = scope.get("hostname")
        return hostname

    def talon_get_active_application_info() -> str:
        """Returns all active app info to the cliboard"""
        result = str(ui.active_app())
        result += "\nActive window: " + str(ui.active_window())
        result += "\nWindows: " + str(ui.active_app().windows())
        result += "\nName: " + actions.app.name()
        result += "\nExecutable: " + actions.app.executable()
        result += "\nBundle: " + actions.app.bundle()
        result += "\nTitle: " + actions.win.title()
        return result

    def talon_version_info() -> str:
        """Returns talon & operation system verison information"""
        result = (
            f"Version: {app.version}, Branch: {app.branch}, OS: {platform.platform()}"
        )
        return result

    def talon_pretty_print(obj: object):
        """Uses pretty print to dump an object"""
        pp.pprint(obj)

    def talon_pretty_format(obj: object):
        """Pretty formats an object"""
        return pp.pformat(obj)

    def talon_debug_app_windows(app: str):
        """Pretty prints the application windows"""
        apps = ui.apps(name=app, background=False)
        for app in apps:
            pp.pprint(app.windows())
