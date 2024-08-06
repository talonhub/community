import pathlib
import json
from talon import Context, Module, actions

mod = Module()
ctx = Context()

vscode_plugin_cache = None

ctx.matches = r"""
    app: vscode
    tag: user.plugins
"""


def vscode_update_plugins_list():
    """Queries the list of vscode plugins"""
    extensions = pathlib.Path.home() / ".vscode/extensions/extensions.json"
    if not extensions.exists():
        return []
    with extensions.open() as f:
        return [x["identifier"]["id"] for x in json.loads(f.read())]


def vscode_plugins_list():
    """Returns a cached or new list of installed vscode plugins"""
    global vscode_plugin_cache
    if vscode_plugin_cache is None:
        vscode_plugin_cache = vscode_update_plugins_list()
    if vscode_plugin_cache is None:
        return []
    return set(vscode_plugin_cache)


@ctx.action_class
class PluginActions:
    def plugins_list():
        return vscode_plugins_list()

    def plugins_list_refresh():
        global vscode_plugin_cache
        vscode_plugin_cache = vscode_update_plugins_list()
        actions.user.plugins_scope_update()

    def plugins_list_print():
        global vscode_plugin_cache
        if vscode_plugin_cache is None:
            actions.user.plugins_list_refresh()
        print(vscode_plugin_cache)
