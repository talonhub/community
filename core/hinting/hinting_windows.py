from talon import Context, Module, actions, app, ui, canvas
from talon.ui import Rect
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def label_for_index(n: int) -> str:
    A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < 26:
        return A[n]

    m = n - 26
    return A[m // 26] + A[m % 26]

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
                 {"control_type": "ComboBox"},                 
                 {"control_type": "CheckBox"},
                 {"control_type": "Edit"},
                 {"control_type": "TreeItem"},
                 {"control_type": "TabItem"},
                 {"control_type": "SplitButton"},
                 {"control_type": "ListViewItem"},
                 {"control_type": "ListItem"},
                 {"control_type": "Menu"},
                 {"control_type": "MenuItem"},]

def find_clickables(element):    
    #help(element.find)
    items = element.find(*control_types, visible_only=True,is_offscreen=False,is_enabled=True,prefetch=["rect"])
    clickables = []
    for item in items:
        clickables.append(item.rect)

    return clickables

def get_window_class(window: ui.Window) -> bool:
    cls = None
    if not window:
        return None
    try:
        cls = window.cls
    except Exception as e:
        cls = None

    return cls

def find_all_clickables_in_list_parallel(window, targets):
    results = []
    # First pass: select which children to process (serial, deterministic)
    # Parallel execution using threads
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(find_all_clickable_rects_parallel, window, child)
            for child in targets
        ]

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.extend(result)
            except Exception as exc:
                # handle/log per-task failures without killing the whole run
                print(f"Thread failed: {exc}")

    return results

def is_within_window(window, element):
    try:
        rect = element.rect
    except:
        rect = None

    if window and rect and window.rect.contains(rect.x, rect.y) or not window:
        return True
    
    return False

def is_clickable(element, depth=0):
    clickable = False

    try:
        control_type = element.control_type
    except:
        return clickable

    match control_type:
        case "Button":
            clickable = True
        case "ComboBox":
            clickable = True
        case "CheckBox":
            clickable = True
        case "Edit":
            clickable = True
        case "TreeItem":
            clickable = True   
        case "TabItem":
            clickable = True  
        case "SplitButton":
            clickable = True 
        case "ListViewItem":
            clickable = True      
        case "ListItem":   
            clickable = True 
        case "Menu":
            clickable = True        
        case "MenuItem":
            clickable = True    
        case _:
            clickable = element.is_keyboard_focusable
    # back up. todo: re-evaluate if this is necessary

                
    return clickable

def find_all_clickable_rects_parallel(window, element, filter_children=None, max_workers=8):
    # Do a shallow expansion on the main thread to avoid sending huge work units

    result = []
    # include root on main thread
    try:
        # note: checking not element.is_offscreen appears to eliminate clickable menu items..
        if is_within_window(window, element) and is_clickable(element):
            result.append(element.rect)
    except Exception:
        pass

    try:
        children = element.children
    except Exception:
        children = []

    def worker(subroot, filter_children):
        # WARNING: only safe if subroot is safe to access in worker threads
        if filter_children:
            if subroot.control_type in filter_children:
                if subroot.name in filter_children[subroot.control_type]:

                    return find_all_clickable_rects_parallel(window, subroot)
                
                #print(f"{subroot.name}: {subroot.control_type}")
                return []
        else:
            return find_all_clickable_rects_parallel(window, subroot)
        
    if len(children) > 0:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(worker, ch, filter_children) for ch in children]
            for f in as_completed(futures):
                try:
                    result.extend(f.result())
                except Exception:
                    pass

    return result

@ctx.action_class("user")
class Actions:
    def hinting_close():
        """Closes hinting canvas if open"""
        global clickables, canvas_active_window, current_button_mapping, active_window_id

        if canvas_active_window:
            clickables = None
            canvas_active_window.close()
            canvas_active_window = None
            current_button_mapping = None
            active_window_id = None
            ctx.tags = []
            return True
        
        return False
        
    def hinting_toggle():
        """Toggles hints"""
        global is_context_menu_open, clickables, canvas_active_window, current_button_mapping, active_window_id

        if actions.user.hinting_close():
            return
        
        if not is_context_menu_open:
            clickables = None
            active_window = ui.active_window()
            element = active_window.element
            focused_element = ui.focused_element()

            match ui.active_app().name:
                case "Windows Explorer":
                    cls = get_window_class(ui.active_window())

                    match cls:
                        case "CabinetWClass":
                            targets = []
                            active_tab_name = strip_more_tabs(ui.active_window().title.replace("- File Explorer", ""))
                            match_found = False
                            for child in element.children:
                                if child.name == "":
                                    targets.append(child)

                                elif child.name.strip() == active_tab_name.strip() and not match_found:
                                    targets.append(child)
                                    match_found = True

                            clickables = find_all_clickables_in_list_parallel(active_window, targets) if len(targets) > 0 else []
                case _:    
                    match focused_element.control_type:
                        case "Menu" | "MenuItem":
                            element = focused_element.parent 

                        case "Edit":
                            match active_window.cls:
                                case "Windows.UI.Core.CoreWindow":
                                    element = active_window.element.parent

            if not clickables:
                clickables = find_clickables(element)

        if clickables and len(clickables) > 0:
            canvas_active_window = canvas.Canvas.from_rect(ui.main_screen().rect)
            canvas_active_window.register("draw", draw_hints)
            canvas_active_window.freeze()

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

        actions.user.hinting_close()

is_context_menu_open = False
def on_win_open(window):
    global is_context_menu_open, clickables, active_window_id
    #print(f"win open - title = {window.title} cls = {window.cls} id = {window.id}")

    match window.cls:

        # file explorer context menu
        case "#32768":
            clickables = find_clickables(window.element)
            active_window_id = window.id
            is_context_menu_open = True

        # taskbar context menus
        case "Xaml_WindowedPopupClass":
            if window.title in ("PopupHost"):
                clickables = find_clickables(window.element)
                active_window_id = window.id
                is_context_menu_open = True

def on_win_close(window):
    global is_context_menu_open, active_window_id
    match window.cls:

        # file explorer context menu
        case "#32768":
            is_context_menu_open = False
            active_window_id = None
            actions.user.hinting_close()

        # taskbar context menus
        case "Xaml_WindowedPopupClass":
            if window.title in ("PopupHost"):
                active_window_id = None
                is_context_menu_open = False
                actions.user.hinting_close()

    if active_window_id == window.id:
        actions.user.hinting_close()

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
           actions.user.hinting_close()
    
if app.platform == "windows":
    ui.register("win_focus", on_win_focus)
    ui.register("win_open", on_win_open)
    ui.register("win_hide", on_win_hide)
    ui.register("win_close", on_win_close)
    ui.register("win_disable", on_win_disable)
    ui.register("win_title", on_win_title)