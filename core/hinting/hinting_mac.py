from typing import Dict, Optional
import math
from talon import Context, Module, actions, app, ui, canvas, settings
from talon.ui import Rect


mod = Module()
ctx = Context()

ctx = Context()
ctx.matches = r"""
os: mac
"""


class HintingState:
    def __init__(self):
        self.canvas_active_window = None
        self.active_window_id = None
        self.cached_element = None
        self.clickables = None
        self.current_button_mapping = {}
        self.is_menu_open = False


state = HintingState()

ROLES = [
    {"AXRole": "AXStaticText"},
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
    {"AXRole": "AXTextField"},
]

CLICK_ACTIONS = {"AXPress", "AXShowMenu"}

SPECIAL_WINDOW_BUNDLES = {
    "com.apple.controlcenter",
    "com.apple.Spotlight",
    "com.apple.loginwindow",
    "com.apple.notificationcenterui",
    "com.apple.coreservices.uiagent",
    "com.apple.UserNotificationCenter",
}


def set_hinting_tag(is_active: bool):
    ctx.tags = ["user.hinting_active"] if is_active else []


def close_hinting_canvas(clear_cache: bool) -> bool:
    if not state.canvas_active_window:
        return False

    state.clickables = None
    state.canvas_active_window.close()
    state.canvas_active_window = None
    state.current_button_mapping = {}
    state.active_window_id = None

    if clear_cache:
        state.cached_element = None

    set_hinting_tag(False)
    return True


def set_menu_context(element=None, active_window_id=None):
    state.cached_element = element
    state.active_window_id = active_window_id
    state.is_menu_open = element is not None


def clear_menu_context():
    state.cached_element = None
    state.active_window_id = None
    state.is_menu_open = False


def get_target_element():
    return state.cached_element or ui.active_window().element

def label_for_index(n: int) -> str:
    label = ""
    while n >= 0:
        n, remainder = divmod(n, 26)
        label = chr(remainder + ord('A')) + label
        n -= 1
    return label

def draw_hints(canvas):
    state.current_button_mapping = {}

    paint = canvas.paint
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    paint.textsize = 10

    if not state.clickables:
        return

    for index, item in enumerate(state.clickables):
        rect = item.AXFrame

        paint.style = paint.Style.FILL
        paint.color = "000000"

        rect_background = Rect(rect.x, rect.y + rect.height *.75, 25, 10)
        canvas.draw_rect(rect_background)

        x_text_position = rect_background.x + rect_background.width / 2
        y_text_position = rect_background.y + rect_background.height / 1.25

        label = label_for_index(index)
        paint.color = "ffffff"
        canvas.draw_text(label, x_text_position, y_text_position)
        state.current_button_mapping[label] = rect

    set_hinting_tag(True)

