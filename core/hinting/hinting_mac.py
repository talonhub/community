from talon import Context, Module, actions, app, ui, canvas, registry
from talon.ui import Rect

mod = Module()
mod.tag("hinting_active", desc="Indicates hints are active")
ctx = Context()

canvas_active_window = None
active_window_id = None
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

import re
def strip_more_tabs(title: str) -> str:
    return re.sub(r"\s+and\s+\d+\s+more\s+tab.*", "", title)

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
         {"AXRole": "AXTextField"}]
         #{"AXRole": "AXTextField"}]


def find_clickables(element): 
    items = []
    menu_bar_items = None
    if not is_menu_open:   
        menu_bar = ui.element_at(0, 0)
        menu_bar_items = menu_bar.children.find(*roles, visible_only=True)
        items.extend(menu_bar_items)

    application_items = element.children.find(*roles, visible_only=True)
    items.extend(application_items)

    return items

@ctx.action_class("user")
class Actions:
    def hinting_close():
        """Closes hinting canvas if open"""
        global clickables, canvas_active_window, current_button_mapping, active_window_id

        if canvas_active_window:
            if not is_menu_open:
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
            print("closed hints")
            return
        
        if not is_menu_open:
            print("menu not opened....")
            clickables = None

            try:
                focused_element = ui.focused_element()
                print(f"focused element {focused_element.AXRole}")
            except:
                print("failed to get focused element...")
                focused_element = None

            element = ui.active_window().element

            # if focused_element and focused_element.AXRole in  ("AXMenu", "AXMenuItem", "AXMenuBarItem"):
            #     element = focused_element
            
            try:
                clickables = find_clickables(element)
            except AttributeError:
                app.notify("find_clickables failed: attribute error")            

        if clickables and len(clickables) > 0:
            canvas_active_window = canvas.Canvas.from_rect(ui.main_screen().rect)
            canvas_active_window.register("draw", draw_hints)
            canvas_active_window.freeze()

    def hinting_select(mouse_button: int, label: str, click_count: int):
        """Click the hint based on the index"""        
        global force_hinting

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
            actions.user.hinting_close()

    def dump_element_at_mouse():
        """"""
        #print(f"{actions.mouse_x()},{actions.mouse_y()}")
        el = ui.element_at(actions.mouse_x(), actions.mouse_y())
        print(el.dump())

is_menu_open = False
def on_win_open(window):
    global is_menu_open, clickables, active_window_id
    print(f"on_win_open {window.app.bundle}")

    try:
        match window.app.bundle:
            case "com.apple.Spotlight":
                is_menu_open = True
                clickables = find_clickables(window.element)
                actions.user.hinting_close()
                actions.user.hinting_toggle()
    except:
        pass
    #print(f"win open - title = {window.title} cls = {window.cls} id = {window.id}")

def on_win_close(window):
    global is_menu_open, active_window_id, clickables
    try:
        print(f"on_win_close {window.app.bundle}")
    except:
        print(f"on_win_close")

    # we need special processig for control center...
    try:
        match window.app.bundle:
            case "com.apple.controlcenter" | "com.apple.Spotlight":
                is_menu_open = False
                clickables = None
                active_window_id = None
                actions.user.hinting_toggle()
    except:
        pass

    if canvas_active_window:
        actions.user.hinting_close()

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

    global is_menu_open, clickables, active_window_id

    if canvas_active_window:
        if active_window_id != window.id:
           actions.user.hinting_close()

    # we need special processigng for control center & a few others...
    try:
        match window.app.bundle:
            case "com.apple.controlcenter" | "com.apple.Spotlight":
                active_window_id = window.id
                is_menu_open = True
                clickables = find_clickables(window.element)
                actions.user.hinting_close()
                actions.user.hinting_toggle()
    except:
        pass    

is_menu_open = False
def on_menu_open(element):
    global is_menu_open, clickables, active_window_id
    clickables = find_clickables(element)
    print(f"on_menu_opened {element.AXRole} {clickables}")

    active_window_id = None
    is_menu_open = True

    actions.user.hinting_close()
    actions.user.hinting_toggle()

def on_menu_close(window):
    print("on_menu_close")
    global is_menu_open, active_window_id, clickables
    clickables = None
    on_win_close(window)
    clickables = None
    is_menu_open = False

    if canvas_active_window:
        actions.user.hinting_close()

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
