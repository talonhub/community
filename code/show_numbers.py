import time
from talon import Module, Context, canvas, ui, actions

mod = Module()


@mod.action_class
class Actions:
    def numbers_pick(n: int):
        """Pick from the displayed numbers"""
        if not interactor.showing:
            raise Exception("Numbers are not visible")
        interactor.pick(n)

    def numbers_cancel():
        """Cancel the number overlay"""
        if not interactor.showing:
            raise Exception("Numbers are not visible")
        interactor.cancel()

    def numbers_show():
        """Show speakable numbers over clickable UI elements"""
        if interactor.showing:
            interactor.cancel()
        interactor.show()


class Interactor:
    def __init__(self):
        self.mapping = {}
        self.buttons = []
        self.showing = False
        self.win = None
        self.canvas = None

    def show(self):
        self.showing = True
        win = self.win = ui.active_window()
        wrect = win.rect

        elements = win.children.find({"AXRole": "AXButton"}, {"AXRole": "AXLink"})
        buttons = []
        mapping = {}
        for i, button in enumerate(elements):
            if button.AXTitle.strip() and "AXPress" in button.actions:
                title = button.AXTitle.replace("\n", " ")
                pos = button.AXFrame["$rect2d"]
                rect = ui.Rect(
                    pos["x"] - wrect.x, pos["y"] - wrect.y, pos["width"], pos["height"]
                )
                mapping[title] = (button, title, rect)
                buttons.append((button, title, rect))
        self.buttons = buttons
        self.mapping = mapping

        self.canvas = canvas.Canvas.from_rect(win.rect, paused=True)
        self.canvas.register("draw", self.draw)
        self.canvas.freeze()

    def cancel(self):
        self.canvas.close()
        self.canvas = None
        self.win = None
        self.showing = False
        self.buttons = []
        self.mapping = {}

    def pick(self, n):
        if n >= 0 and n < len(self.buttons):
            button = self.buttons[n][0]
            button.perform("AXPress")
        self.cancel()

    def draw(self, canvas):
        paint = canvas.paint
        wrect = self.win.rect
        pad = 2
        for i, (button, title, rect) in enumerate(self.buttons):
            rect = ui.Rect(rect.x + wrect.x, rect.y + wrect.y, rect.width, rect.height)
            _, trect = paint.measure_text(str(i))
            target = ui.Rect(
                rect.left - trect.width / 2 - pad,
                rect.top - trect.height / 2 - pad,
                trect.width + pad * 2,
                trect.height + pad * 2,
            )
            paint.style = paint.Style.FILL
            paint.color = "white"
            canvas.draw_rect(target)
            paint.color = "black"
            paint.stroke_width = 1
            paint.style = paint.Style.STROKE
            canvas.draw_rect(target)
            paint.style = paint.Style.FILL
            canvas.draw_text(str(i), target.x + pad, target.y + trect.height + pad / 2)


interactor = Interactor()
