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

TEXT_SIZE = 12
TEXT_COLOR_DARK_MODE = "#D0D0D0"
BUTTON_PADDING = egui.Vec2(5.0, 2.5)
VERTICAL_ITEM_SPACING = 1.0

async def show_row_with_labels(row, contents):
    index = row.index()
    for column in contents[index]:
        async with row.col() as cell_ui:
            cell_ui.label(column)

class PageScroller:
    def __init__(self):
        self.scrolling_time = 0
        self.page_size = 0
        self.page_delta = 0
        self.target_page = None
        self.start_page = None
    
    def increase_page(self):
        self.scrolling_time = 1.0
        self.page_delta += 1
        self.target_page = None

    def decrease_page(self):
        self.scrolling_time = 1.0
        self.page_delta -= 1
        self.target_page = None
    
    def update_target_page(self, current_page):
        if  not self.start_page:
            self.start_page = current_page

        self.target_page = self.start_page + self.page_delta
        return self.target_page*self.page_size

    def handle_scroll(self, time_unit):
        self.scrolling_time -= time_unit
        self.scrolling_time = max(self.scrolling_time, 0)
    
    def is_scrolling(self):
        return self.scrolling_time > 0

        
@dataclass
class TableState:
    top_row: int | None
    bottom_row: int | None

class Helpers:
    def get_text_size(self) -> float:
        return TEXT_SIZE

    def get_label_row_size(self, ui) -> float:
        return ui.spacing().item_spacing.y + egui.TextStyle.Body.resolve(ui.style()).size

    def get_item_spacing(self, ui) -> float:
        return ui.spacing().item_spacing.y

    def title(self, ui: egui.Ui, text: str):
        title = egui.RichText(text).size(TEXT_SIZE * 1.5).strong()
        ui.label(title)
        ui.separator()
        ui.add_space(8)

    def button(self, ui: egui.Ui, text: str) -> bool:
        return ui.button(text).clicked()

    def spacing(self, ui: egui.Ui):
        ui.add_space(TEXT_SIZE)

    async def draw_table(self, ui, headers, rows, row_height=None, show_row=None, auto_size_columns=False, maximum_height=None, id_salt=None, page_delta: int=0):
        if id_salt is None:
            id_salt = str(rows)
        if maximum_height is None:
            maximum_height = ui.available_height()
        column_width = ui.available_width()/len(headers)
        table = (
                egui.TableBuilder(ui)
                .cell_layout(egui.Layout.left_to_right(egui.Align.Center).with_main_wrap(True))
                .min_scrolled_height(0.0)
                .max_scroll_height(maximum_height)
                .animate_scrolling(False)
                .id_salt(id_salt)
            )
        for _ in range(len(headers)):
            if auto_size_columns:
                table = table.column(egui.Column.auto())
            else:
                table = table.column(egui.Column.remainder().at_most(column_width))
        
        if page_delta != 0:
            target_row = 10
            print("scrolling to row", target_row, page_delta)
            table = table.scroll_to_row(target_row, egui.Align.TOP)

        async with table.header(20) as header:
            for h in headers:
                async with header.col() as header_ui:
                    header_ui.strong(h)

        if row_height is None:
            row_height = ui.spacing().interact_size.y
        if show_row is None:
            show_row = show_row_with_labels
        current_row_index = None
        last_row_index = None

        async with header.table().body() as body:
            body_rect = body.max_rect()
            body_top = min(body_rect.top(), body_rect.bottom())
            body_bottom = max(body_rect.top(), body_rect.bottom())
            async for row in body.rows(row_height, len(rows)):
                row.set_overline(True)
                await show_row(row, rows)
                response = row.response()
                rect = response.rect
                top = min(rect.top(), rect.bottom()) - body_top
                bottom = body_bottom - max(rect.top(), rect.bottom())
                if current_row_index is None and top >= 0:
                    current_row_index = row.index()
                if bottom >= 0:
                    last_row_index = row.index()
        return TableState(current_row_index, last_row_index)



def open_gui(
    *,
    screen: Screen | None = None,
    x: float | None = None,
    y: float | None = None,
    width: float | None = None,
    height: float | None = None,
):
    def open_inner(draw):
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
    draw: Callable
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
        draw: Callable,
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
            cron.after("1ms", self.hide)
            return

        try:
            self._stored_rect = self._window.rect
            self._window.close()
        finally:
            self._window = None

    async def _render(self, ui: egui.Ui) -> None:
        self._apply_theme(ui)

        frame = egui.Frame().inner_margin(16.0)

        async with frame.show() as content_ui:
            try:
                self._egui = content_ui
                await self._props.draw(content_ui, Helpers())
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
        spacing = style.spacing
        spacing.button_padding = BUTTON_PADDING
        spacing.item_spacing = egui.Vec2(spacing.item_spacing.x, VERTICAL_ITEM_SPACING)
        style.spacing = spacing

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