DEFAULT_ROLE_PRIORITY = {
    "AXButton": 100,
    "AXLink": 90,
    "AXMenuItem": 85,
    "AXMenuButton": 85,
    "AXCheckBox": 80,
    "AXRadioButton": 80,
    "AXToggle": 80,
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
    
    should_filter_overlaps = settings.get("user.hinting_filter_overlapping_item")
    should_filter_by_actions = settings.get("user.hinting_filter_using_actions")
    should_filter_element_at = settings.get("user.hinting_filter_using_element_at")

    if not should_filter_overlaps and not should_filter_by_actions and not should_filter_element_at:
        return items

    result = items
    if should_filter_element_at:
        result = []
        for item in items:
            try:
                el = ui.element_at(*item.AXFrame.center)
            except (AttributeError, OSError, RuntimeError):
                continue

            if el not in result:
                result.append(el)    

    if not should_filter_by_actions and not should_filter_overlaps:
        return result

    if role_priority is None:
        role_priority = DEFAULT_ROLE_PRIORITY

    def sort_key(item):
        return (
            -role_score(item.AXRole, role_priority),
            area(item.AXFrame)
        )

    if should_filter_overlaps:
        sorted_items = sorted(result, key=sort_key)
    else:
        sorted_items = result

    existing_items = []
    for item in sorted_items:
        r = item.AXFrame

        skip = False

        # double check that it's clickable. 
        # This eliminates many clickable elements in eg finder that don't have actions defined...
        
        if should_filter_by_actions:
            if not CLICK_ACTIONS.intersection(item.actions):
                continue
            
        if should_filter_overlaps:
            for index, existing_element in enumerate(existing_items):
                er = existing_element.AXFrame
                
                # Containment rule
                if contains(er, r):                    
                    skip = True

                # High IoU duplicate
                if not skip and iou(r, er) > iou_threshold:
                    skip = True

                # Nearly identical centers
                if not skip and center_distance(r, er) < center_threshold:
                    skip = True

                if skip:
                    #pressable = "AXPress" in item.actions or "AXShowMenu" in item.actions
                    #existing_pressable = "AXPress" in existing_element.actions or "AXShowMenu" in existing_element.actions
                    is_smaller = area(r) < area(er)

                    if is_smaller: #or (pressable and not existing_pressable):
                        #print("swapping to smaller item")
                        existing_items[index] = item

                    break

            if not skip:
                existing_items.append(item)

    return existing_items


def get_menu_bar_clickables() -> list:
    if state.is_menu_open:
        return []

    try:
        menu_bar = ui.element_at(0, 0)
        return menu_bar.children.find(*ROLES, visible_only=True, prefetch=["AXFrame", "AXRole"])
    except (AttributeError, OSError, RuntimeError):
        app.notify("Failed to get menubar... figure this out later")
        return []


def get_application_clickables(element) -> list:
    application_items = element.children.find(*ROLES, visible_only=True, prefetch=["AXFrame", "AXRole"])
    if settings.get("user.hinting_filter_overlapping_item"):
        return filter_elements(
            application_items,
            iou_threshold=settings.get("user.hinting_iou_threshold"),
            role_priority=DEFAULT_ROLE_PRIORITY,
        )
    return application_items

def find_clickables(element): 
    items = []
    items.extend(get_menu_bar_clickables())
    items.extend(get_application_clickables(element))

    return items


def maybe_auto_hint_menu():
    if state.is_menu_open and settings.get("user.hinting_auto_hint_menus"):
        actions.user.hinting_toggle()


def handle_special_window(window, opened: bool):
    try:
        bundle = window.app.bundle
    except AttributeError:
        return

    if bundle not in SPECIAL_WINDOW_BUNDLES:
        return

    actions.user.hinting_close(True)

    if opened:
        set_menu_context(element=window.element, active_window_id=window.id)
    else:
        clear_menu_context()
        actions.user.hinting_close(True)

    maybe_auto_hint_menu()

@ctx.action_class("user")
class Actions:
    def hinting_close(clear_cache):
        """Closes hinting canvas if open"""
        return close_hinting_canvas(clear_cache)
        
    def hinting_toggle():
        """Toggles hints"""
        if actions.user.hinting_close(False):
            return

        element = get_target_element()

        try:
            state.clickables = find_clickables(element)
        except AttributeError:
            if state.cached_element:
                app.notify("find_clickables failed with cached element. Skipping.")  
                state.cached_element = None
            else:
                app.notify("find_clickables failed with active_window. Skipping.")  

        if state.clickables and len(state.clickables) > 0:
            state.canvas_active_window = canvas.Canvas.from_rect(ui.main_screen().rect)
            state.canvas_active_window.register("draw", draw_hints)
            state.canvas_active_window.freeze()

    def hinting_select(mouse_button: int, label: str, click_count: int):
        """Click the hint based on the index"""        
        suppress_click = False
        label = label.upper()
        if label not in state.current_button_mapping:
            return

        rect = state.current_button_mapping[label]
        x_click = rect.x + rect.width / 2
        y_click = rect.y + rect.height / 2
    
        # do some special processing if the apple menu bar is already open
        if state.is_menu_open:
            x = actions.mouse_x()
            y = actions.mouse_y()

            # this logic attempts to allow the user to "switch" menu bar items
            # without repeated voice commands. e.g. file to edit
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

# we need special processing for certain windows...
def process_problem_children(window, opened):
    handle_special_window(window, opened)

def on_win_open(window):
    print(f"on_win_open {window.app.bundle}")
    process_problem_children(window, True)

    #print(f"win open - title = {window.title} cls = {window.cls} id = {window.id}")

def on_win_close(window):
    try:
        print(f"on_win_close {window.app.bundle}")
    except AttributeError:
        print("on_win_close")

    process_problem_children(window, False)

    if state.canvas_active_window:
        actions.user.hinting_close(False)

def on_win_hide(window):
    print(f"on_win_hide {window.app.bundle}")

    on_win_close(window)

def on_win_disable(window):
    print(f"on_win_disable {window.app.bundle}")
    on_win_close(window)

def on_win_title(window):
    print(f"on_win_title {window.app.bundle}")

    if window.id != state.active_window_id:
        return
    else:
        on_win_close(window)

def on_win_focus(window):
    print(f"on_win_focus {window.app.bundle}")

    if state.canvas_active_window:
        if state.active_window_id != window.id:
           actions.user.hinting_close(False)

    # we need special processigng for control center & a few others...
    process_problem_children(window, True)

def on_menu_open(element):
    print(f"on_menu_opened {element}")

    actions.user.hinting_close(True)

    set_menu_context(element=element)
    maybe_auto_hint_menu()

def on_menu_close(element):
    print("on_menu_close")
    clear_menu_context()

    on_win_close(element)

    if state.canvas_active_window:
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
