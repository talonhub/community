from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
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
os: mac
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
    paint.textsize = 10

    if not clickables:
        return
    
    index = 1

    for item in clickables:
        rect = item.AXFrame
        paint.style = paint.Style.FILL
        paint.color = "000000"

        rect_background = Rect(rect.x, rect.y + rect.height *.75, 25, 10)
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
        global is_menu_open, clickables, canvas_active_window, current_button_mapping, active_window_id
        

        # print("hinting toggle!!!")
        if actions.user.hinting_close():
            return
        
        active_window = ui.active_window()
        element = active_window.element
        if not is_menu_open:
            clickables = find_all_clickable_elements_parallel(active_window, element)

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

is_menu_open = False
def on_win_open(window):
    global is_menu_open, clickables, active_window_id
    #print(f"win open - title = {window.title} cls = {window.cls} id = {window.id}")

def on_win_close(window):
    global is_menu_open, active_window_id

    if canvas_active_window:
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

def on_win_focus(window):
    window = ui.active_window()

    if canvas_active_window:
        if active_window_id != window.id:
           actions.user.hinting_close()

is_menu_open = False
def on_menu_open(element):
    global is_menu_open, clickables, active_window_id
    #print(f"win open - title = {window.title} cls = {window.cls} id = {window.id}")  
    clickables = find_all_clickable_elements(None, element)
    active_window_id = None
    is_menu_open = True


def on_menu_close(window):
    global is_menu_open, active_window_id, clickables
    on_win_close(window)
    clickables = None
    is_menu_open = False

    if canvas_active_window:
        actions.user.hinting_close()


if app.platform == "mac":
    ui.register("win_focus", on_win_focus)
    ui.register("win_open", on_win_open)
    ui.register("win_hide", on_win_hide)
    ui.register("win_close", on_win_close)
    ui.register("win_disable", on_win_disable)
    ui.register("win_title", on_win_title)
    ui.register("menu_open", on_menu_open)
    ui.register("menu_close", on_menu_close)

    #ui.register("", print)

def walk(element, depth=0):
    print("  " * depth + f"{element.AXRole}, {element.actions}") 

    try:
        if app.platform == "windows":
            for child in element.children:
                walk(child, depth + 1)
        else:
            try:
                if element.children and len(element.children) > 0:
                    for child in element.children:
                        walk(child, depth + 1)
            except:
                pass
    except (OSError, RuntimeError):
        pass  # Element became stale


def is_within_window(window, element):
    try:
        frame = element.AXFrame
    except:
        frame = None

    if window and frame and window.rect.contains(frame.x, frame.y) or not window:
        return True
    
    return False


def is_clickable(element, depth=0):
    clickable = False

    try:
        actions = element.actions
    except:
        return clickable

    clickable = element.AXRole in ("AXCell", "AXButton", "AXGroup", "AXRole")

    # if not clickable:
    #     clickable = "AXEnabled" in element.attrs and ("AXPress" in actions or 
    #         "AXShowMenu" in actions or 
    #         "AXConfirm" in actions or 
    #         "AXOpen" in actions or
    #         "AXCell" in actions or
    #         "AXCheckBox" in actions)
    
    
    #print(f"{element.AXRole}")
    # back up. todo: re-evaluate if this is necessary

    return clickable

def find_all_clickable_elements(window, element, depth=0) -> list:
    result = []
    
    is_element_clickable = is_within_window(window, element) and (is_clickable(element))
    if is_element_clickable:
        result.append(element)

    # if the element is disabled, can we safely skip?
    children = None
    try:
        children = element.AXChildren
    except:
        children = None

        #print(f"all clickable exception {e} {name}")
        return result 

    if children:
        for child in children:
            child_result = find_all_clickable_elements(window, child, depth + 1)
            result.extend(child_result)


    return result

def find_all_clickable_elements_parallel(window, element, max_workers=8):
    # Do a shallow expansion on the main thread to avoid sending huge work units

    result = []
    # include root on main thread
    try:
        # note: checking not element.is_offscreen appears to eliminate clickable menu items..
        is_element_clickable = is_within_window(window, element) and (is_clickable(element))
        if is_element_clickable:
            result.append(element)
    except Exception:
        pass

    try:
        children = element.AXChildren
    except Exception:
        children = None

    def worker(subroot):
        # WARNING: only safe if subroot is safe to access in worker threads
        return find_all_clickable_elements_parallel(window, subroot, max_workers=8)

    if children and len(children) > 0:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(worker, ch) for ch in children]
            for f in as_completed(futures):
                try:
                    result.extend(f.result())
                except Exception:
                    pass

    return result