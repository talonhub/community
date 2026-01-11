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

import winreg
from typing import Literal, Optional, TypedDict


TaskbarCombineMode = Literal["always", "when_full", "never", "unknown"]

class TaskbarCombineStatus(TypedDict):
    policy_forces_never_combine: bool
    primary: TaskbarCombineMode
    other_taskbars: Optional[TaskbarCombineMode]  # None if not present


def _read_dword(root, path: str, name: str) -> Optional[int]:
    try:
        with winreg.OpenKey(root, path) as key:
            val, _typ = winreg.QueryValueEx(key, name)
            return int(val)
    except FileNotFoundError:
        return None
    except OSError:
        return None


def _map_glom_level(v: Optional[int]) -> TaskbarCombineMode:
    # Based on observed Win11 mapping for TaskbarGlomLevel/MMTaskbarGlomLevel.
    if v == 0:
        return "always"
    if v == 1:
        return "when_full"
    if v == 2:
        return "never"
    if v is None:
        return "unknown"
    return "unknown"


def get_taskbar_combine_status() -> TaskbarCombineStatus:
    adv_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
    pol_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"

    primary_raw = _read_dword(winreg.HKEY_CURRENT_USER, adv_path, "TaskbarGlomLevel")
    other_raw = _read_dword(winreg.HKEY_CURRENT_USER, adv_path, "MMTaskbarGlomLevel")

    # Policy override: if NoTaskGrouping exists and is non-zero, grouping is disabled (i.e., "never combine").
    policy_raw = _read_dword(winreg.HKEY_LOCAL_MACHINE, pol_path, "NoTaskGrouping")
    policy_forces = bool(policy_raw)  # None/0 -> False; 1 -> True (typical)

    status: TaskbarCombineStatus = {
        "policy_forces_never_combine": policy_forces,
        "primary": "never" if policy_forces else _map_glom_level(primary_raw),
        "other_taskbars": None if other_raw is None else ("never" if policy_forces else _map_glom_level(other_raw)),
    }
    return status

def is_start_left_aligned() -> bool:
    import winreg

    """
    Returns True if Windows 11 taskbar (Start/menu button + icons) is left-aligned.
    Returns False if centered.

    If the value doesn't exist, Windows 11 defaults to centered (False).
    """
    path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
    value_name = "TaskbarAl"

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
            value, value_type = winreg.QueryValueEx(key, value_name)
            # Expecting a DWORD; treat 0 as left, anything else as centered.
            return int(value) == 0
        
    except FileNotFoundError:
        # Key or value missing -> default behavior (Win11 default is centered)
        return False
    
@dataclass
class TaskBarPositionData:
    rect_start_button: Rect
    rect_search_button: Rect
    rect_task_view: Rect
    rect_task_list: Rect
    icon_width: float
    icon_height: float 

    def __init__(self):
        pass

    def set(self, rect_start_button, rect_search_button, rect_task_view, rect_task_list, icon_width, icon_height):
        self.rect_start_button = rect_start_button
        self.rect_search_button = rect_search_button
        self.rect_task_view = rect_task_view
        self.rect_task_list = rect_task_list
        self.icon_width = icon_width
        self.icon_height = icon_height

    def __str__(self):
        return f"rect = {self.rect_task_list}, icon_width = {self.icon_width}, icon_height = {self.icon_height}"

is_windows_eleven = "Windows-11" in platform.platform()
print(platform.platform())
taskbar_data = TaskBarPositionData()
canvas_taskbar = None

mod = Module()

@mod.action_class
class Actions:
    def switcher_click(mouse_button: int, index: int):
        """"""        
        x, y = ctrl.mouse_pos()
        print(index)
        actions.mouse_move(taskbar_data.rect_task_list.x + (taskbar_data.icon_width * (index + .5)), 
                           taskbar_data.rect_task_list.y + taskbar_data.rect_task_list.height / 2)
        actions.mouse_click(mouse_button)
        actions.sleep("150ms")
        actions.mouse_move(x, y)

