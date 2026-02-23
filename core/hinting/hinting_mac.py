from typing import List, Optional, Dict
import math
from talon import Context, Module, actions, app, ui, canvas, settings
from talon.ui import Rect


mod = Module()
ctx = Context()

canvas_active_window = None
active_window_id = None
cached_element = None
clickables = None
force_hinting = False

ctx = Context()
ctx.matches = r"""
os: mac
"""

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

        try:
            label = label_for_index(index - 1)
            paint.color = "ffffff"
            canvas.draw_text(f"{label}", x_text_position, y_text_position)
            index = index + 1
            current_button_mapping[label] = rect
        except:
            print(f"Failed to generate label for index {index}")
            break

    ctx.tags = ['user.hinting_active']

roles = [{"AXRole": "AXStaticText"}, 
         {"AXRole": "AXButton"},
         {"AXRole": "AXRadioButton"}, 
         {"AXRole": "AXMenuButton"}, 
         {"AXRole": "AXRow"}, 
         {"AXRole": "AXCell"}, 
         {"AXRole": "AXPopUpButton"},
         {"AXRole": "AXToggle"},
         {"AXRole": "AXCheckBox"},
         {"AXRole": "AXDisclosureTriangle"},
         {"AXRole": "AXUrl"},
         {"AXRole": "AXGroup"},
         {"AXRole": "AXMenuBarItem"},
         {"AXRole": "AXMenuItem"},
         {"AXRole": "AXMenu"},
         {"AXRole": "AXColorWell"},
         {"AXRole": "AXTextField"}]

         #{"AXRole": "AXTextField"}]

DEFAULT_ROLE_PRIORITY = {
    "AXButton": 100,
    "AXLink": 90,
    "AXMenuItem": 85,
    "AXCheckBox": 80,
    "AXRadioButton": 80,
    "AXTextField": 75,
    "AXPopUpButton": 75,
    "AXGroup": 20,
    "AXScrollArea": 10,
    "AXWindow": 0,
}

def rect_edges(rect):
    return (rect.x, rect.y, rect.x + rect.width, rect.y + rect.height)

def area(rect) -> float:
    return max(0.0, rect.width) * max(0.0, rect.height)


def intersection_area(a, b) -> float:
    ax1, ay1, ax2, ay2 = rect_edges(a)
    bx1, by1, bx2, by2 = rect_edges(b)

    x1 = max(ax1, bx1)
    y1 = max(ay1, by1)
    x2 = min(ax2, bx2)
    y2 = min(ay2, by2)

    if x2 <= x1 or y2 <= y1:
        return 0.0

    return (x2 - x1) * (y2 - y1)


def iou(a, b) -> float:
    inter = intersection_area(a, b)
    if inter == 0:
        return 0.0
    return inter / (area(a) + area(b) - inter)


def contains(a, b) -> bool:
    ax1, ay1, ax2, ay2 = rect_edges(a)
    bx1, by1, bx2, by2 = rect_edges(b)

    return ax1 <= bx1 and ay1 <= by1 and ax2 >= bx2 and ay2 >= by2

def center(rect):
    return (rect.x + rect.width / 2.0, rect.y + rect.height / 2.0)


def center_distance(a, b) -> float:
    ax, ay = center(a)
    bx, by = center(b)
    return math.hypot(ax - bx, ay - by)

def role_score(role: Optional[str],
               role_priority: Dict[str, int]) -> int:
    if role is None:
        return 50
    return role_priority.get(role, 50)

