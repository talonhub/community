from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
from talon.ui import Rect
from ..operating_system.windows.accessibility import find_all_clickable_rects, find_all_clickable_rects_parallel, get_window_class, find_all_clickables_in_list_parallel
import threading

mod = Module()
mod.tag("hinting_active", desc="Indicates hints are active")
ctx = Context()

canvas_active_window = None
active_window_id = None
clickables = None

ctx = Context()
ctx.matches = r"""
os: windows
"""


explorer_automation_ids =[{'automation_id': 'StatusBarModuleInner'}, 
                          {'automation_id': 'System.StatusBarViewItemCount'}, 
                          {'automation_id': 'PropertyValue'}, 
                          {'automation_id': 'ViewButtonsGroup'}, 
                          {'automation_id': 'ViewMode_Details'}, 
                          {'automation_id': 'ViewMode_LargeIcons'}, 
                          {'automation_id': 'ProperTreeHost'}, 
                          {'automation_id': '100'}, 
                          {'automation_id': 'NonClientVerticalScrollBar'}, 
                          {'automation_id': 'UpButton'}, 
                          {'automation_id': 'UpPageButton'}, 
                          {'automation_id': 'ScrollbarThumb'}, 
                          {'automation_id': 'DownPageButton'}, 
                          {'automation_id': 'DownButton'}, 
                          {'automation_id': 'listview'}, 
                          {'automation_id': 'HorizontalScrollBar'}, 
                          {'automation_id': 'UpButton'}, 
                          {'automation_id': 'ScrollbarThumb'}, 
                          {'automation_id': 'DownPageButton'}, 
                          {'automation_id': 'DownButton'}, 
                          {'automation_id': 'System.ItemNameDisplay'}, 
                          {'automation_id': 'DropDown'}, 
                          {'automation_id': 'System.DateModified'}, 
                          {'automation_id': 'DropDown'}, 
                          {'automation_id': 'System.ItemTypeText'}, 
                          {'automation_id': 'DropDown'}, 
                          {'automation_id': 'System.Size'}, 
                          {'automation_id': 'DropDown'},  
                          {'automation_id': 'System.ItemNameDisplay'}, 
                          {'automation_id': 'System.DateModified'}, 
                          {'automation_id': 'System.ItemTypeText'},
                          {'automation_id': 'System.Size'}, 
                          {'automation_id': 'System.ItemNameDisplay'}, 
                          {'automation_id': 'System.DateModified'}, 
                          {'automation_id': 'System.ItemTypeText'}, 
                          {'automation_id': 'System.Size'}, 
                          {'automation_id': 'TabView'}, 
                          {'automation_id': 'TabListView'}, 
                          {'automation_id': 'CloseButton'}, 
                          {'automation_id': 'AddButton'}, 
                          {'automation_id': 'NavigationCommands'}, 
                          {'automation_id': 'backButton'}, 
                          {'automation_id': 'forwardButton'}, 
                          {'automation_id': 'upButton'}, 
                          {'automation_id': 'refreshButton'}, 
                          {'automation_id': 'PART_AutoSuggestBox'}, 
                          {'automation_id': 'TextBox'}, 
                          {'automation_id': 'FirstCrumbStackPanel'}, 
                          {'automation_id': 'PART_BreadcrumbBar'}, 
                          {'automation_id': 'FileExplorerSearchBox'}, 
                          {'automation_id': 'TextBox'}, 
                          {'automation_id': 'FileExplorerCommandBar'}, 
                          {'automation_id': 'SortAndGroupButton'}, 
                          {'automation_id': 'MoreButton'}, 
                          {'automation_id': 'FileExplorerSecondaryCommandBar'}, 
                          {'automation_id': 'PreviewPaneToggleButton'}, 
                          {'automation_id': 'TitleBar'}, 
                          {'automation_id': 'SystemMenuBar'}, 
                          {'automation_id': 'Minimize-Restore'}, 
                          {'automation_id': 'Maximize-Restore'}, 
                          {'automation_id': 'Close'}]


def label_for_index(n: int) -> str:
    A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    label = ""
    while n >= 0:
        n, remainder = divmod(n, 26)
        label = chr(remainder + ord('A')) + label
        n -= 1
    return label

def draw_hints(canvas):
    global current_button_mapping 
    current_button_mapping = {}

    paint = canvas.paint
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    paint.textsize = 20

    if not clickables:
        return
    
    index = 1

    for rect in clickables:
        paint.style = paint.Style.FILL
        paint.color = "000000"

        rect_background = Rect(rect.x, rect.y + rect.height *.75, 50, 20)
        canvas.draw_rect(rect_background)

        x_text_position = rect_background.x + rect_background.width / 2
        y_text_position = rect_background.y + rect_background.height / 1.25

        label = label_for_index(index - 1)

        paint.color = "ffffff"
        canvas.draw_text(f"{label}", x_text_position, y_text_position)
        index = index + 1
        current_button_mapping[label] = rect

    ctx.tags = ['user.hinting_active']

