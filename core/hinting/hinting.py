from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
from talon.ui import Rect
from ..operating_system.windows.accessibility import find_all_clickable_rects, get_window_class, find_all_clickables_in_list_parallel

mod = Module()
mod.tag("hinting_active", desc="Indicates hints are active")
mod.setting(
    "auto_hint_menus",
    type=bool,
    default=True,
    desc="Enables experimental auto-hinting of menus",
)

ctx = Context()

canvas_active_window = None
active_window_id = None
clickables = None

@mod.capture(rule="<user.letter> (twice | second)")
def hinting_double(m) -> str:
    return m.letter + m.letter

@mod.capture(rule="<user.letter> | <user.letter> <user.letter> | <user.letter> <user.letter> <user.letter> | <user.hinting_double> ")
def hinting(m) -> str:
    return "".join(m)

@ctx.action_class("main")
class MainActions:
    def mouse_click(button: int = 0):
        actions.user.hinting_close(True)
        actions.next(button)

    def mouse_scroll(y: float = 0, x: float = 0, by_lines: bool = False):
        actions.user.hinting_close(True)
        actions.next(y, x, by_lines)

def label_for_index(n: int) -> str:
    A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < 26:
        return A[n]

    m = n - 26
    return A[m // 26] + A[m % 26]

@mod.action_class
class Actions:
    def hinting_close(clear_cache: True):
        """Closes hinting canvas if open"""
        return False
        
    def hinting_toggle():
        """Toggles hints"""
        pass

    def hinting_select(mouse_button: int, label: str, click_count: int):
        """Click the hint based on the index"""        
        pass

    def dump_element_at_mouse():
        """"""
        print(f"{actions.mouse_x()},{actions.mouse_y()}")
        el = ui.element_at(actions.mouse_x(), actions.mouse_y())
        print(el.parent)
        #help(el)

        #print(f"{el.AXRole} {el.AXDescription}") 

        #walk(el)

def walk(element, depth=0):
    desc = ""
    try:
        desc = element.AXDescription
    except:
        desc = ""

    print("  " * depth + f"{element.AXRole}") 
    
    try:
        for child in element.children:
            walk(child, depth + 1)
    except (OSError, RuntimeError):
        pass  # Element became stale

