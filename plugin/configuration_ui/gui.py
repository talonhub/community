# This file has code taken from
# distributed under the license:
# MIT License
# https://github.com/AndreasArvidsson/andreas-talon/tree/main?tab=MIT-1-ov-file
# Copyright (c) 2021 Andreas Arvidsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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
INNER_MARGIN = 16.0


async def show_row_with_labels(row, contents):
    """Show every column of the row using a label"""
    index = row.index()
    for column in contents[index]:
        async with row.col() as cell_ui:
            cell_ui.label(column)


class PageScroller:
    """Helps with programmatic scrolling by tracking pagination, determining how far to scroll to reach a target page, and determining when the target page has been reached.
    There should be 2 clients for this class: (1) the part of the code responsible for initiating programmatic scrolling and (2) the part of the code providing the target scroll area.
    Client 1: set page_size first, then call increase_page, decrease_page to trigger scrolling
    Client 2: call is_scrolling to decide if programmatic scrolling should be triggered. call update_start_page on every loop with the current scrolling position and maximum. when scrolling, call compute_target to compute where to scroll to.
    """

    __slots__ = ("page_delta", "page_size", "scroll", "start", "start_page")

    def __init__(self):
        self.page_size = 0
        self.page_delta = 0
        self.start_page = None
        self.start = None
        self.scroll = False

    def increase_page(self):
        self.page_delta += 1
        self.scroll = True

    def decrease_page(self):
        self.page_delta -= 1
        self.scroll = True

    def update_start_page(self, current, maximum_target):
        page = current // self.page_size
        if not self.is_scrolling() or self.start_page is None:
            self.start = current
            self.start_page = page
        target = self.compute_target(maximum_target)
        if (
            self.is_scrolling()
            and page == target // self.page_size
            or (current + self.page_size > target)
        ):
            self.scroll = False
            self.page_delta = 0

    def compute_target(self, maximum):
        target_page = self.start_page + self.page_delta
        # if going back and not at the page start, then the first move back moves to the start of the current page
        if self.page_delta < 0 and self.start % self.page_size != 0:
            target_page += 1
        target = target_page * self.page_size
        target = min(target, maximum)
        target = max(target, 0)
        if target + self.page_size > maximum:
            target = maximum - self.page_size + 1
        return target

    def is_scrolling(self):
        return self.scroll


