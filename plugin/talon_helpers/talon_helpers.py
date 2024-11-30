import os
import platform
import pprint
import re
from itertools import islice
from typing import Union

from talon import Module, actions, app, clip, registry, scope, speech_system, ui
from talon.grammar import Phrase
from talon.scripting.types import ListTypeFull

pp = pprint.PrettyPrinter()


mod = Module()
pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")


def create_name(text, max_len=20):
    return "_".join(list(islice(pattern.findall(text), max_len))).lower()

def talon_convert_list_helper(list_name, output_path):
    import re
    if list_name in registry.lists:
        list_values =  registry.lists[list_name][0]
        result = f"list: {list_name}\n-\n"

        if len(list_values) > 0:
            for spoken_form, mapped_value in list_values.items():
                if re.search(r'^\s+|\s+$',mapped_value):
                    result += f'{spoken_form}: """{mapped_value}"""\n'
                else:
                    result += f"{spoken_form}: {mapped_value}\n"

            f = open(output_path, "w")
            f.write(result)
            f.close()    
            return True
        return False
    else:
        return False

@mod.action_class
class Actions:
    def talon_add_context_clipboard_python():
        """Adds os-specific context info to the clipboard for the focused app for .py files. Assumes you've a Module named mod declared."""
        friendly_name = actions.app.name()
        # print(actions.app.executable())
        executable = os.path.basename(actions.app.executable())
        app_name = create_name(friendly_name.removesuffix(".exe"))
        if app.platform == "mac":
            result = 'mod.apps.{} = """\nos: mac\nand app.bundle: {}\n"""'.format(
                app_name, actions.app.bundle()
            )
        elif app.platform == "windows":
            result = 'mod.apps.{} = r"""\nos: windows\nand app.name: {}\nos: windows\nand app.exe: /^{}$/i\n"""'.format(
                app_name, friendly_name, re.escape(executable.lower())
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
        executable = os.path.basename(actions.app.executable())
        if app.platform == "mac":
            result = f"os: mac\nand app.bundle: {actions.app.bundle()}\n"
        elif app.platform == "windows":
            result = "os: windows\nand app.name: {}\nos: windows\nand app.exe: /^{}$/i\n".format(
                friendly_name, re.escape(executable.lower())
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

    def talon_restart():
        """restart talon"""
        talon_app = ui.apps(pid=os.getpid())[0]
        if app.platform == "mac":
            from shlex import quote
            from subprocess import Popen

            talon_app_path = quote(talon_app.path)
            Popen(
                [
                    "/bin/sh",
                    "-c",
                    f"/usr/bin/open -W {talon_app_path} ; /usr/bin/open {talon_app_path}",
                ],
                start_new_session=True,
            )
            talon_app.quit()
        elif app.platform == "windows":
            os.startfile(talon_app.exe)
            talon_app.quit()

    def talon_convert_lists():
        """Converts all active lists with at least one entry to a talon list"""
        if app.platform == "windows":
            base_path = os.path.expandvars(f"%AppData%\\Talon\\converted_lists")
        else:
            base_path = os.path.expanduser("~/.talon/converted_lists")

        if not os.path.exists(base_path):
            os.mkdir(base_path)
        
        count = 0
        for list_name, value in registry.lists.items():
            output_path = os.path.join(base_path, f"{list_name}.talon-list".replace("user.", ""))
            if talon_convert_list_helper(list_name, output_path):
                count += 1

        actions.app.notify(f"successfully converted {count} files to talon list")

    def talon_convert_list(list_name: str):
        """Converts active lists with at least one entry to a talon list"""
        if app.platform == "windows":
            base_path = os.path.expandvars(f"%AppData%\\Talon\\converted_lists")
        else:
            base_path = os.path.expanduser("~/.talon/converted_lists")

        output_path = os.path.join(base_path, f"{list_name}.talon-list".replace("user.", ""))
        
        if talon_convert_list_helper(list_name, output_path):
            actions.app.notify(f"successfully converted {list_name} to talon list")
        else:
            actions.app.notify(f"failed to convert  {list_name} to talon list")
        
    def talon_kill():
        """kill talon"""
        talon_app = ui.apps(pid=os.getpid())[0]
        if app.platform == "mac":
            talon_app.quit()
        elif app.platform == "windows":
            talon_app.quit()

    def talon_dump_running_applications(): 
        """Dump active applications"""
        for app in ui.apps():
            print(app.name.lower())
    
    def talon_edit_log():
        """Edit talon log"""
        actions.user.exec("code C:\\Users\\knaus\\AppData\\Roaming\\talon\\talon.log")
		
    def talon_get_active_registry_list(name: str) -> ListTypeFull:
        """Returns the active list from the Talon registry"""
        return registry.lists[name][-1]
		
    def talon_get_windows_app_id():
        """do it"""
        import win32com.client

        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.NameSpace('shell:::{4234d49b-0245-4df3-b780-3893943456e1}')
        items = folder.Items()
        
        for item in items:
            if ui.active_app().name.lower() in item.Name.lower():
                clip.set_text(item.path)
    
        