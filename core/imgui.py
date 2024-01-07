from talon import Module, skia, ui, settings
from talon.skia.image import Image as SkiaImage
from talon.skia.imagefilter import ImageFilter as ImageFilter
from talon.canvas import Canvas, MouseEvent
from talon.screen import Screen
from talon.types import Rect
from typing import Callable, Optional
from dataclasses import dataclass

FONT_FAMILY = "Segoe UI Symbol"
FONT_SIZE = 14
background_color = "ffffff"
border_color = "000000"
text_color = "444444"
button_bg_color = "aaaaaa"
button_text_color = "000000"
border_radius = 8
button_radius = 4

mod = Module()

setting_max_rows = mod.setting(
    "gui_max_rows",
    type=int,
    default=5,
)
setting_max_col = mod.setting(
    "gui_max_cols",
    type=int,
    default=50,
)


class State:
    def __init__(self, canvas: skia.Canvas, font_size: float, numbered: bool):
        self.max_rows = settings.get("user.gui_max_rows")
        self.max_cols = settings.get("user.gui_max_cols")
        self.canvas = canvas
        self.font_size = font_size
        self.padding = self.rem(0.5)
        self.image_height = self.max_rows * self.font_size
        self.image_width = 5 * self.image_height
        self.text_offset = self.rem(2.5) if numbered else self.padding
        self.x = canvas.x + self.padding
        self.x_text = canvas.x + self.text_offset
        self.y = canvas.y + self.padding
        self.width = 0
        self.height = self.padding

    def add_width(self, width: float, offset: bool):
        text_offset = self.text_offset if offset else self.padding
        self.width = max(self.width, text_offset + width)

    def add_height(self, height: float):
        self.y += height
        self.height += height

    def get_width(self):
        if self.width:
            return round(self.width + self.padding)
        else:
            return 0

    def get_height(self):
        return round(self.height + self.padding)

    def rem(self, number: int or float):
        return round(self.font_size * number)


class Text:
    def __init__(self, text: str, header: bool):
        self.numbered = not header
        self.text = text
        self.header = header
        self.rect = None
        self._is_clicked = False

    def is_clicked(self):
        is_clicked = self._is_clicked
        self._is_clicked = False
        return is_clicked

    def click(self):
        self._is_clicked = True

    def draw(self, state: State):
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = self.header
        state.canvas.paint.textsize = state.font_size
        state.canvas.paint.color = text_color
        x = state.x if self.header else state.x_text
        start_x = state.x
        start_y = state.y
        width = 0
        height = 0

        lines = self.text.split("\n")
        if len(lines) > state.max_rows:
            lines = lines[: state.max_rows]
            lines[-1] = "..."

        for line in lines:
            line = line.replace("\t", "    ")
            if len(line) > state.max_cols + 4:
                line = line[: state.max_cols] + " ..."
            rect = state.canvas.paint.measure_text(line)[1]
            state.canvas.draw_text(line, x, state.y + state.font_size)
            state.add_width(rect.x + rect.width, offset=not self.header)
            state.add_height(state.font_size)
            width = max(width, rect.x + rect.width)
            height += state.font_size

        self.rect = Rect(
            start_x,
            start_y,
            width + x - start_x,
            height + state.padding / 2,
        )
        # state.canvas.draw_rect(self.rect) TODO remove

        state.add_height(state.padding)

    @classmethod
    def draw_number(cls, state: State, y_start: float, number: int):
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = False
        state.canvas.paint.textsize = state.font_size
        state.canvas.paint.color = button_text_color
        text = str(number).rjust(2)
        rect = state.canvas.paint.measure_text(text)[1]
        x = state.x + rect.x
        y = (state.y + y_start + rect.y + state.font_size) / 2

        # state.canvas.paint.style = state.canvas.paint.Style.FILL
        # state.canvas.paint.color = button_bg_color
        # state.canvas.draw_rect(Rect(x, y_start, rect.x + rect.width, state.y - y_start))
        # state.canvas.paint.color = button_text_color

        state.canvas.draw_text(text, x, y)