import re
def strip_more_tabs(title: str) -> str:
    return re.sub(r"\s+and\s+\d+\s+more\s+tab.*", "", title)

control_types = [{"control_type": "Button"},
                 {"control_type": "CheckBox"},
                 {"control_type": "ComboBox"},                 
                 {"control_type": "Edit"},
                 {"control_type": "ListItem"},
                 {"control_type": "ListViewItem"},
                 {"control_type": "Menu"},
                 {"control_type": "MenuItem"},
                 {"control_type": "SplitButton"},
                 {"control_type": "TabItem"},
                 {"control_type": "TreeItem"},]

@ctx.action_class("user")
class Actions:
    def hinting_close(clear_cache):
        """Closes hinting canvas if open"""
        global clickables, canvas_active_window, current_button_mapping, active_window_id

        if canvas_active_window:
            if clear_cache:
                clickables = None
                current_button_mapping = None
                active_window_id = None

            canvas_active_window.close()
            canvas_active_window = None

            ctx.tags = []
            return True
        
        return False
        
    def hinting_toggle():
        """Toggles hints"""
        global is_context_menu_open, clickables, canvas_active_window, current_button_mapping, active_window_id
        print("toggling hints")
        hinting_toggle_pipe()
        return
    
        if actions.user.hinting_close(False):
            return
        
        active_window = ui.active_window()
        element = active_window.element
        
        if not is_context_menu_open:
            #focused_element = ui.focused_element()
            active_window_id = active_window.id

            # match ui.active_app().name:
            #     case "Windows Explorer":
            #         cls = get_window_class(ui.active_window())

            #         match cls:
            #             case "CabinetWClass":
            #                 targets = []
            #                 active_tab_name = strip_more_tabs(ui.active_window().title.replace("- File Explorer", ""))
            #                 match_found = False
            #                 for child in element.children:
            #                     if child.name == "":
            #                         targets.append(child)

            #                     elif child.name.strip() == active_tab_name.strip() and not match_found:
            #                         targets.append(child)
            #                         match_found = True

            #                 #walk(active_window.element)
            #                 app_bar_navigation = element.find_one(automation_id="NavigationCommands", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
            #                 app_bar_nav_buttons = app_bar_navigation.find(control_type="Button", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])

            #                 app_bar_command = element.find_one(automation_id="FileExplorerCommandBar", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
            #                 app_bar_command_buttons = app_bar_command.find(control_type="Button", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])

            #                 app_bar_second_command = element.find_one(automation_id="FileExplorerSecondaryCommandBar", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
            #                 app_bar_second_command_buttons = app_bar_second_command.find(control_type="Button", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])

            #                 tree = element.find_one(automation_id="100", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
            #                 tree_items = tree.find(control_type="TreeItem", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
                            
            #                 listy = element.find_one(control_type="List", name = "Items View", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
            #                 list_items = listy.find(control_type="ListItem", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
                           
            #                 menu_bar = element.find_one(automation_id="TitleBar")
            #                 menu_bar_buttons = menu_bar.find(control_type="Button", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
                            
            #                 tab_list = element.find_one(automation_id="TabView", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
            #                 tab_buttons = tab_list.find(control_type="Button", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
                            
            #                 search_box = element.find_one(automation_id="FileExplorerSearchBox", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
                             
            #                 crumb_stack = element.find_one(automation_id="FirstCrumbStackPanel", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect", "parent"])
            #                 crumb_buttons = crumb_stack.parent.find(control_type="SplitButton", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect", "parent"])
                            
            #                 #listview = element.find_one(automation_id="listview", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect", "parent"])
            #                 #whimmywazzle = [{"control_type":"SplitButton"},{"control_type":"Button"}]
            #                 #listview_buttons = listview.parent.find(*whimmywazzle, visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect", "parent"])

            #                 #view_button_group = element.find_one(automation_id="ViewButtonsGroup", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
            #                 #view_buttons = view_button_group.find(control_type="RadioButton", visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
                            
            #                 #others = element.find(*explorer_automation_ids, visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
            #                 clickables = [item.rect for item in tree_items]
            #                 clickables.append(search_box.rect)
            #                 for item in list_items:
            #                     clickables.append(item.rect)

            #                 for item in app_bar_nav_buttons:
            #                     clickables.append(item.rect)

            #                 for item in app_bar_command_buttons:
            #                     clickables.append(item.rect)

            #                 for item in app_bar_second_command_buttons:
            #                     clickables.append(item.rect)
                            
            #                 for item in tab_buttons:
            #                     clickables.append(item.rect)

            #                 for item in menu_bar_buttons:
            #                     clickables.append(item.rect)

            #                 for crumb in crumb_buttons:
            #                     clickables.append(crumb.rect)

            #                 # for button in listview_buttons:
            #                 #     clickables.append(button.rect)
            #                 #clickables.appednfind_all_clickables_in_list_parallel(active_window, targets) if len(targets) > 0 else []

            #             case _:
            #                 pass
            #                 #clickables = find_all_clickable_rects_parallel(active_window, element)
            #     case _:    
            #         match focused_element.control_type:
            #             case "Menu" | "MenuItem":
            #                 element = focused_element.parent 

            #             case "Edit":
            #                 match active_window.cls:
            #                     case "Windows.UI.Core.CoreWindow":
            #                         element = active_window.element.parent


        items = element.find(*control_types, 
                             visible_only=True,
                             is_offscreen=False,
                             is_keyboard_focusable=True,
                             prefetch=["rect", "control_type", "is_keyboard_focusable", "is_enabled"])
        
        clickables = [el.rect for el in items]
        help(element.find)

        # if clickables and len(clickables) > 0:
        #     canvas_active_window = canvas.Canvas.from_rect(ui.main_screen().rect)
        #     canvas_active_window.register("draw", draw_hints)
        #     canvas_active_window.freeze()

    def hinting_select(mouse_button: int, label: str, click_count: int):
        """Click the hint based on the index"""        

        label = label.upper()
        if label not in current_button_mapping:
            return

        rect = current_button_mapping[label]
        x_click = rect.x + rect.width / 2
        y_click = rect.y + rect.height / 2

        actions.mouse_move(x_click, y_click)
        
        if click_count > 0:
            for i in range(0, click_count):
                actions.mouse_click(mouse_button)

        actions.user.hinting_close(True)

