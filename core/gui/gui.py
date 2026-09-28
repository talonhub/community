"""This file has code taken from 
distributed under the license:
MIT License
https://github.com/AndreasArvidsson/andreas-talon/tree/main?tab=MIT-1-ov-file
Copyright (c) 2021 Andreas Arvidsson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from collections.abc import Callable
from dataclasses import dataclass

import egui
from skia import Rect
from talon import cron, ui
from talon.egui import Window
from talon.screen import Screen

TEXT_SIZE = 14
TEXT_COLOR_DARK_MODE = "#D0D0D0"
BUTTON_PADDING = egui.Vec2(5.0, 2.5)

class Helpers:
    pass

draw_callback_type = Callable[[egui.Ui, Helpers], None]

def open_gui(
    *,
    screen: Screen | None = None,
    x: float | None = None,
    y: float | None = None,
    width: float | None = None,
    height: float | None = None,
):
    def open_inner(draw: draw_callback_type):
        return GUI(
            draw,
            screen=screen,
            x=x,
            y=y,
            width=width,
            height=height,
        )

    return open_inner


@dataclass
class Props:
    draw: draw_callback_type
    screen: Screen | None
    x: float | None
    y: float | None
    width: float | None
    height: float | None


class GUI:
    _props: Props
    _window: Window | None
    _egui: egui.Ui | None
    _stored_rect: Rect | None

    def __init__(
        self,
        draw: draw_callback_type,
        screen: Screen | None,
        x: float | None,
        y: float | None,
        width: float | None,
        height: float | None,
    ):
        self._props = Props(
            draw=draw,
            screen=screen,
            x=x,
            y=y,
            width=width,
            height=height,
        )
        self._window = None
        self._egui = None
        self._stored_rect = None

    @property
    def showing(self) -> bool:
        return self._window is not None

    def show(self):
        if self.showing:
            return

        self._window = Window()
        self._window.draggable = True
        self._window.autosize = self._props.width is None or self._props.height is None
        # Hide title bar
        self._window.decorated = False
        self._window.set_content(self._render)

        if self._stored_rect is not None:
            self._window.show()
            self._window.rect = self._stored_rect
        else:
            screen = self._get_screen()
            self._window.show()
            self._window.rect = self._apply_partial_rect(screen.rect)

    def hide(self):
        if self._window is None:
            return

        # Defer hiding until after rendering
        if self._egui is not None:
            cron.after("0ms", self.hide)
            return

        try:
            self._stored_rect = self._window.rect
            self._window.close()
        finally:
            self._window = None

    def text(self, text: str):
        self._ui().label(text)

    def header(self, text: str):
        self._ui().heading(text)

    def title(self, text: str):
        ui = self._ui()
        title = egui.RichText(text).size(TEXT_SIZE * 1.5).strong()
        ui.label(title)
        ui.separator()
        self._ui().add_space(8)

    def button(self, text: str) -> bool:
        return self._ui().button(text).clicked()

    def separator(self):
        self._ui().separator()

    def spacing(self):
        self._ui().add_space(TEXT_SIZE)

    async def _render(self, ui: egui.Ui) -> None:
        self._apply_theme(ui)

        frame = egui.Frame().inner_margin(16.0)

        async with frame.show() as content_ui:
            try:
                self._egui = content_ui
                self._props.draw(content_ui, Helpers())
            finally:
                # An egui.Ui is only valid during the current frame.
                self._egui = None

    def _apply_theme(self, ui: egui.Ui) -> None:
        style = ui.style()
        visuals = style.visuals()

        # Default dark mode text is too dark.
        if visuals.dark_mode:
            visuals.override_text_color = egui.Color32.from_hex(TEXT_COLOR_DARK_MODE)
            style.set_visuals(visuals)

        # Default text size (13) is too small. This also applies to the button text.
        style.set_text_style(
            egui.TextStyle.Body,
            egui.FontId(TEXT_SIZE, egui.FontFamily.Proportional),
        )

        # Default button padding (4, 1) is too little.
        style.spacing.button_padding = BUTTON_PADDING

        ui.set_style(style)

    def _apply_partial_rect(self, screen: Rect) -> Rect:
        if self._window is None:
            raise RuntimeError("Window is not initialized")

        props = self._props
        window = self._window.rect

        width = window.width if props.width is None else screen.width * props.width
        height = window.height if props.height is None else screen.height * props.height

        if props.x is None:
            x = screen.center.x - width / 2
        else:
            x = screen.x + screen.width * props.x

        if props.y is None:
            y = screen.center.y - height / 2
        else:
            y = screen.y + screen.height * props.y

        return Rect(x, y, width, height)

    def _get_screen(self):
        if self._props.screen is not None:
            return self._props.screen
        try:
            return ui.active_window().screen
        except Exception as e:
            print(f"Error getting active screen, defaulting to main screen: {e}")
            return ui.main_screen()

    def _ui(self) -> egui.Ui:
        if self._egui is None:
            raise RuntimeError(
                "GUI widgets may only be created inside the draw callback"
            )
        return self._egui