def filter_elements(
    items: list,
    iou_threshold: float = 0.85,
    center_threshold: float = 4.0,
    role_priority: Optional[Dict[str, int]] = None,
) -> list:
    """
    items: list of dicts:
        {
            "rect": (x, y, w, h),
            "role": "AXButton"  # optional
        }

    Returns filtered list.
    """

    if role_priority is None:
        role_priority = DEFAULT_ROLE_PRIORITY

    def sort_key(item):
        return (
            -role_score(item.AXRole, role_priority),
            area(item.AXFrame)
        )

    sorted_items = sorted(items, key=sort_key)

    result = []

    for item in sorted_items:
        r = item.AXFrame

        skip = False

        # double check that it's clickable. 
        # This eliminates many clickable elements in eg finder that don't have actions defined...
        # if "AXPress" not in item.actions and "AXShowMenu" not in item.actions:
        #     #print("FITLERED NON-CLICKABLE ELEMENT")
        #     continue

        for existing in result:
            er = existing.AXFrame

            # Containment rule
            if contains(er, r):
                skip = True
                break

            # High IoU duplicate
            if iou(r, er) > iou_threshold:
                skip = True
                break

            # Nearly identical centers
            if center_distance(r, er) < center_threshold:
                skip = True
                break

        if not skip:
            result.append(item)

    return result

def find_clickables(element): 
    items = []
    menu_bar_items = None
    if not is_menu_open:   
        menu_bar = ui.element_at(0, 0)
        menu_bar_items = menu_bar.children.find(*roles, visible_only=True,prefetch=["AXFrame", "AXRole"])
        items.extend(menu_bar_items)

    if settings.get("user.hinting_filter_items"):
        application_items = filter_elements(element.children.find(*roles, visible_only=True,prefetch=["AXFrame", "AXRole"]), iou_threshold=0.00,role_priority=DEFAULT_ROLE_PRIORITY)
    else:
        application_items = element.children.find(*roles, visible_only=True,prefetch=["AXFrame", "AXRole"])
    items.extend(application_items)

    return items

@ctx.action_class("user")
class Actions:
    def hinting_close(clear_cache):
        """Closes hinting canvas if open"""
        global clickables, canvas_active_window, current_button_mapping, active_window_id, cached_element

        if canvas_active_window:
            clickables = None
            canvas_active_window.close()
            canvas_active_window = None
            current_button_mapping = None
            active_window_id = None

            if clear_cache:
                cached_element = None

            ctx.tags = []
            return True
        
        return False
        
    def hinting_toggle():
        """Toggles hints"""
        global is_menu_open, clickables, canvas_active_window, current_button_mapping, active_window_id
        

        # print("hinting toggle!!!")
        if actions.user.hinting_close(False):
            #print("closed hints")
            return
        
        # if cached_element:
        #     print("cached!!")

        element = ui.active_window().element if not cached_element else cached_element
            
        try:
            clickables = find_clickables(element)
        except AttributeError:
            app.notify("find_clickables failed: attribute error. Skipping.")            

        #walk(element)
        
        if clickables and len(clickables) > 0:
            canvas_active_window = canvas.Canvas.from_rect(ui.main_screen().rect)
            canvas_active_window.register("draw", draw_hints)
            canvas_active_window.freeze()

    def hinting_select(mouse_button: int, label: str, click_count: int):
        """Click the hint based on the index"""        
        suppress_click = False
        label = label.upper()
        if label not in current_button_mapping:
            return

        rect = current_button_mapping[label]
        x_click = rect.x + rect.width / 2
        y_click = rect.y + rect.height / 2
    
        # do some special processing if the apple menu bar is already open
        if is_menu_open:
            x = actions.mouse_x()
            y = actions.mouse_y()

            # this logic attempts to allow the user to "switch" menu bar items
            # without repeated voice commands. e.g. file to 
            menu_bar = ui.element_at(0, 0)
            is_clicking_menu_bar = menu_bar.AXFrame.contains(x_click, y_click)
            if is_clicking_menu_bar:
                if menu_bar.AXFrame.contains(x,y):
                    suppress_click = ui.element_at(x_click, y_click).AXRole == "AXMenuBarItem"
                # elif is_menu_open:
                #     print("context menu open, forcing multiple clicks")
                #     forcing_multiple_clicks = True
                #     click_count = 2

        actions.mouse_move(x_click, y_click)

        if not suppress_click:
            if click_count > 0:
                for i in range(0, click_count):
                    actions.mouse_click(mouse_button)

        if not ui.element_at(x_click, y_click).AXRole == "AXMenuBarItem":
            actions.user.hinting_close(True)

