from talon.windows.ax import Element
from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
from dataclasses import dataclass, asdict
from talon.ui import Rect
import math
import platform

mod = Module()

mod.setting(
    "talon_icon_index",
    type=int,
    default=0,
    desc="index of the talent icon in the taskbar",
)

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
        if index == settings.get("user.talon_icon_index"):
            return
        
        x, y = ctrl.mouse_pos()
        actions.mouse_move(position_cache[index].x, position_cache[index].y)
        actions.mouse_click(mouse_button)


        actions.sleep("150ms")
        actions.mouse_move(x, y)


def draw_options(canvas):
    if not width:
        return
    paint = canvas.paint
    #for b in cache:
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    count = math.floor(tasklist_width / width)
    paint.textsize = 20

    x = x_start
    y = y_start + .8 * height
    for index in range(1, count + 1):
        paint.style = paint.Style.FILL
        paint.color = "000000"
        canvas.draw_rect(Rect(math.floor(x + width / 2), y, width / 3, height * .8 ))

        paint.color = "ffffff"

        position = Position(x + width / 2 + width * .18 , y+ height * .18)
        canvas.draw_text(f"{index}", position.x, position.y )

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
def get_windows_ten_taskbar(forced: bool = False):
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
                # tray = first_matching_child(taskbar.element, class_name=["TrayNotifyWnd"])
                # pager = first_matching_child(tray, class_name=["SysPager"])
                # toolbar = first_matching_child(pager, class_name=["ToolbarWindow32"])
                # for child in toolbar.children:
                #     print(f"{child.name} {child.rect.width} {child.rect.height}")
                # break
                
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
            print(f"{width}x{height}")
            break

def get_windows_eleven_taskbar(forced: bool = False):
    global cache, taskbar, ms_tasklist, tasklist_width

    if not taskbar:
        apps = ui.apps(name="Windows Explorer")
        for app in apps:
            for window in app.windows():
                if window.cls == "Shell_TrayWnd":
                    taskbar = window.element
                    break

        if taskbar:
            print(f"taskbar rect {taskbar.rect}")
            # ms_tasklist = first_matching_child(taskbar.element, class_name=["Taskbar.TaskbarFrameAutomationPeer"])            
            show_hidden_x = None
            for element in taskbar.children:
                for child in element.children:
                    for child2 in child.children:
                        #print(child2)
                        if child2.name != "Start" and child2.name != "Search" and child2.name != "Task View":
                            global width, height, x_start, y_start, tasklist_width

                            tasklist_width = child.rect.width
                            
                            if not x_start:
                                width = child2.rect.width
                                height = child2.rect.height
                                x_start = child2.rect.x
                                y_start = child2.rect.y
                                print(f"first taskbar icon found {child2.name}: {child2.rect}")

                    if child.name == "Show Hidden Icons":
                        show_hidden_x = child.rect.x
                        print(f"found hidden icons! {child.rect}")
            
            tasklist_width = show_hidden_x - x_start
mcanvas = None

def update_canvas():
    global mcanvas
    global cache, taskbar, ms_tasklist, tasklist_width
    global width, height, x_start, y_start
    
    main_screen = ui.main_screen()
    print(f"main screen: {main_screen}")
    print(f"screens: {ui.screens()}")
    
    if mcanvas:
        taskbar = None
        ms_tasklist = None
        tasklist_width = None
        width = None
        height = None
        x_start = None
        y_start = None
        mcanvas.close()
    
    mcanvas = canvas.Canvas.from_screen(main_screen)
    platform_str = platform.platform()

    if "Windows-11" not in platform_str:
        get_windows_ten_taskbar(True)
    else:
        get_windows_eleven_taskbar(True)

    mcanvas.register("draw", draw_options)
    mcanvas.freeze()

def on_screen_change(_):
    print("on_screen_change")
    update_canvas()

if app.platform == "windows":

    def on_ready():
        update_canvas()
        ui.register("screen_change", on_screen_change)    

    app.register("ready", on_ready)


