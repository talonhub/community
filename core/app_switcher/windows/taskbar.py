from unittest import case

from talon.windows.ax import Element
from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
from dataclasses import dataclass, asdict
from talon.ui import Rect
import math
import platform

mod = Module()

cron_poll_start_menu = None
cron_show_hidden = None

def first_matching_child(element, **kw):
    if len(kw) > 1:
        raise Exception("Only one matching attribute supported")
    attr, values = list(kw.items())[0]
    return next(e for e in element.children if getattr(e, attr) in values)

import winreg
from typing import Literal, Optional, TypedDict

@dataclass
class TaskbarItemData:
    name: str
    rect: Rect
    element: ui.Element
    control_type: str

def find_clickables(element):    
    items = element.find(control_type="Button", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
    result = []

    for item in items:
        if item.name:
            result.append(TaskbarItemData(item.name, item.rect, item, item.control_type))

    return result

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
class SystemTrayIconData:
    rect: Rect
    name: str

    def __init__(self, rect, name):
        self.name = name
        self.rect = rect

@dataclass
class SystemTrayPositionData:
    rect_hidden_icons: Rect = None
    sys_tray_icons: list[SystemTrayIconData] = None

    def __init__(self):
        pass

    def set(self, rect_hidden_icons, sys_tray_icons):
        self.rect_hidden_icons = rect_hidden_icons
        self.sys_tray_icons = sys_tray_icons
        

@dataclass
class TaskBarPositionData:
    rect_start_button: Rect
    rect_search_button: Rect
    rect_taskbar: Rect
    rect_task_view: Rect
    rect_task_list: Rect
    rect_hidden_icons: Rect
    icon_width: float
    icon_height: float 
    application_start_index: int
    search_index: int
    task_view_index: int

    def __init__(self):
        pass

    def set(self, 
            rect_taskbar,
            rect_start_button, 
            rect_search_button, 
            rect_task_view, 
            rect_task_list,
            rect_hidden_icons,
            icon_width, 
            icon_height,
            task_view_index, 
            search_index,
            application_start_index):
        
        self.rect_taskbar = rect_taskbar
        self.rect_start_button = rect_start_button
        self.rect_search_button = rect_search_button
        self.rect_task_view = rect_task_view
        self.rect_task_list = rect_task_list
        self.rect_hidden_icons = rect_hidden_icons
        self.icon_width = icon_width
        self.icon_height = icon_height
        
        self.task_view_index = task_view_index
        self.search_index = search_index
        self.application_start_index = application_start_index

    def __str__(self):
        return f"rect = {self.rect_task_list}, icon_width = {self.icon_width}, icon_height = {self.icon_height}"

is_windows_eleven = "Windows-11" in platform.platform()
print(platform.platform())
sys_tray_data = SystemTrayPositionData()
taskbar_data = TaskBarPositionData()
canvas_taskbar = None
canvas_system_tray = None
canvas_hidden_icons = None

mod = Module()

@mod.action_class
class Actions:
    def taskbar_hover(index: int):
        """hover over taskbar button"""
        #print(index)
        x_click = taskbar_data.rect_search_button.x
        y_click = taskbar_data.rect_search_button.y + taskbar_data.rect_search_button.height / 2

        # index zero is always the start button
        if index == 0:
            if taskbar_data.rect_start_button:
                x_click = taskbar_data.rect_start_button.x + taskbar_data.rect_start_button.width / 2
        
        # if not the start menu, add the start width to x_click
        if index != 0:
            x_click += taskbar_data.rect_start_button.width
        
        if index > 0:

            # if the search button is enabled, adjust x_click as appropriate
            if taskbar_data.search_index:
                if taskbar_data.search_index == index:
                    x_click += taskbar_data.rect_search_button.width / 2
                else:
                    x_click += taskbar_data.rect_search_button.width

        if index >= taskbar_data.application_start_index:
            x_click += (taskbar_data.icon_width * (index - taskbar_data.application_start_index - .5)) 
    
        actions.mouse_move(x_click, y_click)

    def taskbar_click(mouse_button: int, index: int):
        """Click the taskbar button based on the index"""        
        x, y = ctrl.mouse_pos()

        if index < len(selectable_taskbar_items):
            item = selectable_taskbar_items[index]
            x_click = item.x + item.width / 2
            y_click = item.y + item.height / 2

            is_application = index >= taskbar_data.application_start_index
            
            if is_application and mouse_button == 0:
                actions.mouse_move(x_click, y_click)
                actions.sleep("150ms")
                actions.key(f"super-{index - taskbar_data.application_start_index + 1}")
            else:
                actions.mouse_move(x_click, y_click)
                actions.mouse_click(mouse_button)
                actions.mouse_move(x, y)

            actions.sleep("150ms")
            

    def taskbar_control_click(mouse_button: int, index: int):
        """Click the taskbar button based on the index"""        
        x, y = ctrl.mouse_pos()

        if index < len(selectable_taskbar_items):
            item = selectable_taskbar_items[index]
            x_click = item.x + item.width / 2
            y_click = item.y + item.height / 2

            actions.mouse_move(x_click, y_click)

            actions.key("ctrl:down")
            actions.mouse_click(mouse_button)
            actions.key("ctrl:up")

            actions.sleep("150ms")
            actions.mouse_move(x, y)

    def system_tray_show_hidden():
        """Reveal hidden icons"""
        if sys_tray_data.rect_hidden_icons:
            rect_hidden_icons = sys_tray_data.rect_hidden_icons

            x, y = ctrl.mouse_pos()

            actions.mouse_move(rect_hidden_icons.x + rect_hidden_icons.width / 2, rect_hidden_icons.y)
            actions.mouse_click(0)

            actions.sleep("150ms")
            actions.mouse_move(x, y)

    def system_tray_move(index: int):
        """hover over icon"""
        x, y = ctrl.mouse_pos()
        sys_tray_count = len(sys_tray_data.sys_tray_icons)
        if index >= sys_tray_count:
            if is_hidden_menu_showing:
                sys_tray_icon = main_buttons[index - sys_tray_count]
            else:
                return
        else:       
            sys_tray_icon = sys_tray_data.sys_tray_icons[index].rect

        actions.mouse_move(sys_tray_icon.x + sys_tray_icon.width / 2, sys_tray_icon.y + sys_tray_icon.height / 2)

    def system_tray_click(mouse_button: int, index: int):
        """Clicks system tray icon"""

        x, y = ctrl.mouse_pos()
        sys_tray_count = len(sys_tray_data.sys_tray_icons)
        if index >= sys_tray_count:
            if is_hidden_menu_showing:
                sys_tray_icon = main_buttons[index - sys_tray_count]
            else:
                return
        else:       
            sys_tray_icon = sys_tray_data.sys_tray_icons[index].rect

        actions.mouse_move(sys_tray_icon.x + sys_tray_icon.width / 2, sys_tray_icon.y + sys_tray_icon.height / 2)
        actions.mouse_click(mouse_button)

        actions.sleep("150ms")
        actions.mouse_move(x, y)

    def taskbar_force_refresh():
        """Forces fresh of taskbar"""  
        on_screen_change(None)

is_hidden_menu_showing = False
def draw_hidden_icon_canvas(canvas):
    paint = canvas.paint
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    paint.textsize = 20

    if not is_hidden_menu_showing:
        return
    
    index = len(sys_tray_data.sys_tray_icons) + 1
    #print(index)
    for rect in main_buttons:
        x = rect.x
        y = rect.y
        x_end = rect.x + rect.width

        width = x_end - x

        paint.style = paint.Style.FILL
        paint.color = "000000"

        rect_background = Rect(rect.x, rect.y + rect.height *.75, width * .5, rect.height *.25)
        canvas.draw_rect(rect_background)

        x_text_position = rect_background.x + rect_background.width / 2
        y_text_position = rect_background.y + rect_background.height / 1.25

        paint.color = "ffffff"
        canvas.draw_text(f"{index}", x_text_position, y_text_position)
        index = index + 1

def draw_sys_tray_options(canvas):
    paint = canvas.paint
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    paint.textsize = 15
    index = 1
    if sys_tray_data.rect_hidden_icons:
        #print(f"drawing {len(sys_tray_data.sys_tray_icons)}")

        for i in range(0, len(sys_tray_data.sys_tray_icons)):
            icon = sys_tray_data.sys_tray_icons[i]
            if len(icon.name) > 0:
                
                rect = icon.rect

                x = icon.rect.x
                y = icon.rect.y
                x_end = icon.rect.x + icon.rect.width

                width = x_end - x

                paint.style = paint.Style.FILL
                paint.color = "000000"

                rect_background = Rect(rect.x, rect.y + rect.height *.75, width * .5, rect.height *.25)

                canvas.draw_rect(rect_background)

                x_text_position = rect_background.x + rect_background.width / 2
                y_text_position = rect_background.y + rect_background.height / 1.25

                paint.color = "ffffff"
                canvas.draw_text(f"{index}", x_text_position, y_text_position)

            index += 1
        
selectable_taskbar_items = []

def draw_task_bar_options(canvas):
    #print("draw_task_bar_options")
    global selectable_taskbar_items
    selectable_taskbar_items = []

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
        selectable_taskbar_items.append(rect_start_menu)
        

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
        selectable_taskbar_items.append(rect_search_button)

    max_task_list_count = math.floor(rect_task_bar_list.width / taskbar_data.icon_width)

    for index in range(current_index,  current_index + max_task_list_count):
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
        selectable_taskbar_items.append(rect_number_background)

def get_window_class(window: ui.Window):
    cls = None
    if not window:
        return None
    try:
        cls = window.cls
    except Exception as e:
        #app.notify("get_window_class exception - taskbar")
        print(f"exception = {e}")
        cls = None
    
    return cls

def get_windows_ten_taskbar() -> bool:
    """Populated the TaskBarData class for windows 10"""
    return False
    icon_width: float = 0.0
    icon_height: float = 0.0
    icon_dimensions_set: bool = False
    
    ms_tasklist = None
    taskbar = None

    apps = ui.apps(name="Windows Explorer")
    for application in apps:
        for window in application.windows():
            cls = get_window_class(window)

            if cls == "Shell_TrayWnd":
                taskbar = window
                break

    if taskbar:
        ms_tasklist = first_matching_child(taskbar.element, class_name=["MSTaskListWClass"])
        # tray = first_matching_child(taskbar.element, class_name=["TrayNotifyWnd"])
        # pager = first_matching_child(tray, class_name=["SysPager"])
        # toolbar = first_matching_child(pager, class_name=["ToolbarWindow32"])
        # for child in toolbar.children:
        #     #print(f"{child.name} {child.rect.width} {child.rect.height}")
        # break

    # include the task view if enabled
    for e in taskbar.element.children:
        ##print(e)
        if "Task View" in e.name and "Task View" not in icons_to_exclude:
            icon_width = e.rect.width
            icon_height = e.rect.height
            icon_dimensions_set = True
            
    if not taskbar:
        if not ms_tasklist:
            print("failed to find MSTaskListWClass")
            pass
        
        return False
    
    for e in ms_tasklist.children:
        if not icon_dimensions_set:
            print(f"found first icon {e.name} {e.rect}")
            icon_width = e.rect.width
            icon_height = e.rect.height
            icon_dimensions_set = True
            
    if taskbar and icon_dimensions_set:
        rect_taskbar = ms_tasklist.rect.copy()
        taskbar_data.set(rect_taskbar, icon_width, icon_height)
        print(f"all prequistes found for windows 10 taskbar numbers: {taskbar_data}")

        return True
    
    return False

def get_windows_eleven_taskbar() -> bool:
    """Populates the TaskBarData class for windows 11"""
    taskbar = None
    icon_width: float = 0.0
    icon_height: float = 0.0
    icon_dimensions_set: bool = False
    first_icon_rect: Rect = None
    rect_start_button: Rect = None
    rect_task_view: Rect = None
    rect_search_button: Rect = None
    rect_hidden_icons: Rect = None
    hidden_icon_found: bool = False
    start_menu_found: bool = False
    search_button_found: bool = False
    task_view_button_found: bool = False
    sys_tray_icons = []

    task_view_index = None
    search_button_index = None

    # is_taskbar_left_aligned = is_start_left_aligned()
    # task_bar_combine_status = get_taskbar_combine_status()

    # start_menu_configured_correctly = (is_taskbar_left_aligned 
    #     and task_bar_combine_status["primary"] == "always")
   
    # if not is_start_left_aligned():
    #     print("Start menu must be left-aligned")

    # if task_bar_combine_status["primary"] != "always":
    #     print("Start menu icons must be configued to always combine and hide labels")

    # if not start_menu_configured_correctly:
    #     return False
        
    explorer_instances = ui.apps(name="Windows Explorer")

    for instance in explorer_instances:
        try:
            windows = instance.windows()

        except Exception as e:
            print(f"taskbar - caught exception {e}")
            continue

        for window in windows:
            cls = get_window_class(window)

            if cls == "Shell_TrayWnd":
                #print(f"found taskbar {window.title}")
                taskbar = window.element

        if taskbar:
            break

    if not taskbar:
        return False
    
    if taskbar:
        application_start_index = 0
        rect_taskbar = taskbar.rect.copy()
        pinned_found = False
        try:
            clickables = find_clickables(taskbar)
        except Exception as e:
            print(f"start_menu_poller - caught exception {e}")
            cron_poll_start_menu_helper(True)
            return

        #print(f"taskbar rect {rect_taskbar}")
        clickables = [item for item in clickables if item.rect.width > 0 and item.rect.height > 0 and len(item.name.strip()) > 0]
        clickables = sorted(clickables, key=lambda item: item.rect.x)   

        for current_index, item in enumerate(clickables):
            match item.name:
                case "Show Hidden Icons" | "Show Hidden Icons Hide":
                    hidden_icon_found = True
                    rect_hidden_icons = item.rect
                    #sys_tray_icons.append(SystemTrayIconData(item.rect, item.name))
                    #print(f"found hidden icons! {item.name}")
                    
                case "Start":
                    rect_start_button = item.rect
                    start_menu_found = True
                    application_start_index += 1
                    #print(f"found start button! {item.rect}")

                case "Search":
                    rect_search_button = item.rect
                    search_button_index = current_index
                    application_start_index += 1

                    search_button_found = True
                    #print(f"found search button! {item.rect}")

                case "Task View":  
                    rect_task_view = item.rect
                    first_icon_rect = rect_task_view
                    task_view_index = current_index
                    icon_width = item.rect.width
                    icon_height = item.rect.height
                    
                    icon_dimensions_set= True
                    task_view_button_found = True
                    #print(f"found Task View button! {item.rect}")
                            
                case _:
                    if "pinned" in item.name and not pinned_found:
                        icon_width = item.rect.width
                        icon_height = item.rect.height
                        icon_dimensions_set = True
                        pinned_found = True
                        application_start_index = current_index

                    # if rect_hidden_icons and item.rect.x > rect_hidden_icons.x:
                    #     sys_tray_icons.append(SystemTrayIconData(item.rect, item.name))

        # The taskbar rect in windows 11 includes the system tray
        # we want to provide a rect that removes this
        if (icon_dimensions_set 
            and hidden_icon_found
            and start_menu_found):
            rect_task_list = Rect(rect_taskbar.x, 
                                  rect_taskbar.y, 
                                  rect_hidden_icons.x - rect_taskbar.x, 
                                  rect_taskbar.height)
            
            
            sys_tray_icons = sorted(sys_tray_icons, key=lambda icon: int(icon.rect.x))             
            sys_tray_data.set(rect_hidden_icons.copy(), sys_tray_icons)
            taskbar_data.set(rect_taskbar.copy(),
                             rect_start_button.copy() if rect_start_button else None,
                             rect_search_button.copy() if rect_search_button else None,
                             rect_task_view.copy() if rect_task_view else None,
                             rect_task_list, 
                             rect_hidden_icons.copy(),
                             icon_width, 
                             icon_height,
                             task_view_index,
                             search_button_index,
                             application_start_index)
            
            print(f"all prequistes found for windows 11 taskbar numbers: {taskbar_data}")

            #print(f"sys tray = {sys_tray_icons}, count = {len(sys_tray_icons)}")
            return True
    
    return False

def update_task_bar_canvases():
    global canvas_taskbar 
    global canvas_system_tray
    global canvas_hidden_icons

    main_screen = ui.main_screen()
    #print(f"main screen: {main_screen}")
    #print(f"screens: {ui.screens()}")
    
    if canvas_taskbar:
        canvas_taskbar.close()

    if canvas_system_tray:
        canvas_system_tray.close()
    
    if not is_windows_eleven:
        success = get_windows_ten_taskbar()
    else:
        success = get_windows_eleven_taskbar()
        
    if success:
        rect_task_list = taskbar_data.rect_task_list
        rect_taskbar = taskbar_data.rect_taskbar
        rect_hidden = sys_tray_data.rect_hidden_icons

        canvas_taskbar = canvas.Canvas.from_rect(rect_task_list)

        canvas_taskbar.register("draw", draw_task_bar_options)
        canvas_taskbar.freeze()
        
        rect_system_tray = Rect(rect_hidden.x, rect_hidden.y, rect_taskbar.width, rect_taskbar.height)
        canvas_system_tray = canvas.Canvas.from_rect(rect_system_tray)
        canvas_system_tray.register("draw", draw_sys_tray_options)
        canvas_system_tray.freeze()

    else:
        print("taskbar data population failed. Skipping canvas creation")

    return success

def start_menu_poller():
    print("***poll_start_menu started***")
    global cron_poll_start_menu, canvas_hidden_icons
    global pollerSim, pollerCount
    taskbar = None
    rect_hidden_icons: Rect = None
    rect_start_menu: Rect = None
    hidden_icon_found = False
    start_icon_found = False
    search_button_found = False
    task_view_button_found = False
    explorer_instances = ui.apps(name="Windows Explorer")

    for instance in explorer_instances:
        try:
            windows = instance.windows()
            
        except Exception as e:
            print(f"start_menu_poller - caught exception {e}")
            continue

        for window in windows:
            cls = get_window_class(window)

            if cls == "Shell_TrayWnd":
                #print(f"found taskbar {window.title}")
                taskbar = window.element

        if taskbar:
            break

    if not taskbar:
        cleanup_and_retry(True)
        return 

    update_required = False
    if taskbar:
        try:
            clickables = find_clickables(taskbar)
        except Exception as e:
            print(f"start_menu_poller - caught exception {e}")
            cron_poll_start_menu_helper(True)
            return

        for item in clickables:
            match item.name:
                case "Show Hidden Icons" | "Show Hidden Icons Hide":
                    hidden_icon_found = True
                    rect_hidden_icons = item.rect
                
                    if not taskbar_data.rect_hidden_icons:
                        update_required = True
                        #print("hidden status doesn't match")

                    elif abs(rect_hidden_icons.x - taskbar_data.rect_hidden_icons.x) > 15:
                        #print("hidden x position doesn't match")
                        print(rect_hidden_icons)
                        print(taskbar_data.rect_hidden_icons)
                        update_required = True
                    
                case "Start":
                        rect_start_button = item.rect
                        start_menu_found = True

                        if not taskbar_data.rect_start_button:
                            update_required = True
                            print("start status doesn't match")

                        elif rect_start_button.width != taskbar_data.rect_start_button.width:
                            print("start width doesn't match")
                            update_required = True

                case "Search":
                    if item.control_type == "Button":
                        rect_search_button = item.rect
                        search_button_found = True

                        if not taskbar_data.rect_search_button:
                            print("search not found previously")
                            update_required = True

                        elif rect_search_button.width != taskbar_data.rect_search_button.width:
                            print(f"search width doesn't match {rect_search_button.width} vs {taskbar_data.rect_search_button.width}")
                            update_required = True

                        #print(f"found search button! {child2.rect}")

                case "Task View":  
                    rect_task_view = item.rect
                    task_view_button_found = True

                    # if not taskbar_data.rect_task_view:
                    #     print("task view status doesn't match")
                    #     update_required = True

                    # elif rect_task_view.width != taskbar_data.rect_task_view.width:
                    #     print("task view width doesn't match")
                    #     update_required = True
                    # print(f"found Task View button! {child2.rect}")

                            
                case _:
                    pass
                    #print(f"{item.name}")

        if not update_required:
            update_required = (taskbar_data.rect_search_button and not search_button_found or
                            taskbar_data.rect_hidden_icons and not hidden_icon_found)
                
        # the only time we should need to update the canvases is when
        # the rect associated with the system tray changes.
        if update_required:
            #print("redrawing taskbar numbers")
            #actions.app.notify("Redrawing Taskbar Numbers")
            cron_show_hidden_helper(False)

            if update_task_bar_canvases():
                if canvas_hidden_icons:
                    canvas_hidden_icons.resume()
                    canvas_hidden_icons.freeze()

                cron_poll_start_menu_helper(True)
            else:
                cleanup_and_retry(True)
        else:
            cron_poll_start_menu_helper(True)

    #print("***poll_start_menu complete***")


def show_hidden_icon_numbers():
    #print("***show_hidden_icon_numbers started***")
    global main_buttons, canvas_hidden_icons
    active_window = ui.active_window()
    global is_hidden_menu_showing, main_buttons
    main_buttons = []

    if canvas_hidden_icons:
        canvas_hidden_icons.close()
        canvas_hidden_icons = None

    cls = get_window_class(active_window)
    
    if is_hidden_menu_showing:
        if canvas_hidden_icons:
            canvas_hidden_icons.close()
            canvas_hidden_icons = None

    if not cls:
        return
    
    match cls:
        # case "XamlExplorerHostIslandWindow":
        #     print("wat")
        #     active_window = ui.active_window()
            
        #     for child in active_window.element.children:
        #         for child2 in child.children:
        #             print(f"{child2.name}")

        case "TopLevelWindowForOverflowXamlIsland":
            is_hidden_menu_showing = True
            active_element = active_window.element
            for child in active_element.children:
                for child2 in child.children:
                    if (child2.name.strip()):
                        main_buttons.append(child2.rect)

            canvas_hidden_icons = canvas.Canvas.from_rect(active_element.rect)
            canvas_hidden_icons.register("draw", draw_hidden_icon_canvas)
            canvas_hidden_icons.freeze()

        # case "Windows.UI.Core.CoreWindow":
        #     print("core")
        #     if ("Jump List" in active_window.title):
        #         for child in active_window.element.children:
        #             print(child.name)

        #             for child2 in child.children:
        #                 print(child2.name)
        #                 main_buttons.append(child2.rect)   
        # 
    
    #print("***show_hidden_icon_numbers completed***")
       
                
def on_focus_change(_):
    #print(f"***on_focus_change started***")
    global is_hidden_menu_showing, main_buttons, cron_show_hidden, canvas_hidden_icons
    active_window = ui.active_window()
    was_showing = is_hidden_menu_showing

    is_hidden_menu_showing = active_window.title == "System tray overflow window."
   
    if was_showing:
        if canvas_hidden_icons:
            canvas_hidden_icons.close()
            canvas_hidden_icons = None

    # if the numbers are up, try to show the popup
    if is_hidden_menu_showing and canvas_system_tray and canvas_taskbar:
        cron_show_hidden_helper()

    #print(f"***on_focus_change complete {active_window.title}***")

def cron_show_hidden_helper(start = True, time = "500ms", func=show_hidden_icon_numbers):
    global cron_show_hidden
    if cron_show_hidden:
        cron.cancel(cron_show_hidden)
        cron_show_hidden = None

    if start:   
        cron_show_hidden = cron.after(time, func)

def cron_poll_start_menu_helper(start = True, time = "3s", func=start_menu_poller):
    global cron_poll_start_menu

    print(f"cron_poll_start_menu_helper {start}")
    
    if cron_poll_start_menu:
        cron.cancel(cron_poll_start_menu)
        cron_poll_start_menu = None

    if start:   
        cron_poll_start_menu = cron.after(time, func)

def on_screen_change(_):
    global canvas_hidden_icons, canvas_taskbar
    #print(f"on_screen_change started")
    cron_show_hidden_helper(False)
    cron_poll_start_menu_helper(False)
    
    if canvas_hidden_icons:
        canvas_hidden_icons.close()
        canvas_hidden_icons = None

    if canvas_taskbar:
        canvas_taskbar.close()
        canvas_taskbar = None

    if not update_task_bar_canvases():
        cleanup_and_retry(True)
    else:
        cron_poll_start_menu_helper(True)

    #print(f"on_screen_change complete = {result}")

ready_cron = None
def cleanup_and_retry(start=False):
    global ready_cron
    print(f"cleanup_and_retry {start}")
    cron_poll_start_menu_helper(False)
    cron_show_hidden_helper(False)

    if ready_cron:
        cron.cancel(ready_cron)
        ready_cron = None

    if start:   
        ready_cron = cron.after("100ms", on_ready)
        #app.notify("start readycron")

if app.platform == "windows":
    def on_ready():
        if update_task_bar_canvases():
            cron_poll_start_menu_helper(True)
            ui.unregister("screen_change", on_screen_change) 
            ui.unregister("win_focus", on_focus_change)
            ui.register("screen_change", on_screen_change) 
            ui.register("win_focus", on_focus_change)
        else:
            cleanup_and_retry(True)
            

    app.register("ready", on_ready)

    


