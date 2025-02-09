from talon.windows.ax import Element
from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl
from dataclasses import dataclass, asdict
from talon.ui import Rect
import math
import platform

def first_matching_child(element, **kw):
    if len(kw) > 1:
        raise Exception("Only one matching attribute supported")
    attr, values = list(kw.items())[0]
    return next(e for e in element.children if getattr(e, attr) in values)

@dataclass
class Position:
    x: int
    y: int

position_cache = []

mod = Module()

@mod.action_class
class Actions:
    def switcher_click(mouse_button: int, index: int):
        """"""
        x, y = ctrl.mouse_pos()
        actions.mouse_move(position_cache[index].x, position_cache[index].y)
        actions.mouse_click(mouse_button)

        # if mouse_button == 0:
        #     actions.sleep("150ms")
        #     actions.mouse_move(x, y)


mcanvas = canvas.Canvas.from_screen(ui.main_screen())
def draw_options(canvas):
    if not width:
        return
    paint = canvas.paint
    #for b in cache:
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    count = math.floor(tasklist_width / width)
    paint.textsize = 20

    x = x_start
    y = y_start + math.floor(height / 2)
    for index in range(1, count + 1):
        paint.style = paint.Style.FILL
        paint.color = "000000"
        canvas.draw_rect(Rect(math.floor(x + width / 2), y, width / 3, height / 3))

        paint.color = "ffffff"

        position = Position(x + width / 2 + 17, y + 20)
        canvas.draw_text(f"{index}", position.x, position.y)

        position_cache.append(position)
        x = x + width


cache = None 
ms_tasklist = None 
taskbar = None
width = None 
height = None 
x_start = None 
y_start = None

tasklist_width = None
def rebuild_taskbar_app_list(forced: bool = False):
    global cache, taskbar, ms_tasklist, tasklist_width


    if not taskbar:
        apps = ui.apps(name="Windows Explorer")
        for app in apps:
            for window in app.windows():
                if window.cls == "Shell_TrayWnd":
                    taskbar = window
                    break
            if taskbar:
                ms_tasklist = first_matching_child(taskbar.element, class_name=["MSTaskListWClass"])
                break
                
    if not taskbar:
        actions.app.notify("taskbar window not found")
        return
    
    #update_canvas = forced or len(running_applications.children) != len(cache)
    cache = []

    tasklist_width = ms_tasklist.rect.width
    #running = {}
    global width, height, x_start, y_start
    for e in ms_tasklist.children:
        title = e.name
        splits = title.split(" - ")
        name = splits[0] 

        if not x_start:
            width = e.rect.width
            height = e.rect.height
            x_start = e.rect.x
            y_start = e.rect.y
            break

if app.platform == "windows":
    # uncomment the following for quick testing
    def on_ready():
        if "Windows-11" not in platform.platform():
            rebuild_taskbar_app_list()
        else:
            global tasklist_width, height, width, x_start, y_start
            tasklist_width = 2400
            width = 88
            height = 96
            x_start = 646
            y_start = 2090
        mcanvas.register("draw", draw_options)

    app.register("ready", on_ready)


