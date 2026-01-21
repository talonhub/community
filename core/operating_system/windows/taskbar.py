from talon.windows.ax import Element
from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
from dataclasses import dataclass, asdict
from talon.ui import Rect
import math
import platform
from enum import Enum

mod = Module()
mod.tag("taskbar_canvas_popup_showing", desc="Indicates a taskbar popup is showing")
ctx = Context()


cron_poll_start_menu = None
cron_delay_showing_canvas = None

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

class ExplorerPopUpState(Enum):
    NONE = 0
    DESKTOP = 1
    SYSTEM_TRAY = 2
    START_MENU = 3
    START_MENU_CONTEXT_MENU = 4
    SEARCH_MENU = 5
    TASK_VIEW = 6
    TASK_BAR_JUMP_LIST = 7
    NOTIFICATION_CENTER = 8
    CONTROL_CENTER = 9
    GENERIC_CONTEXT_MENU = 10
    JUMP_LIST_CONTEXT_MENU = 11
    PROGRAM_MANAGER = 12
    SNAP_ASSIST = 13
    FILE_EXPLORER = 14

class ExplorerPopUpElementStrategy(Enum):
    FOCUSED_ELEMENT = 0
    FOCUSED_ELEMENT_PARENT = 1
    ACTIVE_WINDOW_PARENT = 2
    ACTIVE_WINDOW = 3

@dataclass
class ExplorerPopupStatus:
    state: ExplorerPopUpState
    strategy: ExplorerPopUpElementStrategy
    element_override: Element

    def __init__(self, state=ExplorerPopUpState.NONE, element_override: Element =None):
        self.state = state
        self.element_override = element_override   
        self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW

    def set(self, state: ExplorerPopUpState, element_override: Element = None, strategy=ExplorerPopUpElementStrategy.FOCUSED_ELEMENT):
        self.state = state
        self.element_override = element_override    

    def reset(self):
        self.state = ExplorerPopUpState.NONE
        self.element_override = None   
        self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW    

    def update_state(self):
        active_window = ui.active_window()
        focused_element = ui.focused_element()

        try:
            parent_element = focused_element.parent
        except Exception as e:
            print("failed to get parent")
            parent_element = None

        cls = get_window_class(active_window)

        self.state = ExplorerPopUpState.NONE
        self.strategy = ExplorerPopUpElementStrategy.FOCUSED_ELEMENT_PARENT

        match cls:
            case "Windows.UI.Core.CoreWindow":
                if (parent_element and (focused_element.name == "Lock" or focused_element.parent.name == "Lock")):
                    self.state = ExplorerPopUpState.NONE
                elif ((focused_element.name == "Notification Center")):
                    self.state = ExplorerPopUpState.NOTIFICATION_CENTER
                    self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW
                elif "Jump List" in active_window.title:
                    self.state = ExplorerPopUpState.JUMP_LIST_CONTEXT_MENU
                    self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW
                elif "Search" == active_window.title: #and parent_element and parent_element.name == "Start":
                    if parent_element:
                        self.state = ExplorerPopUpState.START_MENU
                        if parent_element.parent and parent_element.parent.name == "Start":
                            self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW_PARENT
                        else:
                            self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW

                elif "Notification Center":
                    self.state = ExplorerPopUpState.NOTIFICATION_CENTER
                    self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW

            case "ControlCenterWindow":
                self.state = ExplorerPopUpState.CONTROL_CENTER

            case "ProgMan":
                self.state = ExplorerPopUpState.PROGRAM_MANAGER
                self.strategy = ExplorerPopUpElementStrategy.FOCUSED_ELEMENT_PARENT

            case "Shell_TrayWnd":
                # if focused_element.name in ("Installed apps", "Desktop"):
                #     self.state = ExplorerPopUpState.GENERIC_CONTEXT_MENU
                if focused_element.control_type == "MenuItem":
                    self.state = ExplorerPopUpState.NONE

                # there's a weird case where if you right click on empty space in the taskbar,
                # and then open the start menu, we end up with the traywnd class for the start menu.
                # go figure?
                elif (focused_element.name == "Search box"):
                    self.state = ExplorerPopUpState.START_MENU
                    self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW_PARENT

                elif (parent_element.name == "Running applications"):
                    self.state = ExplorerPopUpState.TASK_VIEW
                    self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW

            case "XamlExplorerHostIslandWindow":
                match active_window.title:
                    case "Task View":
                        self.state = ExplorerPopUpState.TASK_VIEW
                        self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW
                    case "Snap Assist":
                        self.state = ExplorerPopUpState.SNAP_ASSIST
                        self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW

            case "ControlCenterWindow":
                self.state = ExplorerPopUpState.CONTROL_CENTER
                self.strategy = ExplorerPopUpElementStrategy.FOCUSED_ELEMENT_PARENT

            case _:
                if active_window.title == "System tray overflow window.":
                    self.state = ExplorerPopUpState.SYSTEM_TRAY
                    self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW
                elif focused_element.control_type == "ListItem" and (parent_element and "Desktop" in parent_element.name):
                    self.state = ExplorerPopUpState.NONE
                    self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW

                elif "File Explorer" in active_window.title:
                    self.state = ExplorerPopUpState.NONE
                    self.strategy = ExplorerPopUpElementStrategy.ACTIVE_WINDOW                 



        #print(f"cls = {cls} win_title = {active_window.title} element = {focused_element.name}, parent = {parent_element.name} control_type = {focused_element.control_type} parent_control_type = {parent_element.control_type if parent_element else "None"}")
    

