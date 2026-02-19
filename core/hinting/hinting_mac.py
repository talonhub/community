from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
from talon.ui import Rect

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

    for axframe in clickables:
        rect = axframe
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

roles = [{"AXRole": "AXStaticText"}, 
         {"AXRole": "AXButton"}, 
         {"AXRole": "AXRadioButton"}, 
         {"AXRole": "AXMenuButton"}, 
         {"AXRole": "AXCell"}, 
         {"AXRole": "AXPopUpButton"},
         {"AXRole": "AXToggle"},
         {"AXRole": "AXCheckBox"},
         {"AXRole": "AXDisclosureTriangle"},
         {"AXRole": "AXMenuItem"}]

def find_clickables(element):    
    items = element.children.find(*roles, visible_only=True)
    clickables = [item.AXFrame for item in items]
    return clickables

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
        
        if not is_menu_open:
            clickables = None
            active_window = ui.active_window()
            clickables = find_clickables(active_window.element)

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
    clickables = find_clickables(element)
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
