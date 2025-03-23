from talon.windows.ax import Element
from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings
from dataclasses import dataclass, asdict
from talon.ui import Rect
import math
import platform
@dataclass
class Position:
    x: int
    y: int

ctx = Context()
ctx.matches = r"""
os: mac
"""

@ctx.action_class("user")
class Actions:
    def switcher_click(mouse_button: int, index: int):
        """"""
        dock_items = ui.apps(bundle="com.apple.dock")[0].children
        if index > len(dock_items[0].children):
            return

        item_frame = dock_items[0].children[index]
        if mouse_button == 0:
            item_frame.perform("AXPress")
        else:
            item_frame.perform("AXShowMenu")
        # x, y = ctrl.mouse_pos()
        # actions.mouse_move(item_frame.x + item_frame.width / 2 , item_frame.y + item_frame.height / 2)
        # actions.mouse_click(mouse_button)
        # actions.sleep("150ms")
        # actions.mouse_move(x, y)

count = None
mcanvas = canvas.Canvas.from_screen(ui.main_screen())
def draw_options(canvas):
    global count
    paint = canvas.paint
    #for b in cache:
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    paint.textsize = 12
    index = 0
    
    dock_items = ui.apps(bundle="com.apple.dock")[0].children
    for child in dock_items[0].children:
        index += 1



        paint.style = paint.Style.FILL
        #paint.color = "ffffff"
        rect = child.AXFrame
        frame_rect = Rect(math.floor(rect.x), rect.y + rect.height / 4, rect.width / 3, rect.height )
        #canvas.draw_rect(frame_rect)
        paint.color = "ffffff"
        if child.AXSubrole == "AXSeparatorDockItem":
            continue 
        canvas.draw_text(f"{index}", rect.x, frame_rect.y + rect.height / 2 )
        #if index == 38:
        #    print(child)


    count = len(dock_items[0].children)

if app.platform == "mac":
    # uncomment the following for quick testing
    def on_ready():
        mcanvas.register("draw", draw_options)

        # for child in dock_items[0].children:
        #     rect = child.AXFrame
        #     print(rect.width)
        
    app.register("ready", on_ready)