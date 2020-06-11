from talon import app, Module, Context, actions, ui,imgui
from talon.voice import Capture
import re
import time
import os

app_cache = {}
overrides = {
    'grip': 'DataGrip',
    'term': 'iTerm2',
    'lock': 'Slack'
}

# If you don't like an app name you can remap it here
# key: name OS thinks app is
# value: what you want to say
friendly_names = {
    'pycharm64': 'pycharm',
    'idea64': 'idea',
    'webstorm64': 'webstorm',
    'outlook.exe': 'outlook'
}

mod = Module()
mod.list('running', desc='all running applications')
mod.list('launch', desc='all launchable applications')

@mod.capture
def running_applications(m) -> str:
    "Returns a single application name"

@mod.capture
def launch_applications(m) -> Capture:
    "Returns a single application name"

ctx = Context()
@ctx.capture(rule='{self.running}')
def running_applications(m):
    return m.running

@ctx.capture(rule='{self.launch}')
def launch_applications(m):
    return m.launch

def split_camel(word):
    return re.findall(r'[0-9A-Z]*[a-z]+(?=[A-Z]|$)', word)

def get_words(name):
    words = re.findall(r'[0-9A-Za-z]+', name)
    out = []
    for word in words:
        out += split_camel(word)
    return out

@mod.action_class
class Actions:
    def switcher_focus(name: str):
        """Focus a new application by  name"""
        for app in ui.apps():
            #print("app.name:" + app.name)
            #print("app.bundler: " + app.bundle)
            if app.name == name and not app.background:
                app.focus()
                break

    def switcher_launch(path: str):
        """Launch a new application by path"""
        ui.launch(path=path)

    def switcher_list_running():
        """Lists all running applications"""
        gui.show()

    def switcher_hide_running():
        """Hides list of running applications"""
        gui.hide()

@imgui.open(software=False)
def gui(gui: imgui.GUI):
    gui.text("Names of running applications")
    gui.line()
    for line in  ctx.lists['self.running']:
        gui.text(line)

def update_lists():
    running = {}
    launch = {}

    for cur_app in ui.apps(background=False):
        name = cur_app.name
        if name.endswith('.exe'):
            name = name.rsplit('.', 1)[0]
        words = get_words(name)
        for word in words:
            if word and not word in running:
                running[word.lower()] = cur_app.name
        running[name.lower()] = cur_app.name
    for override in overrides:
        running[override] = overrides[override]

    running = {(friendly_names.get(friendly_name) or friendly_name): app_name
               for (friendly_name, app_name) in running.items()}

    if app.platform == "mac":
        for base in '/Applications', '/Applications/Utilities':
            for name in os.listdir(base):
                path = os.path.join(base, name)
                name = name.rsplit('.', 1)[0].lower()
                launch[name] = path
                words = name.split(' ')
                for word in words:
                    if word and word not in launch:
                        if len(name) > 6 and len(word) < 3:
                            continue
                        launch[word] = path

    lists = {
        'self.running': running,
        'self.launch': launch,
    }

    #batch update lists
    ctx.lists.update(lists)

def ui_event(event, arg):
    if event in ('app_activate', 'app_launch', 'app_close', 'win_open', 'win_close'):
        update_lists()

ui.register('', ui_event)
update_lists()