class Helpers:
    """Provides helper methods for drawing on a ui. These methods use the wrapped ui by default, but you can use the ui parameter to provide another one"""

    __slots__ = ("ui",)

    def __init__(self, ui):
        self.ui = ui

    def _ui(self, ui):
        if ui is not None:
            return ui
        return self.ui

    def get_text_size(self, ui=None) -> float:
        """Compute the text size of the ui"""
        ui = self._ui(ui)
        return egui.TextStyle.Body.resolve(ui.style()).size

    def get_label_row_size(self, ui=None) -> float:
        """Compute the size of a row consisting of a text label"""
        ui = self._ui(ui)
        return (
            ui.spacing().item_spacing.y + egui.TextStyle.Body.resolve(ui.style()).size
        )

    def get_item_spacing(self, ui=None) -> float:
        """Get the vertical item spacing"""
        ui = self._ui(ui)
        return ui.spacing().item_spacing.y

    def title(self, text, subtitle="", ui=None):
        """Draw a title.
        text: the main title
        subtitle: an optional subtitle shown in smaller font
        """
        ui = self._ui(ui)
        title = egui.RichText(text).size(TEXT_SIZE * 1.5).strong()
        ui.label(title)
        if subtitle:
            ui.strong(subtitle)
        ui.separator()
        ui.add_space(8)

    def button(self, text, ui=None) -> bool:
        """Draw a button and return True if the button was clicked this frame"""
        ui = self._ui(ui)
        return ui.button(text).clicked()

    def spacing(self, ui=None):
        """Add space based on the default text size"""
        ui = self._ui(ui)
        ui.add_space(TEXT_SIZE)

    async def draw_table(
        self,
        headers,
        rows,
        row_height=None,
        show_row=None,
        auto_size_columns=False,
        maximum_height=None,
        id_salt=None,
        scroller=None,
        ui=None,
    ):
        """Draw a table with consistent row height. Assumes each row is at most the given row height. Uses the interact_size of the ui for the default row height, which may be excessive for your application. This assumes that each row has a single line.
        headers: the headers to show at the top of the table. The length of the headers should equal the column size of the rows.
        rows: the rows to display in the table.
        row_height: each row should be at most this big.
        show_row: a callback for displaying the row. The default uses a label for each column.
        auto_size_columns: decides if the column width should be based on the item sizes. Otherwise, each column takes an equal portion of the available width.
        maximum_height: the maximum height of the scroll area for the table. Setting this is recommended if you need to leave room for widgets after the table.
        id_salt: used to distinguish between this table and other tables in the ui. The default used by this function is str(rows), which may be expensive.
        scroller: handles programmatic scrolling.
        """
        ui = self._ui(ui)

        # use defaults when needed
        if id_salt is None:
            id_salt = str(rows)
        if maximum_height is None:
            maximum_height = ui.available_height()
        if row_height is None:
            row_height = ui.spacing().interact_size.y
        if show_row is None:
            show_row = show_row_with_labels

        async with ui.scope() as scope, scope.style_mut() as style:
            # make scrollbar always visible when a scroll area is needed
            spacing = style.spacing
            spacing.scroll = egui.ScrollStyle.solid()
            style.spacing = spacing

            # set up the table
            column_width = ui.available_width() / len(headers)
            table = (
                egui.TableBuilder(ui)
                .cell_layout(
                    egui.Layout.left_to_right(egui.Align.Center).with_main_wrap(False)
                )
                .min_scrolled_height(0.0)
                .max_scroll_height(maximum_height)
                .animate_scrolling(False)
                .id_salt(id_salt)
            )
            # set column sizes
            for _ in range(len(headers)):
                if auto_size_columns:
                    table = table.column(egui.Column.auto())
                else:
                    table = table.column(
                        egui.Column.remainder().at_most(column_width).clip(True)
                    )
            # scroll programmatically if needed
            if scroller and scroller.is_scrolling():
                target_row = scroller.compute_target(len(rows) - 1)
                table = table.scroll_to_row(target_row, egui.Align.TOP)

            # add the headers
            async with table.header(20) as header:
                for h in headers:
                    async with header.col() as header_ui:
                        header_ui.strong(h)

            current_row_index = None

            # show the visible rows
            async with header.table().body() as body:
                # track the top of the rectangle to help determine the first visible row
                # this still gets called for some rows that are not visible, but those can be filtered out because they are considered above the scroll area
                body_rect = body.max_rect()
                body_top = min(body_rect.top(), body_rect.bottom())
                async for row in body.rows(row_height, len(rows)):
                    # draw lines above each row with a value for the first column
                    if rows[row.index()][0]:
                        row.set_overline(True)
                    # let the call back decide how to draw the row
                    await show_row(row, rows)
                    # if this is the first visible row, update current_row_index
                    response = row.response()
                    rect = response.rect
                    top = min(rect.top(), rect.bottom()) - body_top
                    if current_row_index is None and top >= 0:
                        current_row_index = row.index()
            # update the scroller's understanding of the scroll area location
            if (
                scroller
                and scroller.page_size is not None
                and current_row_index is not None
            ):
                scroller.update_start_page(current_row_index, len(rows) - 1)


def open_gui(
    *,
    screen: Screen | None = None,
    x: float | None = None,
    y: float | None = None,
    width: float | None = None,
    height: float | None = None,
    refresh_period: str | None = None,
    toplevel: bool = True,
    decorated: bool = False,
):
    """Decorator for for an egui callback drawing function.
    screen: the screen to show the gui on.
    x, y, width, height: location and dimensions of the gui window relative to the screen. The width and height are fractions of the screen width/height.
    refresh_period: an optional string giving a cron time period for how often to refresh the gui. egui only updates a ui when the user interacts with it by, so setting this causes a periodic refresh. If you only need to update the ui under specific conditions, call .refresh() on the GUI instead.
    toplevel: decides if the ui should be shown as the top level.
    decorated: decides if the gui should be shown with window borders.
    """

    def open_inner(draw):
        return GUI(
            draw,
            screen=screen,
            x=x,
            y=y,
            width=width,
            height=height,
            refresh_period=refresh_period,
            toplevel=toplevel,
            decorated=decorated,
        )

    return open_inner