class Button:
    def __init__(self, text: str):
        self.numbered = False
        self.text = text
        self.rect = None
        self._is_clicked = False

    def is_clicked(self):
        is_clicked = self._is_clicked
        self._is_clicked = False
        return is_clicked

    def click(self):
        self._is_clicked = True

    def draw(self, state: State):
        state.canvas.paint.textsize = state.font_size
        text_rect = state.canvas.paint.measure_text(self.text)[1]
        padding = state.rem(0.25)
        width = text_rect.width + 2 * padding
        height = state.font_size + 2 * padding

        self.rect = Rect(
            state.x + text_rect.x - padding,
            state.y + (height + text_rect.y - text_rect.height) / 2,
            width,
            height,
        )

        rrect = skia.RoundRect.from_rect(self.rect, x=button_radius, y=button_radius)

        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.color = button_bg_color
        state.canvas.draw_rrect(rrect)

        state.canvas.paint.style = state.canvas.paint.Style.STROKE
        state.canvas.paint.color = border_color
        state.canvas.draw_rrect(rrect)

        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = False
        state.canvas.paint.textsize = state.font_size
        state.canvas.paint.color = button_text_color
        state.canvas.draw_text(self.text, state.x, state.y + state.font_size)

        state.add_width(width, offset=False)
        state.add_height(height + state.padding)


class Line:
    def __init__(self, bold: bool):
        self.numbered = False
        self.bold = bold
        self.rect = None

    def draw(self, state: State):
        y = state.y + state.padding - 1
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.color = text_color if self.bold else button_bg_color
        state.canvas.draw_line(
            state.x, y, state.x + state.canvas.width - state.font_size, y
        )
        state.add_height(state.font_size)


class Spacer:
    def __init__(self):
        self.numbered = False
        self.rect = None

    def draw(self, state: State):
        state.add_height(state.font_size)


class Image:
    def __init__(self, image: SkiaImage):
        self.numbered = True
        self._image = image
        self.rect = None

    def _resize(self, width: int, height: int) -> SkiaImage:
        aspect_ratio = self._image.width / self._image.height
        if self._image.width < self._image.height:
            height = round(width / aspect_ratio)
        else:
            width = round(height * aspect_ratio)
        return self._image.reshape(width, height)

    def draw(self, state: State):
        image = self._resize(state.image_width, state.image_height)
        state.canvas.draw_image(image, state.x_text, state.y)
        state.add_width(image.width, offset=True)
        state.add_height(image.height + state.padding)


