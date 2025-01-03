from talon import ui, app
from talon.windows.ax import Element
from .app_switcher import APPLICATIONS_OVERRIDES
from dataclasses import dataclass

cache = []

@dataclass
class TaskBarItem:
    name: str
    type: str
    element: Element

def first_matching_child(element, **kw):
    if len(kw) > 1:
        raise Exception("Only one matching attribute supported")
    attr, values = list(kw.items())[0]
    return next(e for e in element.children if getattr(e, attr) in values)

def rebuild_taskbar_app_list():
    global cache

    explorer = ui.apps(name="Windows Explorer")[0]
    taskbar = next(
        window for window in explorer.windows() if window.cls == "Shell_TrayWnd"
    )

    running_applications = first_matching_child(taskbar.element, class_name=["MSTaskListWClass"])

    if len(running_applications.children) == len(cache):
        return
    
    cache = []

    for e in running_applications.children:
        title = e.name
        splits = title.split(" - ")
        name = splits[0] 
        is_app_running = len(splits) == 2
        
        if name in APPLICATIONS_OVERRIDES:
            override = APPLICATIONS_OVERRIDES[name]
            
            e.el.invoke()
            break
    
        cache.append(TaskBarItem(name, str(e.control_type), e))

    #pager = first_matching_child(tray, class_name=["SysPager"])
    #toolbar = first_matching_child(pager, class_name=["ToolbarWindow32"])

def ui_event(event, arg):
    if event in ("app_launch", "app_close", "app_activate", "app_deactivate"):
        rebuild_taskbar_app_list()

def on_ready():
    rebuild_taskbar_app_list()
    ui.register("", ui_event)

app.register("ready", on_ready)