import win32pipe
import win32file
import threading

def send_to_pipe(command: str):
    """Send a command to the HintOverlay named pipe in a non-blocking thread"""
    def _send():
        try:
            # Ensure command ends with newline
            if not command.endswith('\n'):
                command_with_newline = command + '\n'
            else:
                command_with_newline = command
            
            handle = win32file.CreateFile(
                r"\\.\pipe\HintOverlay_Pipe",  # ← Note: underscore, not camelCase
                win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            win32file.WriteFile(handle, command_with_newline.encode('utf-8'))
            handle.Close()
            print(f"✓ Command sent: {command.strip()}")
        except Exception as e:
            print(f"✗ Pipe error: {e}")
    
    threading.Thread(target=_send, daemon=True).start()

def hinting_toggle_pipe():
    """Toggle hints using the named pipe"""
    send_to_pipe("TOGGLE")

def hinting_select_pipe(label: str):
    """Select a hint using the named pipe"""
    send_to_pipe(f"SELECT {label}")

def hinting_deactivate_pipe():
    """Deactivate the overlay using the named pipe"""
    send_to_pipe("DEACTIVATE")

is_context_menu_open = False
def on_win_open(window):
    global is_context_menu_open, clickables, active_window_id
    #print(f"win open - title = {window.title} cls = {window.cls} id = {window.id}")

    match window.cls:

        # file explorer context menu
        case "#32768":
            clickables = find_all_clickable_rects(None, window.element)
            active_window_id = window.id
            is_context_menu_open = True

        # taskbar context menus
        case "Xaml_WindowedPopupClass":
            if window.title in ("PopupHost"):
                clickables = find_all_clickable_rects(None, window.element)
                active_window_id = window.id
                is_context_menu_open = True

def on_win_close(window):
    global is_context_menu_open, active_window_id
    match window.cls:

        # file explorer context menu
        case "#32768":
            is_context_menu_open = False
            active_window_id = None
            actions.user.hinting_close(True)

        # taskbar context menus
        case "Xaml_WindowedPopupClass":
            if window.title in ("PopupHost"):
                active_window_id = None
                is_context_menu_open = False
                actions.user.hinting_close(True)

    if active_window_id == window.id:
        actions.user.hinting_close(True)

def on_win_hide(window):
    on_win_close(window)

def on_win_disable(window):
    on_win_close(window)

def on_win_title(window):
    if window.id != active_window_id:
        return
    else:
        on_win_close(window)

def on_win_focus(_):
    window = ui.active_window()

    if canvas_active_window:
        if active_window_id != window.id:
           actions.user.hinting_close(True)
    
if app.platform == "windows":
    ui.register("win_focus", on_win_focus)
    ui.register("win_open", on_win_open)
    ui.register("win_hide", on_win_hide)
    ui.register("win_close", on_win_close)
    ui.register("win_disable", on_win_disable)
    ui.register("win_title", on_win_title)
    #ui.register("", print)


#control_types = [{"control_type": "Button"}]
def walk(element, depth=0):
    result = []
    if element.automation_id:
        #result.append({"automation_id": element.automation_id})

        print("  " * depth + f"{element.control_type}: {element.name}, automation_id = {element.automation_id}") 
    
    try:
        for child in element.children:
            walk(child, depth + 1)
    except (OSError, RuntimeError, AttributeError):
        return []

    return result