explorer_popup_status = ExplorerPopupStatus()

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

    def __init__(self, rect_hidden_icons, sys_tray_icons):
        self.rect_hidden_icons = rect_hidden_icons
        self.sys_tray_icons = sys_tray_icons

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

    def __init__(self, 
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
system_try_data = None
taskbar_data = None
canvas_taskbar = None
canvas_system_tray = None
canvas_popup = None
canvas_jump_list = None

mod = Module()

@mod.action_class
class Actions:
    def taskbar_hide(show: bool):
        """"""
        if show:
            if canvas_popup:
                canvas_popup.freeze()

            if canvas_system_tray:
                canvas_system_tray.freeze()

            if canvas_taskbar:
                canvas_taskbar.freeze()
        else:
            if canvas_popup:
                canvas_popup.hide()

            if canvas_system_tray:
                canvas_system_tray.hide()

            if canvas_taskbar:
                canvas_taskbar.hide()

        cron.after("500ms", finish_capture)

    def taskbar_hover(index: int):
        """hover over taskbar button"""
        #print(index)
        x_click = taskbar_data.rect_search_button.x
        y_click = taskbar_data.rect_search_button.y + taskbar_data.rect_search_button.height / 2

        # index zero is always the start button
        if index == 0:
            if taskbar_data.rect_start_button:
                x_click = taskbar_data.rect_start_button.x + taskbar_data.rect_start_button.width / 2
        else:
            x_click = taskbar_data.rect_start_button.x + taskbar_data.rect_start_button.width

            # if the search button is enabled, adjust x_click as appropriate
            if taskbar_data.search_index:
                if taskbar_data.search_index == index:
                    x_click += taskbar_data.rect_search_button.width / 2
                else:
                    x_click += taskbar_data.rect_search_button.width

        if index >= taskbar_data.application_start_index:
            x_click += (taskbar_data.icon_width * (index - taskbar_data.application_start_index - .5)) 
    
        actions.mouse_move(x_click, y_click)

    def taskbar_popup(mouse_button: int, index: int, click_count: int):
        """Click the taskbar popup button based on the index"""        
        x, y = ctrl.mouse_pos()  

        index = index - popup_start_index
        if index > len(buttons_popup):
            return

        x_click = buttons_popup[index].x + buttons_popup[index].width / 2
        y_click = buttons_popup[index].y + buttons_popup[index].height / 2

        actions.mouse_move(x_click, y_click)
        
        for i in range(0, click_count):
            actions.mouse_click(mouse_button)

        actions.sleep("150ms")

        actions.mouse_move(x, y)      

    def taskbar_click(mouse_button: int, index: int):
        """Click the taskbar button based on the index"""        
        x, y = ctrl.mouse_pos()
        
        #print(index)
        x_click = taskbar_data.rect_search_button.x
        y_click = taskbar_data.rect_search_button.y + taskbar_data.rect_search_button.height / 2

        # index zero is always the start button
        if index == 0:
            if taskbar_data.rect_start_button:
                x_click = taskbar_data.rect_start_button.x + taskbar_data.rect_start_button.width / 2
        else:
            x_click = taskbar_data.rect_start_button.x + taskbar_data.rect_start_button.width

            # if the search button is enabled, adjust x_click as appropriate
            if taskbar_data.search_index:
                if taskbar_data.search_index == index:
                    x_click = taskbar_data.rect_search_button.x + (taskbar_data.rect_search_button.width / 2)
                else:
                    x_click += taskbar_data.rect_search_button.width
                    
            if taskbar_data.task_view_index:
                if taskbar_data.task_view_index == index:
                    x_click += taskbar_data.rect_task_view.width / 2
                elif index >= taskbar_data.application_start_index:
                    x_click += taskbar_data.rect_task_view.width

        if index >= taskbar_data.application_start_index:
            #print("app start")
            x_click += (taskbar_data.icon_width * (index - taskbar_data.application_start_index + 1 - .5)) 
    
        actions.mouse_move(x_click, y_click)
        actions.mouse_click(mouse_button)

        actions.sleep("150ms")
        actions.mouse_move(x, y)

    def taskbar_control_click(mouse_button: int, index: int):
        """Click the taskbar button based on the index"""        
        x, y = ctrl.mouse_pos()
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

        actions.key("ctrl:down")
        actions.mouse_click(mouse_button)
        actions.key("ctrl:up")

        actions.sleep("150ms")
        actions.mouse_move(x, y)

    def system_tray_show_hidden():
        """Reveal hidden icons"""
        if system_try_data.rect_hidden_icons:
            rect_hidden_icons = system_try_data.rect_hidden_icons

            x, y = ctrl.mouse_pos()

            actions.mouse_move(rect_hidden_icons.x + rect_hidden_icons.width / 2, rect_hidden_icons.y)
            actions.mouse_click(0)

            actions.sleep("150ms")
            actions.mouse_move(x, y)

    def system_tray_move(index: int):
        """hover over icon"""
        x, y = ctrl.mouse_pos()
        sys_tray_count = len(system_try_data.sys_tray_icons)
        if index >= sys_tray_count:
            if explorer_popup_status.state != ExplorerPopupStatus.NONE:
                sys_tray_icon = buttons_popup[index - sys_tray_count]
            else:
                return
        else:       
            sys_tray_icon = system_try_data.sys_tray_icons[index].rect

        actions.mouse_move(sys_tray_icon.x + sys_tray_icon.width / 2, sys_tray_icon.y + sys_tray_icon.height / 2)

    def system_tray_click(mouse_button: int, index: int):
        """Clicks system tray icon"""

        x, y = ctrl.mouse_pos()
        sys_tray_count = len(system_try_data.sys_tray_icons)
        if index >= sys_tray_count:
            if explorer_popup_status.state == ExplorerPopUpState.SYSTEM_TRAY:
                sys_tray_icon = buttons_popup[index - sys_tray_count]
            else:
                return
        else:       
            sys_tray_icon = system_try_data.sys_tray_icons[index].rect

        actions.mouse_move(sys_tray_icon.x + sys_tray_icon.width / 2, sys_tray_icon.y + sys_tray_icon.height / 2)
        actions.mouse_click(mouse_button)

        actions.sleep("150ms")
        actions.mouse_move(x, y)

    def taskbar_force_refresh():
        """Forces fresh of taskbar"""  
        global taskbar_data
        taskbar_data = None
        cron_poll_start_menu_helper(False)

        start_menu_poller()
        ui.unregister("screen_change", on_screen_change) 
        ui.unregister("element_focus", on_focus_change)

        ui.register("screen_change", on_screen_change) 
        ui.register("element_focus", on_focus_change)        
    
        cron_poll_start_menu_helper()
        
        

popup_start_index = 0

def draw_canvas_popup(canvas):
    #print("draw_canvas_popup")
    ctx.tags = ['user.taskbar_canvas_popup_showing']

    paint = canvas.paint
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    paint.textsize = 20

    if explorer_popup_status.state == ExplorerPopUpState.NONE:
        return
    
    index = popup_start_index + 1
    #print(f"mainbuttons {len(buttons_popup)} {buttons_popup}")
    for rect in buttons_popup:
        x = rect.x
        y = rect.y
        x_end = rect.x + rect.width

        width = x_end - x

        paint.style = paint.Style.FILL
        paint.color = "000000"

        rect_background = Rect(rect.x, rect.y + rect.height *.75, 50, 20)
        canvas.draw_rect(rect_background)

        x_text_position = rect_background.x + rect_background.width / 2
        y_text_position = rect_background.y + rect_background.height / 1.25

        paint.color = "ffffff"
        canvas.draw_text(f"{index}", x_text_position, y_text_position)
        index = index + 1

def draw_canvas_system_tray(canvas):
    paint = canvas.paint
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    paint.textsize = 15
    index = 1

    if system_try_data.rect_hidden_icons:
        #print(f"drawing {len(sys_tray_data.sys_tray_icons)}")

        for i in range(0, len(system_try_data.sys_tray_icons)):
            icon = system_try_data.sys_tray_icons[i]
            if len(icon.name) > 0:
                
                rect = icon.rect

                x = icon.rect.x
                y = icon.rect.y
                x_end = icon.rect.x + icon.rect.width

                width = x_end - x

                paint.style = paint.Style.FILL
                paint.color = "000000"

                rect_background = Rect(icon.rect.x - icon.rect.width / 2 - 10, icon.rect.y + rect.height - 30, 20, 20)
                #canvas.draw_rect(rect_background)

                x_text_position = icon.rect.x + icon.rect.width / 2
                y_text_position = icon.rect.y + rect.height *.9

                paint.color = "ffffff"
                canvas.draw_text(f"{index}", x_text_position, y_text_position)

            index += 1
        
def draw_task_bar_options(canvas):
    #print("draw_task_bar_options")
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

def get_window_class(window: ui.Window) -> bool:
    cls = None
    if not window:
        return None
    try:
        cls = window.cls
    except Exception as e:
        #app.notify("get_window_class exception - taskbar")
        print(f"get_window_class exception = {e}")
        cls = None
    
    return cls

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
            #print("failed to find MSTaskListWClass")
            pass
        
        return False
    
    for e in ms_tasklist.children:
        if not icon_dimensions_set:
            #print(f"found first icon {e.name} {e.rect}")
            icon_width = e.rect.width
            icon_height = e.rect.height
            icon_dimensions_set = True
            
    if taskbar and icon_dimensions_set:
        rect_taskbar = ms_tasklist.rect.copy()
        taskbar_data.set(rect_taskbar, icon_width, icon_height)
        #print(f"all prequistes found for windows 10 taskbar numbers: {taskbar_data}")

        return True
    
    return False

count = 0
simcount = 3
def get_windows_eleven_taskbar():
    """Populates the TaskBarData class for windows 11"""
    taskbar = None
    global count, simcount
    icon_dimensions_set: bool = False
    first_icon_rect: Rect = None
    rect_start_button: Rect = None
    rect_task_view: Rect = None
    rect_search_button: Rect = None
    rect_hidden_icons: Rect = None
    sys_tray_icons = []

    task_view_index = None
    search_button_index = None

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

    for explorer_instances in apps:
        try:
            windows = explorer_instances.windows()
        except Exception as e:
            print(f"taskbar - caught exception {e}")
            continue

        for window in windows:
            cls = get_window_class(window)

            if cls == "Shell_TrayWnd":
                taskbar = window.element
                print(f"found taskbar cls = {cls} {window.title} parent = {taskbar.parent} control_type = {taskbar.control_type}")

        if taskbar:
            break

    if not taskbar:
        return False, None, None
    
    if taskbar:
        rect_taskbar = taskbar.rect

        taskbar_clickables = find_all_clickable_elements(taskbar)
        
        for element in taskbar_clickables:
            match element.name:
                case "Show Hidden Icons" | "Show Hidden Icons Hide":
                    rect_hidden_icons = element.rect
                    hidden_icon_found = True

                case "Search":
                    rect_search_button = element.rect
                    search_button_found = True

                case "Start":
                    rect_start_button = element.rect
                    start_menu_found = True

                case "Task View":
                    rect_task_view = element.rect
                    task_view_button_found = True
                case _:
                    if not icon_dimensions_set:
                        first_icon_rect = element.rect
                        icon_dimensions_set = True
            
        application_start_index = 1
        if search_button_found:
            search_button_index = 1
            application_start_index = 2

        if task_view_button_found:
            if search_button_found:
                task_view_index = 2
                application_start_index = 3
            else:
                task_view_index = 1
                application_start_index = 2

        for element in taskbar_clickables:
            if rect_hidden_icons and element.rect.x >= rect_hidden_icons.x:
                sys_tray_icons.append(SystemTrayIconData(element.rect.copy(), element.name))

        # The taskbar rect in windows 11 includes the system tray
        # we want to provide a rect that removes this
        if (icon_dimensions_set and rect_hidden_icons):
            rect_task_list = Rect(rect_taskbar.x, 
                                  rect_taskbar.y, 
                                  rect_hidden_icons.x - rect_taskbar.x, 
                                  rect_taskbar.height)
            
            sys_tray_icons = sorted(sys_tray_icons, key=lambda icon: int(icon.rect.x)) 
            system_tray = SystemTrayPositionData(rect_hidden_icons.copy(), sys_tray_icons)
            task_bar = TaskBarPositionData(rect_taskbar.copy(),
                             rect_start_button.copy() if rect_start_button else None,
                             rect_search_button.copy() if rect_search_button else None,
                             rect_task_view.copy() if rect_task_view else None,
                             rect_task_list, 
                             rect_hidden_icons.copy(),
                             first_icon_rect.width, 
                             first_icon_rect.height,
                             task_view_index,
                             search_button_index,
                             application_start_index)
            
            #print(f"all prequistes found for windows 11 taskbar numbers: {task_bar} {system_tray}")

            #print(f"sys tray = {sys_tray_icons}, count = {len(sys_tray_icons)}")
            return True, task_bar, system_tray
    
    return False, None, None

def create_task_bar_canvases(taskbar: TaskBarPositionData, system_tray: SystemTrayPositionData):
    global taskbar_data, system_try_data
    global canvas_taskbar 
    global canvas_system_tray
    global canvas_popup

    taskbar_data = taskbar
    system_try_data = system_tray
    
    if canvas_taskbar:
        canvas_taskbar.close()

    if canvas_system_tray:
        canvas_system_tray.close()
    
    rect_task_list = taskbar_data.rect_task_list
    rect_taskbar = taskbar_data.rect_taskbar
    rect_hidden = system_try_data.rect_hidden_icons

    canvas_taskbar = canvas.Canvas.from_rect(rect_task_list)

    canvas_taskbar.register("draw", draw_task_bar_options)
    canvas_taskbar.freeze()
    
    rect_system_tray = Rect(rect_hidden.x, rect_hidden.y, rect_taskbar.width - rect_hidden.x, rect_taskbar.height)
    canvas_system_tray = canvas.Canvas.from_rect(rect_system_tray)
    canvas_system_tray.register("draw", draw_canvas_system_tray)
    canvas_system_tray.freeze()

def start_menu_poller():
    print("***poll_start_menu started***")
    global canvas_popup, canvas_taskbar, canvas_system_tray
    global taskbar_data, system_try_data
    success, task_bar, sys_tray = get_windows_eleven_taskbar()

    # if something's gone horribly wrong, close everything
    if not success:
        cleanup_and_retry()
        return

    # if the taskbar itself has focus, skip updates until it loses focus
    # we get garbage data in this case
    active_window = ui.active_window()
    cls = get_window_class(active_window)

    if cls == "Shell_TrayWnd":
        cron_poll_start_menu_helper()
        return        

    update_required = (taskbar_data == None 
                       
                       # check if the sys tray has changed
                       or (len(system_try_data.sys_tray_icons) != len(sys_tray.sys_tray_icons)) 

                       # check if the icon width has changed
                       or (taskbar_data.icon_width != task_bar.icon_width or taskbar_data.icon_height != task_bar.icon_height)

                       # check if the start index has changed. Indicates the task view or search button
                       # was disabled
                       or (taskbar_data.application_start_index != task_bar.application_start_index)

                       # check if search button status has changed
                       or (taskbar_data.rect_search_button and not task_bar.rect_search_button)
                       or (not taskbar_data.rect_search_button and task_bar.rect_search_button)
                       or (taskbar_data.rect_search_button and task_bar.rect_search_button 
                           and taskbar_data.rect_search_button.width != task_bar.rect_search_button.width)

                       # check if task view button status has changed
                       or (taskbar_data.rect_task_view and not task_bar.rect_task_view)
                       or (not taskbar_data.rect_task_view and task_bar.rect_task_view)
    )
    
    if update_required:
        cron_delay_canvas_helper(False)
        cron_poll_start_menu_helper(False)
        create_task_bar_canvases(task_bar, sys_tray)

        if canvas_popup:
            show_canvas_popup()

        app.notify("Redrawing taskbar")
            

    cron_poll_start_menu_helper()
    #print("***poll_start_menu complete***")

def is_clickable(element, depth=0):
    try:
        if element.control_type in ("Button", "ListViewItem", "ListItem", "Menu"):
            return True
        
        pattern = element.invoke_pattern

        if pattern and not isinstance(pattern, str):
            return True
        else:
            if element.name in ["Shut down or sign out"]:
                return True
            
            return False
    except Exception as e:
        if element.name in ["Shut down or sign out"]:
            return True
        
        return False
    

def find_all_clickable_rects(element, depth=0) -> list[Rect]:
    result = []
    if (is_clickable(element)):
        result.append(element.rect)

    for child in element.children:
        child_result = find_all_clickable_rects(child, depth + 1)
        result.extend(child_result)

    return result

def find_all_clickable_elements(element, depth=0) -> list:
    result = []

    if (is_clickable(element)):
        result.append(element)
        #print("  " * depth + f"{element.control_type}: {element.name}")
    #else:
        #print("  " * depth + f"*{element.control_type}: {element.name}")

    for child in element.children:
        child_result = find_all_clickable_elements(child, depth + 1)
        result.extend(child_result)

    return result


def walk(element, depth=0):
    print("  " * depth + f"{element.control_type}: {element.name}")
    try:
        for child in element.children:
            walk(child, depth + 1)
    except (OSError, RuntimeError):
        pass  # Element became stale

#walk(ui.active_window().element)

def show_canvas_popup():
    global canvas_popup, buttons_popup, popup_start_index
    active_window = ui.active_window()
    focused_element = ui.focused_element()
    element = None

    #print(f"title = {active_window.title} {focused_element} {focused_element.parent} {active_window.element.parent}")

    match explorer_popup_status.strategy:
        case ExplorerPopUpElementStrategy.ACTIVE_WINDOW:
            element = active_window.element
        case ExplorerPopUpElementStrategy.ACTIVE_WINDOW_PARENT:
            element = active_window.element.parent
        case ExplorerPopUpElementStrategy.FOCUSED_ELEMENT:
            element = focused_element
        case ExplorerPopUpElementStrategy.FOCUSED_ELEMENT_PARENT:
            element = focused_element.parent

    # if we've somehow reach the desktop element, something's gone horribly wrong
    # so, skip
    if "Desktop" in element.name and element.control_type == "Pane":
        print("Prevent enumerating the desktop - skipping")
        explorer_popup_status.set(ExplorerPopUpState.NONE)
        return

    buttons_popup = find_all_clickable_rects(element)

    #print(f"show_canvas_popup {buttons_popup}")

    if canvas_popup:
        canvas_popup.close()
        canvas_popup = None

    canvas_popup = canvas.Canvas.from_rect(element.rect)
    canvas_popup.register("draw", draw_canvas_popup)
    canvas_popup.freeze()

def on_focus_change(_):
    #print(f"***on_focus_change started***")
    global buttons_popup, cron_delay_showing_canvas
    global canvas_popup, popup_start_index

    
    #is_menu_bar = cls == "Tray Window" and focused_element.control_type == "MenuBar"
    #2026-01-19 05:08:33.436    IO cls = = <menu bar 'Application'>, parent = <window 'T'> Desktop 1 control_type = MenuBar parent_control_type = Window
    # if the taskbar itself has focus, ignore for now
    if canvas_popup:
        cron_delay_canvas_helper(False)
        canvas_popup.close()
        ctx.tags = []
        canvas_popup = None

    active_app = ui.active_app()
    if active_app.name not in ("Windows Explorer", "SearchHost.exe", "Windows Shell Experience Host", "ShellHost", "Windows Start Experience Host"):
        print(f"{active_app.name} - skipping")
        explorer_popup_status.reset()
        return 

    explorer_popup_status.update_state()

    #print(explorer_popup_status)
    if explorer_popup_status.state != ExplorerPopUpState.NONE:

        if explorer_popup_status.state == ExplorerPopUpState.SYSTEM_TRAY:
            popup_start_index = len(system_try_data.sys_tray_icons)
            cron_delay_canvas_helper(start=True,func=show_canvas_popup)
        else:
            popup_start_index = 0
            cron_delay_canvas_helper(start=True,time="50ms",func=show_canvas_popup)

    #print(f"***on_focus_change complete {active_window.title}***")

def cron_delay_canvas_helper(start = True, time = "50ms", func=show_canvas_popup):
    global cron_delay_showing_canvas

    if cron_delay_showing_canvas:
        cron.cancel(cron_delay_showing_canvas)
        cron_delay_showing_canvas = None

    if start:   
        cron_delay_showing_canvas = cron.after(time, func)

def cron_poll_start_menu_helper(start = True, time = "500ms", func=start_menu_poller):
    global cron_poll_start_menu

    if cron_poll_start_menu:
        cron.cancel(cron_poll_start_menu)
        cron_poll_start_menu = None

    if start:   
        cron_poll_start_menu = cron.after(time, func)

def cleanup_and_retry():
    # reset data
    global taskbar_data, system_try_data

    cron_delay_canvas_helper(False)
    cron_poll_start_menu_helper(False)

    taskbar_data = None
    system_try_data = None

    if canvas_taskbar: 
        canvas_taskbar.close()
    
    if canvas_system_tray:
        canvas_system_tray.close()

    if canvas_popup:
        canvas_popup.close()

    # attempt to recover
    print("Failed to get taskbar, attempting recovery")
    #app.notify("Failed to get taskbar, attempting recovery")

    cron_poll_start_menu_helper(True, time = "100ms")





def on_screen_change(_):
    global canvas_popup
    #print(f"on_screen_change started")
    cron_delay_showing_canvas(False)

    success, task_bar, sys_tray = get_windows_eleven_taskbar()
    
    if success:
        create_task_bar_canvases(task_bar, sys_tray)

        if canvas_popup:
            canvas_popup.close()
            canvas_popup = None
    else:
        cleanup_and_retry()

    #print(f"on_screen_change complete = {result}")

if app.platform == "windows":
    def on_ready():
        global cron_poll_start_menu
        success, task_bar, sys_tray = get_windows_eleven_taskbar()

        if success:
            create_task_bar_canvases(task_bar, sys_tray)
            ui.register("screen_change", on_screen_change) 
            ui.register("element_focus", on_focus_change)
            cron_poll_start_menu_helper()
        else:
            cleanup_and_retry()

    app.register("ready", on_ready)

