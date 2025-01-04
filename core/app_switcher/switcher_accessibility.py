from talon import Context, Module, actions, app, registry, canvas, actions, ui, app, skia
from talon.ui import Rect
from talon import ui, app
from talon.windows.ax import Element
from .app_switcher import APPLICATIONS_OVERRIDES
from dataclasses import dataclass

mod = Module()
mod.list("running_applications", desc="all running applications")
ctx = Context()
cache = []

@dataclass
class TaskBarItem:
    title: str
    type: str
    element: Element

@mod.action_class
class Actions:
    def switcher_accessibility_focus(title: str):
        """experimental"""
        rebuild_taskbar_app_list()
        for item in cache:
            if item.title == title:
                item.element.invoke_pattern.invoke()
                break

    # def switcher_accessibility_show():
    #     """what"""
    #     create_canvases()

def first_matching_child(element, **kw):
    if len(kw) > 1:
        raise Exception("Only one matching attribute supported")
    attr, values = list(kw.items())[0]
    return next(e for e in element.children if getattr(e, attr) in values)

def rebuild_taskbar_app_list(forced: bool = False):
    global cache

    explorer = ui.apps(name="Windows Explorer")[0]
    taskbar = next(
        window for window in explorer.windows() if window.cls == "Shell_TrayWnd"
    )
    running_applications = first_matching_child(taskbar.element, class_name=["MSTaskListWClass"])
    #update_canvas = forced or len(running_applications.children) != len(cache)
    cache = []
    result = {}

    for e in running_applications.children:

        title = e.name
        splits = title.split(" - ")
        name = splits[0] 
        cache.append(TaskBarItem(title, str(e.control_type), e))
        override = None
        if name in APPLICATIONS_OVERRIDES:
            override = APPLICATIONS_OVERRIDES[name]
            
        if override and override.spoken_forms:
            for form in override.spoken_forms:
                result[form] = title
        else:
            result[name] = title

    ctx.lists["user.running_applications"] = result

def ui_event(event, arg):
    if event in ("app_launch", "app_close", "app_activate", "app_deactivate"):
        rebuild_taskbar_app_list()

def on_ready():
    rebuild_taskbar_app_list()
    ui.register("", ui_event)

app.register("ready", on_ready)