from talon import app, Module, Context, actions, ui
import re
import time
import os
import platform

app_cache = {}
overrides = {}

mod = Module()
mod.list('running', desc='all running applications')
mod.list('launch', desc='all launchable applications')

ctx = Context()
@ctx.capture('running_applications', rule='{self.running}')
def running_applications(m):
    print(str(m))
    return m._words[-1]
    
@ctx.capture('launch_applications', rule='{self.launch}')
def launch_applications(m):
    return m
    
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
    def focus(name: str):
        """Focus a new application by  name"""
        full = ctx.lists['self.running'].get(name)
        if not full:
            return
        for app in ui.apps():
            if app.name == full and not app.background:
                app.focus()
                break

    def launch(path: str):
        """Launch a new application by path"""
        ui.launch(path=path)

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