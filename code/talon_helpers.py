from talon import Context, actions, ui, Module, app, clip
import os
import re
from itertools import islice


mod = Module()
pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")

# todo: should this be an action that lives elsewhere??
def create_name(text, max_len=20):
    return "_".join(list(islice(pattern.findall(text), max_len))).lower()


@mod.action_class
class Actions:
    def talon_add_context_clipboard():
        """Adds os-specific context info to the clipboard"""
        friendly_name = actions.app.name()

        executable = actions.app.executable().split(os.path.sep)[-1]
        if app.platform == "mac":
            result = 'mod.apps.{} = """\nos: {}\nand app.bundle: {}\n"""'.format(
                create_name(friendly_name), app.platform, actions.app.bundle()
            )
        elif app.platform != "windows" or friendly_name == executable:
            result = 'mod.apps.{} = """\nos: {}\nand app.name: {}\n"""'.format(
                create_name(friendly_name), app.platform, friendly_name
            )

        # on windows, it's best to include both the friendly name and executable name in case the muicache breaks....
        else:
            result = 'mod.apps.{} = """\nos: {}\nand app.name: {}\nos: {}\nand app.name: {}\n"""'.format(
                create_name(friendly_name),
                app.platform,
                friendly_name,
                app.platform,
                executable,
            )

        clip.set(result)