is_menu_open = False

# we need special processing for certain windows...
def process_problem_children(window, opened):
    global is_menu_open, active_window_id, cached_element

    try:
        match window.app.bundle:
            case "com.apple.controlcenter" | "com.apple.Spotlight" | "com.apple.loginwindow" | "com.apple.notificationcenterui" | "com.apple.coreservices.uiagent" | "com.apple.UserNotificationCenter":
                actions.user.hinting_close(True)

                if opened:
                    active_window_id = window.id
                    cached_element = window.element
                    is_menu_open = True

                else:
                    is_menu_open = False
                    cached_element = None
                    active_window_id = None
                    actions.user.hinting_close(True) 

                if is_menu_open and settings.get("user.hinting_auto_hint_menus"):
                    actions.user.hinting_toggle()
    except:
        pass

def on_win_open(window):
    print(f"on_win_open {window.app.bundle}")
    process_problem_children(window, True)

    #print(f"win open - title = {window.title} cls = {window.cls} id = {window.id}")

def on_win_close(window):
    global is_menu_open, active_window_id, clickables, cached_element
    try:
        print(f"on_win_close {window.app.bundle}")
    except:
        print(f"on_win_close")

    process_problem_children(window, False)

    if canvas_active_window:
        actions.user.hinting_close(False)

def on_win_hide(window):
    print(f"on_win_hide {window.app.bundle}")

    on_win_close(window)

def on_win_disable(window):
    print(f"on_win_disable {window.app.bundle}")
    on_win_close(window)

def on_win_title(window):
    print(f"on_win_title {window.app.bundle}")

    if window.id != active_window_id:
        return
    else:
        on_win_close(window)

def on_win_focus(window):
    print(f"on_win_focus {window.app.bundle}")

    global is_menu_open, clickables, active_window_id, cached_element    
    if canvas_active_window:
        if active_window_id != window.id:
           actions.user.hinting_close(False)

    # we need special processigng for control center & a few others...
    process_problem_children(window, True)

is_menu_open = False
def on_menu_open(element):
    global is_menu_open, clickables, active_window_id, cached_element
    print(f"on_menu_opened {element}")

    actions.user.hinting_close(True)

    active_window_id = None
    cached_element = element

    active_window_id = None
    is_menu_open = True

    if settings.get("user.hinting_auto_hint_menus"):
        actions.user.hinting_toggle()

def on_menu_close(element):
    print("on_menu_close")
    global is_menu_open, active_window_id, clickables, cached_element
    active_window_id = None
    is_menu_open = False
    cached_element = None

    on_win_close(element)

    if canvas_active_window:
        actions.user.hinting_close(True)

def on_element_focus(element):
    pass
    #print(f"on_element_focus: {element.AXRole}")

if app.platform == "mac":
    ui.register("win_focus", on_win_focus)
    ui.register("win_open", on_win_open)
    ui.register("win_hide", on_win_hide)
    ui.register("win_close", on_win_close)
    ui.register("win_disable", on_win_disable)
    ui.register("win_title", on_win_title)
    ui.register("menu_open", on_menu_open)
    ui.register("menu_close", on_menu_close)
    ui.register("element_focus", on_element_focus)

    #ui.register("", print)

def walk(element, depth=0):
    desc = ""
    try:
        desc = element.AXDescription
    except:
        desc = ""

    try:
        print("  " * depth + f"{element.AXRole}") 
    except:
        pass

    try:
        for child in element.children:
            walk(child, depth + 1)
    except (OSError, RuntimeError, AttributeError):
        pass  # Element became stale