@dataclass
class Props:
    """Contains information on how to draw the ui"""

    draw: Callable
    screen: Screen | None
    x: float | None
    y: float | None
    width: float | None
    height: float | None
    toplevel: bool
    decorated: bool

    def will_auto_size(self):
        return self.width is None or self.height is None

    def create_window(self, callback):
        """Create a window for showing the callback on a ui. This allows wrapping the draw callable."""
        window = Window()
        window.draggable = True
        window.autosize = self.will_auto_size()
        window.decorated = self.decorated
        window.toplevel = self.toplevel
        window.set_content(callback)
        return window


class GUI:
    """Manages an egui window"""

    _props: Props
    _window: Window | None
    _egui: egui.Ui | None
    _stored_rect: Rect | None
    _refresh_period: str | None
    _last_height_taken: float | None
    _previous_height_taken: float | None

    def __init__(
        self,
        draw: Callable,
        screen: Screen | None,
        x: float | None,
        y: float | None,
        width: float | None,
        height: float | None,
        refresh_period: str | None,
        toplevel: bool,
        decorated: bool,
    ):
        self._props = Props(
            draw=draw,
            screen=screen,
            x=x,
            y=y,
            width=width,
            height=height,
            toplevel=toplevel,
            decorated=decorated,
        )
        self._window = None
        self._egui = None
        self._stored_rect = None
        self._refresh_period = refresh_period
        self._refresh_job = None
        self._last_height_taken = None
        self._previous_height_taken = None

    @property
    def showing(self) -> bool:
        return self._window is not None

    def show(self):
        if self.showing:
            self._window.focus()
            return

        self._cancel_refresh_job()

        self._window = self._props.create_window(self._render)

        if self._stored_rect is not None and not self._props.will_auto_size():
            self._window.show()
            self._window.rect = self._stored_rect
        else:
            screen = self._get_screen()
            self._window.show()
            rectangle = self._compute_rect_relative_to_screen(screen.rect)
            if self._stored_rect is not None and self._props.will_auto_size():
                rectangle.x = self._stored_rect.x
                rectangle.y = self._stored_rect.y
            self._window.rect = rectangle

        if self._refresh_period:
            self._refresh_job = cron.interval(self._refresh_period, self.refresh)

    def _cancel_refresh_job(self):
        if self._refresh_job:
            cron.cancel(self._refresh_job)
            self._refresh_job = None

    def hide(self):
        self._cancel_refresh_job()

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

        available_height = ui.available_height()
        frame = egui.Frame().inner_margin(INNER_MARGIN)

        async with frame.show() as content_ui:
            try:
                self._egui = content_ui
                await self._props.draw(content_ui, Helpers(content_ui))
            finally:
                # An egui.Ui is only valid during the current frame.
                self._egui = None
        # keep track of the amount of height actually taken
        self._last_height_taken = (
            available_height - ui.available_height() + INNER_MARGIN
        )

    def _apply_theme(self, ui: egui.Ui) -> None:
        style = ui.style()
        visuals = style.visuals()

        # Default dark mode text is too dark.
        if visuals.dark_mode:
            visuals.override_text_color = egui.Color32.from_hex(TEXT_COLOR_DARK_MODE)
            style.set_visuals(visuals)

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

    def _compute_rect_relative_to_screen(self, screen: Rect) -> Rect:
        """Compute the rectangle for the window relative to the screen location and dimensions."""
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

    def focus(self):
        if self._window:
            self._window.focus()

    def refresh(self):
        if self._window:
            # do our own auto sizing instead of the builtin for now
            # our on detection of the height is flawed unless we allow the auto sizing first
            # so when we detect a height change, temporarily re enable auto sizing
            if self._last_height_taken is not None and self._props.will_auto_size():
                if (
                    self._previous_height_taken
                    and self._last_height_taken != self._previous_height_taken
                ):
                    self._window.autosize = True
                else:
                    self._window.autosize = False
                    self._window.resize(
                        int(self._window.rect.width), int(self._last_height_taken)
                    )
                self._previous_height_taken = self._last_height_taken
            self._window.refresh()