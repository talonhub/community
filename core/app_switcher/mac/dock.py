from talon.windows.ax import Element
from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
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
    def taskbar_click(mouse_button: int, index: int):
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

mcanvas = canvas.Canvas.from_screen(ui.main_screen())
cached_count = 0
def draw_options(canvas):
    global cached_count
    paint = canvas.paint
    #for b in cache:
    canvas.paint.text_align = canvas.paint.TextAlign.CENTER
    paint.textsize = 12
    index = 0
    
    dock_items = ui.apps(bundle="com.apple.dock")[0].children
    for child in dock_items[0].children:
        index += 1

        if child.AXSubrole == "AXSeparatorDockItem":
            continue

        paint.style = paint.Style.FILL
        #paint.color = "ffffff"
        rect = child.AXFrame
        frame_rect = Rect(math.floor(rect.x), rect.y + rect.height / 4, rect.width / 3, rect.height )
        #canvas.draw_rect(frame_rect)
        paint.color = "ffffff"
        canvas.draw_text(f"{index}", rect.x, frame_rect.y + rect.height / 2 )
        #if index == 38:
        #    print(child)


    cached_count = len(dock_items[0].children)

def update():
    if len(ui.apps(bundle="com.apple.dock")[0].children) != cached_count:
        mcanvas.freeze()
        
        
if app.platform == "mac":
    # uncomment the following for quick testing
    def on_ready():
        mcanvas.register("draw", draw_options)
        mcanvas.freeze()
        ui.register("app_launch", lambda _: update())
        ui.register("app_close", lambda _: update())
        ui.register("screen_change", lambda _: update())
        # for child in dock_items[0].children:
        #     rect = child.AXFrame
        #     print(rect.width)
        
    app.register("ready", on_ready)