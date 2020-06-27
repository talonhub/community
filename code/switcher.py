from talon import app, Module, Context, actions, ui,imgui
from talon.voice import Capture
import re
import time
import os
# Construct at startup a list of overides for application names (similar to how homophone list is managed)
# ie for a given talon recognition word set  `one note`, recognized this in these switcher functions as `ONENOTE`
# the list is a comma seperated `<Recognized Words>, <Overide>`
#TODO: Consider put list csv's (homophones.csv, app_name_overrides.csv) files together in a seperate directory,`knausj_talon/lists`
cwd = os.path.dirname(os.path.realpath(__file__))
overrides_file = os.path.join(cwd, "app_name_overrides.csv")
overrides ={}
with open(overrides_file, "r") as f:
    for line in f:
        line = line.rstrip()
        line = line.split(",")
        overrides[line[0].lower()] = line[1].strip()

print(f'knausj_talon.switcher------------ app name overrides:{overrides}')

app_cache = {}


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
            # print(f"--------- app.name:{app.name}  app.bundler:{app.bundle}")
            if name in app.name and not app.background:
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
        # print(f'------------------ event:{event}  arg:{arg}')
        update_lists()

ui.register('', ui_event)
update_lists()