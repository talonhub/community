from talon import app, Module, Context, actions, ui,imgui
from talon.voice import Capture
import re
import time
import os
import platform

app_cache = {}
overrides = {'code': 'VSCode', 'grip': 'DataGrip', 'term': 'iTerm2'}

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

@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Names of running applications")
    gui.line()
    for line in  ctx.lists['self.running']:
        gui.text(line)

def update_lists():
    new = {}
    for cur_app in ui.apps(background=False):
        name = cur_app.name
        if name.endswith('.exe'):
            name = name.rsplit('.', 1)[0]
        words = get_words(name)
        for word in words:
            if word and not word in new:
                new[word] = cur_app.name
        new[name] = cur_app.name
    for override in overrides:
        new[override] = overrides[override]
        
    ctx.lists['self.running'] = new
    
    #print(str(new))
    new = {}
    
    if app.platform == "mac":
        for base in '/Applications', '/Applications/Utilities':
            for name in os.listdir(base):
                path = os.path.join(base, name)
                name = name.rsplit('.', 1)[0].lower()
                new[name] = path
                words = name.split(' ')
                for word in words:
                    if word and word not in new:
                        if len(name) > 6 and len(word) < 3:
                            continue
                        new[word] = path
    
        ctx.lists['self.launch'] = new

def ui_event(event, arg):
    if event in ('app_activate', 'app_launch', 'app_close', 'win_open', 'win_close'):
        update_lists()

ui.register('', ui_event)
update_lists()