class GUI:
    def __init__(
        self,
        callback: Callable,
        screen: Screen or None,
        x: float or None,
        y: float or None,
        numbered: bool,
    ):
        self._callback = callback
        self._screen = screen
        self._x = x
        self._y = y
        self._numbered = numbered
        self._x_moved = None
        self._y_moved = None
        self._showing = False
        self._screen_current = None
        self._buttons: dict[str, Button] = {}
        self._texts: dict[str, Text] = {}

    @property
    def showing(self):
        return self._showing

    def show(self):
        self._screen_current = self._get_active_screen()
        # Initializes at minimum size so to calculate and set correct size later
        self._canvas = Canvas(self._screen_current.x, self._screen_current.y, 1, 1)
        self._showing = True
        self._canvas.draggle = True
        self._canvas.blocks_mouse = True
        self._last_mouse_pos = None
        self._canvas.register("draw", self._draw)
        self._canvas.register("mouse", self._mouse)

    def freeze(self):
        self._canvas.freeze()

    def hide(self):
        if self._showing:
            self._canvas.unregister("draw", self._draw)
            self._canvas.unregister("mouse", self._mouse)
            self._canvas.close()
            self._buttons = {}
            self._texts = {}
            self._showing = False

    def text(self, text: str) -> bool:
        return self._text(text, header=False)

    def header(self, text: str) -> bool:
        return self._text(text, header=True)

    def _text(self, text: str, header: bool) -> bool:
        if text in self._texts:
            element = self._texts[text]
        else:
            element = Text(text, header)
            self._texts[text] = element
        self._elements.append(element)
        return element.is_clicked()

    def button(self, text: str) -> bool:
        if text in self._buttons:
            element = self._buttons[text]
        else:
            element = Button(text)
            self._buttons[text] = element
        self._elements.append(element)
        return element.is_clicked()

    def line(self, bold: Optional[bool] = False):
        self._elements.append(Line(bold))

    def spacer(self):
        self._elements.append(Spacer())

    def image(self, image):
        self._elements.append(Image(image))

    def _draw(self, canvas):
        canvas.paint.typeface = FONT_FAMILY
        self._elements = []
        self._callback(self)
        self._draw_background(canvas)
        font_size = FONT_SIZE * settings.get("imgui.scale") * self._screen_current.scale
        state = State(canvas, font_size, self._numbered)
        number = 1

        if self._elements:
            for el in self._elements:
                y_start = state.y
                el.draw(state)
                if self._numbered and el.numbered:
                    Text.draw_number(state, y_start, number)
                    number += 1
        else:
            state.width = 1
            state.height = 1

        # Resize to fit content
        if canvas.width != state.get_width() or canvas.height != state.get_height():
            self._resize(state.get_width(), state.get_height())

    def _resize(self, width: int or float, height: int or float):
        screen = self._screen_current
        if self._x_moved:
            x = self._x_moved
        elif self._x is not None:
            x = screen.x + screen.width * self._x
        else:
            x = screen.x + max(0, (screen.width - width) / 2)
        if self._y_moved:
            y = self._y_moved
        elif self._y is not None:
            y = screen.y + screen.height * self._y
        else:
            y = screen.y + max(0, (screen.height - height) / 2)
        if self._showing:
            self._canvas.rect = Rect(x, y, width, height)

    def _move(self, dx: float, dy: float):
        self._x_moved = self._canvas.rect.x + dx
        self._y_moved = self._canvas.rect.y + dy
        center_x = self._canvas.rect.center.x + dx
        center_y = self._canvas.rect.center.y + dy
        self._screen_current = self._get_screen_for_pos(center_x, center_y)
        self._canvas.move(self._x_moved, self._y_moved)

    def _draw_background(self, canvas):
        rrect = skia.RoundRect.from_rect(canvas.rect, x=border_radius, y=border_radius)

        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.color = background_color
        canvas.draw_rrect(rrect)

        canvas.paint.style = canvas.paint.Style.STROKE
        canvas.paint.color = border_color
        canvas.draw_rrect(rrect)

    def _mouse(self, e: MouseEvent):
        if e.event == "mousedown" and e.button == 0:
            if not self._get_element(e.gpos):
                self._last_mouse_pos = e.gpos
        elif e.event == "mousemove" and self._last_mouse_pos:
            dx = e.gpos.x - self._last_mouse_pos.x
            dy = e.gpos.y - self._last_mouse_pos.y
            self._last_mouse_pos = e.gpos
            self._move(dx, dy)
        elif e.event == "mouseup" and e.button == 0:
            self._last_mouse_pos = None
            element = self._get_element(e.gpos)
            if element:
                element.click()

    def _get_element(self, pos):
        for el in self._elements:
            if el.rect and el.rect.contains(pos.x, pos.y):
                return el
        return None

    def _get_active_screen(self) -> Screen:
        if self._screen is not None:
            return self._screen
        try:
            return ui.active_window().screen
        except:
            return ui.main_screen()

    def _get_screen_for_pos(self, x: float, y: float) -> Screen:
        if self._screen_current.contains(x, y):
            return self._screen_current
        for screen in ui.screens():
            if screen.contains(x, y):
                return screen
        raise Exception("Can't find screen for position {x}, {y}")


@dataclass
class ImGUI:
    GUI: GUI

    @classmethod
    def open(
        cls,
        screen: Optional[Screen] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        numbered: Optional[bool] = False,
    ):
        def open_inner(draw):
            return GUI(
                draw,
                numbered=numbered,
                screen=screen,
                x=x,
                y=y,
            )

        return open_inner


imgui = ImGUI(GUI)


@imgui.open(numbered=True, x=0.7, y=0.3)
def gui(gui: imgui.GUI):
    gui.header("Some header")
    gui.line(bold=True)
    gui.text("text before spacer")
    gui.spacer()
    gui.text("text after spacer, jg")
    for i in range(10):
        gui.line()
        gui.text(f"stuff stuff {i}")
    gui.line()
    gui.text(
        """def draw(self, state: State):
            y = state.y + state.padding - 1
            state.canvas.paint.style = state.canvas.paint.Style.FILL
            state.canvas.paint.color = text_color if self.bold else button_bg_color
            state.canvas.draw_line(
                state.x, y, state.x + state.canvas.width - state.font_size, y
            )
            state.add_height(state.font_size)"""
    )

    if gui.button("some text"):
        print("Hide")


# gui.show()