def draw_options(canvas):
    print("draw_options")
    paint = canvas.paint
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    rect_start_menu = taskbar_data.rect_start_button
    rect_search_button = taskbar_data.rect_search_button

    rect_task_bar_list = taskbar_data.rect_task_list
    paint.textsize = 20

    current_index = 1
    x = rect_start_menu.x
    y = rect_task_bar_list.y + .8 * taskbar_data.icon_height
    y_text_position = y + taskbar_data.icon_height * .18

    if rect_start_menu:
        paint.style = paint.Style.FILL
        paint.color = "000000"

        rect_number_background = Rect(math.floor(x + rect_start_menu.width / 2), 
                                y, 
                                rect_start_menu.width / 3, 
                                rect_start_menu.height * .8 )
        
        canvas.draw_rect(rect_number_background)
        x_text_position = rect_number_background.x + rect_number_background.width / 2

        paint.color = "ffffff"
        canvas.draw_text(f"{current_index}", x_text_position, y_text_position)

        current_index = current_index + 1
        x += rect_start_menu.width

    if rect_search_button:
        paint.style = paint.Style.FILL
        paint.color = "000000"

        rect_number_background = Rect(math.floor(x + rect_search_button.width / 2), 
                                    y, 
                                    rect_search_button.width / 3, 
                                    rect_search_button.height * .8)
        
        canvas.draw_rect(rect_number_background)   
        x_text_position = rect_number_background.x + rect_number_background.width / 2

        paint.color = "ffffff"
        canvas.draw_text(f"{current_index}", x_text_position, y_text_position)

        current_index = current_index + 1
        x += rect_search_button.width        

    max_task_list_count = math.floor(rect_task_bar_list.width / taskbar_data.icon_width)

    for index in range(current_index,  current_index + max_task_list_count + 1):
        paint.style = paint.Style.FILL
        paint.color = "000000"

        rect_number_background = Rect(math.floor(x + taskbar_data.icon_width / 2), 
                                    y, 
                                    taskbar_data.icon_width / 3, 
                                    taskbar_data.icon_height * .8 )
        
        canvas.draw_rect(rect_number_background)
        x_text_position = rect_number_background.x + rect_number_background.width / 2
        y_text_position = rect_number_background.y + taskbar_data.icon_height * .18
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
    first_icon_rect: Rect = None
    rect_start_button: Rect = None
    rect_task_view: Rect = None
    rect_search_button: Rect = None
    hidden_icon_found: bool = False
    start_menu_found: bool = False
    search_button_found: bool = False
    task_view_button_found: bool = False

    is_taskbar_left_aligned = is_start_left_aligned()
    task_bar_combine_status = get_taskbar_combine_status()

    start_menu_configured_correctly = (is_taskbar_left_aligned 
        and task_bar_combine_status["primary"] == "always")
    
    if not is_start_left_aligned():
        print("Start menu must be left-aligned")

    if task_bar_combine_status["primary"] != "always":
        print("Start menu icons must be configued to always combine and hide labels")

    if not start_menu_configured_correctly:
        return False
        
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
                match child.name:
                    case "Show Hidden Icons":
                        hidden_icon_found = True
                        rect_hidden_icons = child.rect
                        print(f"found hidden icons! {child.name}")
                    case _:
                        print(f"{child.name}")

                for child2 in child.children:
                    match child2.name:
                        case "Start":
                            rect_start_button = child2.rect
                            start_menu_found = True
                            print(f"found start button! {child2.rect}")

                        case "Search":
                            rect_search_button = child2.rect
                            search_button_found = True
                            print(f"found search button! {child2.rect}")

                        case "Task View":  
                            rect_task_view = child2.rect
                            first_icon_rect = rect_task_view
                            icon_width = child2.rect.width
                            icon_height = child2.rect.height

                            icon_dimensions_set= True
                            task_view_button_found = True
                            print(f"found Task View button! {child2.rect}")

                        case _:
                            if not icon_dimensions_set:                            
                                icon_width = child2.rect.width
                                icon_height = child2.rect.height
                                first_icon_rect = child2.rect
                                icon_dimensions_set = True
                                print(f"first taskbar icon found {child2.name}: {child2.rect}")

        
        # The taskbar rect in windows 11 includes the system tray
        # we want to provide a rect that removes this
        if (icon_dimensions_set 
            and hidden_icon_found
            and start_menu_found):
            rect_task_list = Rect(taskbar_rect.x, 
                                  taskbar_rect.y, 
                                  rect_hidden_icons.x - taskbar_rect.x, 
                                  taskbar_rect.height)
            
            taskbar_data.set(rect_start_button.copy() if rect_start_button else None,
                             rect_search_button.copy() if rect_search_button else None,
                             rect_task_view.copy() if rect_task_view else None,
                             rect_task_list, 
                             icon_width, 
                             icon_height)
            
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
        rect = taskbar_data.rect_task_list
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


