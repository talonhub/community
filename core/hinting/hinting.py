from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
from talon.ui import Rect
from ..operating_system.windows.accessibility import walk, find_all_clickable_elements, find_all_clickable_elements_parallel, find_all_clickable_rects, find_all_clickable_rects_parallel, process_children_in_parallel

mod = Module()
mod.tag("hinting_active", desc="Indicates hints are active")
ctx = Context()

canvas_active_window = None
active_window_id = None
clickables = None

@mod.capture(rule="<user.letter> (twice | second)")
def hinting_double(m) -> str:
    return m.letter + m.letter

@mod.capture(rule="<user.letter> | <user.letter> <user.letter> | <user.hinting_double>")
def hinting(m) -> str:
    return "".join(m)

@ctx.action_class("main")
class MainActions:
    def mouse_click(button: int = 0):
        actions.user.hinting_close()
        actions.next(button)

    def mouse_scroll(y: float = 0, x: float = 0, by_lines: bool = False):
        actions.user.hinting_close()
        actions.next(y, x, by_lines)

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
        canvas.close()
        return
    
    index = 1

    for rect in clickables:
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

        label = label_for_index(index - 1)

        paint.color = "ffffff"
        canvas.draw_text(f"{label}", x_text_position, y_text_position)
        index = index + 1
        current_button_mapping[label] = rect

    ctx.tags = ['user.hinting_active']

@mod.action_class
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
        global clickables, canvas_active_window, current_button_mapping, active_window_id

        if actions.user.hinting_close():
            return
        
        active_window = ui.active_window() 
        
        focused_element = ui.focused_element()
        parent_element = focused_element.parent
        active_window_id = active_window.id

        match focused_element.control_type:
            case "Menu" | "MenuItem":

                element = focused_element.parent 
                clickables = find_all_clickable_rects_parallel(element)

            case "Edit":
                match active_window.cls:
                    case "Windows.UI.Core.CoreWindow":
                        if parent_element.name == "Search":
                            clickables = find_all_clickable_rects_parallel(active_window.element.parent)
                        else:
                            clickables = find_all_clickable_rects_parallel(active_window.element)
                    case _:
                        clickables = find_all_clickable_rects_parallel(active_window.element)
            case _:
                #print(f"{focused_element.control_type} {active_window.cls} {active_window.title}")
                clickables = find_all_clickable_rects_parallel(active_window.element)

        canvas_active_window = canvas.Canvas.from_rect(active_window.rect)
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

def on_win_focus(_):
    window = ui.active_window()

    if canvas_active_window:
        if active_window_id != window.id:
           actions.user.hinting_close()
    
ui.register("win_focus", on_win_focus)