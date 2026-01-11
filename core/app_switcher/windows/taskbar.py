from talon.windows.ax import Element
from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
from dataclasses import dataclass, asdict
from talon.ui import Rect
import math
import platform

mod = Module()

def first_matching_child(element, **kw):
    if len(kw) > 1:
        raise Exception("Only one matching attribute supported")
    attr, values = list(kw.items())[0]
    return next(e for e in element.children if getattr(e, attr) in values)

@dataclass
class TaskBarPositionData:
    rect: Rect
    icon_width: float
    icon_height: float 

    def __init__(self):
        pass

    def set(self, rect, icon_width, icon_height):
        self.rect = rect
        self.icon_width = icon_width
        self.icon_height = icon_height

    def __str__(self):
        return f"rect = {self.rect}, icon_width = {self.icon_width}, icon_height = {self.icon_height}"

is_windows_eleven = "Windows-11" in platform.platform()
print(platform.platform())
taskbar_data = TaskBarPositionData()
canvas_taskbar = None
icons_to_exclude = ["Start"]#, "Search", "Task View"]

mod = Module()

@mod.action_class
class Actions:
    def switcher_click(mouse_button: int, index: int):
        """"""        
        x, y = ctrl.mouse_pos()
        print(index)
        actions.mouse_move(taskbar_data.rect.x + (taskbar_data.icon_width * (index + .5)), 
                           taskbar_data.rect.y + taskbar_data.rect.height / 2)
        actions.mouse_click(mouse_button)
        actions.sleep("150ms")
        actions.mouse_move(x, y)

def draw_options(canvas):
    print("draw_options")
    paint = canvas.paint
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    taskbar_rect = taskbar_data.rect
    count = math.floor(taskbar_rect.width / taskbar_data.icon_width)
    paint.textsize = 20

    x = taskbar_rect.x
    y = taskbar_rect.y + .8 * taskbar_data.icon_height
    for index in range(1, count + 1):
        paint.style = paint.Style.FILL
        paint.color = "000000"
        canvas.draw_rect(Rect(math.floor(x + taskbar_data.icon_width / 2), 
                              y, 
                              taskbar_data.icon_width / 3, 
                              taskbar_data.icon_height * .8 ))
        
        x_text_position = x + taskbar_data.icon_width / 2 + taskbar_data.icon_width * .18
        y_text_position = y + taskbar_data.icon_height * .18
        paint.color = "ffffff"
        canvas.draw_text(f"{index}", x_text_position, y_text_position)
        x = x + taskbar_data.icon_width

def get_windows_ten_taskbar() -> bool:
    """Populated the TaskBarData class for windows 10"""
    icon_width: float = 0.0
    icon_height: float = 0.0
    icon_dimensions_set: bool = False
    
    ms_tasklist = None
    taskbar = None

    apps = ui.apps(name="Windows Explorer")
    for application in apps:
        for window in application.windows():
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

    # include the task view if enabled
    for e in taskbar.element.children:
        #print(e)
        if "Task View" in e.name and "Task View" not in icons_to_exclude:
            icon_width = e.rect.width
            icon_height = e.rect.height
            icon_dimensions_set = True
            
    if not taskbar:
        if not ms_tasklist:
            print("failed to find MSTaskListWClass")

        return False
    
    for e in ms_tasklist.children:
        if not icon_dimensions_set:
            print(f"found first icon {e.name} {e.rect}")
            icon_width = e.rect.width
            icon_height = e.rect.height
            icon_dimensions_set = True
            
    if taskbar and icon_dimensions_set:
        taskbar_rect = ms_tasklist.rect.copy()
        taskbar_data.set(taskbar_rect, icon_width, icon_height)
        print(f"all prequistes found for windows 10 taskbar numbers: {taskbar_data}")

        return True
    
    return False

def get_windows_eleven_taskbar() -> bool:
    """Populates the TaskBarData class for windows 11"""
    icon_width: float = 0.0
    icon_height: float = 0.0
    icon_dimensions_set: bool = False
    first_icon_rect: Rect
    hidden_icon_found: bool = False

    apps = ui.apps(name="Windows Explorer")
    for app in apps:
        for window in app.windows():
            if window.cls == "Shell_TrayWnd":
                print("found taskbar")
                taskbar = window.element
                break

    if taskbar:
        taskbar_rect = taskbar.rect.copy()
        print(f"taskbar rect {taskbar.rect}")
        for element in taskbar.children:
            for child in element.children:
                for child2 in child.children:
                    if child2.name not in icons_to_exclude:
                        if not icon_dimensions_set:                            
                            icon_width = child2.rect.width
                            icon_height = child2.rect.height
                            first_icon_rect = child2.rect
                            icon_dimensions_set = True
                            print(f"first taskbar icon found {child2.name}: {child2.rect}")


                if child.name == "Show Hidden Icons":
                    hidden_icon_found = True
                    hidden_icon_rect = child.rect
                    print(f"found hidden icons! {child.rect}")
        
        # The taskbar rect in windows 11 includes the system tray
        # we want to provide a rect that removes this
        if icon_dimensions_set and hidden_icon_found:
            task_list_rect = Rect(first_icon_rect.x, 
                                  taskbar_rect.y, 
                                  hidden_icon_rect.x - first_icon_rect.x, 
                                  taskbar_rect.height)
            
            taskbar_data.set(task_list_rect, icon_width, icon_height)
            print(f"all prequistes found for windows 11 taskbar numbers: {taskbar_data}")

            return True
    
    return False

def update_canvas():
    global canvas_taskbar    
    main_screen = ui.main_screen()

    print(f"main screen: {main_screen}")
    print(f"screens: {ui.screens()}")
    
    if canvas_taskbar:
        canvas_taskbar.close()
    
    if not is_windows_eleven:
        success = get_windows_ten_taskbar()
    else:
        success = get_windows_eleven_taskbar()

    if success:
        rect = taskbar_data.rect
        canvas_taskbar = canvas.Canvas.from_rect(rect)

        print(f"taskbar data successfully populated. Creating canvas for taskbar numbers {rect}")
        canvas_taskbar.register("draw", draw_options)
        canvas_taskbar.freeze()
    else:
        print("taskbar data population failed. Skipping canvas creation")


def on_screen_change(_):
    print("on_screen_change")
    update_canvas()

if app.platform == "windows":
    def on_ready():
        update_canvas()
        ui.register("screen_change", on_screen_change)    

    app.register("ready", on_ready)


