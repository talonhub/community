"""Drawing the switcher: render() picks the layout for the mode and draws the header,
marked bar, search field, cells (via the kit's grid), column headings, A-Z index and
scrollbar, and says where the open menu goes; render_menu() draws the menu in its popup
window; the minimap shown while placing."""

import egui
from talon import cron
from ...egui_kit import widgets
from ...egui_kit import menu as kit_menu
from ...egui_kit import table as kit_table
from ...egui_kit import grid as kit_grid
from ...egui_kit.search_box import search_box
from ...egui_kit.text import elide_estimate as elide
from .config import (
    APP_MODES,
    APP_TAG,
    BACKGROUND,
    BORDER,
    CHIP,
    CLOSE_BUTTON,
    COLUMN_HEADER_HEIGHT,
    CURRENT_DESKTOP,
    DESK_TAG,
    DETAIL_COLUMNS,
    DETAIL_ROW_HEIGHT,
    DIM_TEXT,
    HEADER_HEIGHT,
    INDEX_LETTERS,
    INDEX_WIDTH,
    JUMP_MENU_WIDTH,
    KIT,
    LABEL_HEIGHT,
    MARKED,
    MARK_BAR_FONT,
    MENU_BUTTON_TIPS,
    MENU_WIDTH,
    MINIMAP_WIDTH,
    PADDING,
    ROW_GAP,
    ROW_HEIGHT,
    SCREEN_BADGE,
    SCREEN_TAG,
    SCROLLBAR_WIDTH,
    SEARCH_HEIGHT,
    SECTION_HEIGHT,
    SELECTED,
    TEXT,
    TILE,
    TILE_ASPECT,
    WINDOW_DETAIL_COLUMNS,
)
from .menus import Menu
from .model import detail_columns, index_letter, launcher_letters, launcher_sections, tile_hwnds
from .placement import Placement, slot_fractions, slot_label
from .sizing import to_pixels


class ViewsMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    async def render(self, ui: egui.Ui) -> None:
        # (The host turns on AccessKit and asks for the extra frames.)
        painter = ui.painter()
        painter.rect_filled(ui.clip_rect(), 0, BACKGROUND)
        ppp = ui.ctx().pixels_per_point()

        with self.lock:
            entries = list(self.entries)
            pool_hwnds = {entry.hwnd for entry in self.pool}
            # The launcher's installed apps keep their icon textures too.
            icon_hwnds = pool_hwnds | ({a.hwnd for a in self.launch_list.apps} if self.launch_list else set())
            running_count = self.running_count if self.mode == "launcher" else None
            window_rows = self.mode == "windows" and self.window_details
            apps_rows = self.mode == "apps" and bool(self.apps_details)
            details = (self.mode == "launcher" and bool(self.launcher_details)) or window_rows or apps_rows
            if window_rows:
                sort_column, sort_reverse = self.window_sort, self.window_sort_reverse
            elif apps_rows:
                sort_column, sort_reverse = self.apps_sort, self.apps_sort_reverse
            else:
                sort_column, sort_reverse = self.launcher_sort, self.launcher_sort_reverse
            chip = self.chip
            query = self.query
            previews = self.previews
            cols = max(self.cols, 1)
            thumbnails = dict(self.thumbnails)
            current = self.selected
            target = self.target
            placement = self.placement
            placed = dict(placement.placed) if placement else {}
            desktops = list(self.desktops)
            current_desktop = self.current_desktop
            show_screens = self.screen_count > 1
            menu = self.menu
            mode = self.mode
            marked = set(self.marked) & pool_hwnds
            if bool(self.marked) != ("user.thumbnail_switcher_marked" in (self.tag_context.tags if self.tag_context is not None else ())):
                # Marks come and go in many places; the marked bar's voice commands
                # follow from here.
                cron.after("0ms", self._update_tags)
            menu_entry = self._menu_entry(menu)
            if menu is not None and menu_entry is None and not (menu.marked and marked):
                # Its window (or the last marked one) went away.
                self.menu = menu = None
            if menu is not None and menu.marked and menu.page in ("snap", "layout") and (menu.page == "snap") != (len(marked) == 1):
                # Marks changed under it: Snap is for one marked window, Layout for several.
                self.menu = menu = None
            # The first frames can come before the window has its final size; scrolling
            # the selection into view then would leave the list scrolled for no reason.
            settled = target is not None and abs(
                ui.clip_rect().height() * ppp - (target[3] - target[1])
            ) < 3
            reveal = self.reveal_selected and settled
            if reveal:
                self.reveal_selected = False
            # Drop textures of windows no longer shown, here on egui's thread.
            self.textures.drop_where(lambda key: key[0] not in icon_hwnds)

        async with ui.input() as inp:
            action = self._handle_input(inp, cols, previews or mode in APP_MODES)
            # Window-relative positions only mean something once the window is in place.
            pointer_pos = inp.pointer.latest_pos()
            pointer_moving = settled and self._pointer_moved(pointer_pos)
            primary_clicked = inp.pointer.primary_clicked()
            # Only a mouse that is moving now takes the selection from the keyboard.
            pointer_moving_now = inp.pointer.is_moving()
            wheel = inp.raw_scroll_delta.y
            # For Ctrl+click and Shift+click.
            ctrl_down = bool(inp.modifiers.ctrl)
            shift_down = bool(inp.modifiers.shift)
        if action is not None:
            # Don't hide the window from inside its own render.
            cron.after("0ms", action)

        area = ui.available_rect_before_wrap()
        heading = chip.label if chip is not None else "All windows"
        # The close button, for the mouse: top right, in line with the search field's edge.
        close_rect = egui.Rect.from_min_size(
            egui.Pos2(area.max.x - PADDING - CLOSE_BUTTON, area.min.y + (HEADER_HEIGHT - CLOSE_BUTTON) / 2),
            egui.Vec2(CLOSE_BUTTON, CLOSE_BUTTON),
        )
        if self._draw_close_button(ui, painter, close_rect):
            cron.after("0ms", self.cancel)
        # The header's switches, right to left from the close button.
        pills = []
        if mode in APP_MODES or placement is None:
            # The layout switch of every view: icons (or tiles) or details. Not while
            # placing windows, which needs the tiles.
            pills.append(widgets.Pill("layout", "Icons" if details else "Details", tip="Switch between icons and details (Ctrl+D)"))
        if mode in ("windows", "apps") and placement is None:
            # Over to the other view, unfiltered: windows <-> apps.
            label = "Apps" if mode == "windows" else "Windows"
            pills.append(widgets.Pill("view", label, name=f"Show {label.lower()}", tip=f"Show {label.lower()}, without filters (Ctrl+Tab)"))
        switch, _rects, header_right = widgets.pill_row(
            ui, KIT, close_rect.min.x - PADDING, area.min.y + HEADER_HEIGHT / 2, pills, align="right", height=22, gap=PADDING
        )
        if switch == "layout":
            if mode == "launcher":
                cron.after("0ms", lambda: self.set_launcher_details(None))
            elif mode == "apps":
                cron.after("0ms", lambda: self.set_apps_details(not self.apps_details))
            else:
                cron.after("0ms", lambda: self.show_window_details(not self.window_details))
        elif switch == "view":
            cron.after("0ms", self.switch_view)
        header_action = None
        if placement is None and marked:
            # The marked windows' bar, instead of the hint.
            visible = {h for e in entries for h in tile_hwnds(e)}
            hidden = sum(1 for h in marked if h not in visible)
            header_action = self._draw_mark_bar(ui, painter, area, len(marked), hidden, show_screens, header_right)
        elif placement is not None:
            text = (
                f"Placing {slot_label(placement.layout)}: {slot_label(placement.slot)} "
                f"({placement.index + 1} of {len(placement.slots)}). Say a number, skip, or cancel"
            )
        elif mode == "launcher":
            text = f"{'App launcher' if chip is None else heading}: type to search, a number or Enter focuses or launches, \"launch new\" a number, \"jump\" a letter or Alt+letter" + (", \"sort by\" a column" if details else "")
        elif mode == "apps" and details:
            text = f"{'Apps' if chip is None else heading}: type to search, say a number or Enter to focus, \"sort by\" a column, Ctrl+D for icons"
        elif mode == "apps":
            text = f"{'Apps' if chip is None else heading}: type to search, say a number or Enter to focus, Down for its windows"
        elif details:
            text = f"{heading}: type to search, say a number or Enter to focus, \"sort by\" a column, Ctrl+D switches views"
        else:
            text = f"{heading}: type to search, say a number, click a window, or use the arrow keys and Enter"
        if not (placement is None and marked):
            painter.text(
                egui.Pos2(area.min.x + PADDING, area.min.y + HEADER_HEIGHT / 2),
                egui.Align2.LEFT_CENTER,
                elide(text, header_right - area.min.x - PADDING, 15.0),
                egui.FontId.proportional(15.0),
                SELECTED if placement is not None else TEXT,
            )
        if header_action is not None:
            cron.after("0ms", header_action)
        field = egui.Rect.from_min_max(
            egui.Pos2(area.min.x + PADDING, area.min.y + HEADER_HEIGHT),
            egui.Pos2(area.max.x - PADDING, area.min.y + HEADER_HEIGHT + SEARCH_HEIGHT - PADDING),
        )
        if placement is not None:
            minimap = egui.Rect.from_min_max(
                egui.Pos2(field.max.x - MINIMAP_WIDTH, field.min.y), field.max
            )
            field = egui.Rect.from_min_max(field.min, egui.Pos2(minimap.min.x - PADDING, field.max.y))
            self._draw_minimap(painter, minimap, placement)
        hint = f'Search titles and apps; "{APP_TAG}name", "{DESK_TAG}2" or "{SCREEN_TAG}2" + Tab filters'
        if chip is not None:
            hint = "Search these windows; Backspace shows all"
        if search_box(
            ui,
            KIT,
            field,
            query,
            hint,
            chip_text=f"{chip.tag} {chip.label}" if chip is not None else None,
            chip_name=f"Remove filter {chip.tag}{chip.label}" if chip is not None else None,
        ):
            cron.after("0ms", lambda: self.set_chip(None))
        show_desktops = len(desktops) > 1

        # Everything below the header and search field scrolls; tiles are clipped to
        # this viewport, so the search field stays put.
        viewport = egui.Rect.from_min_max(
            egui.Pos2(area.min.x, area.min.y + HEADER_HEIGHT + SEARCH_HEIGHT + (COLUMN_HEADER_HEIGHT if details else 0)), area.max
        )
        gap = PADDING if previews else ROW_GAP
        sections = launcher_sections(entries, running_count) if running_count is not None else []
        letter_at = launcher_letters(entries, running_count) if running_count is not None else {}
        # The A-Z index fits the default order, or sorting by application.
        index_letters = set(letter_at.values()) if sort_column in (None, "name") else set()
        if sort_column not in (None, "name"):
            letter_at = {}
        # The launcher keeps room for its A-Z index on the right.
        index_w = INDEX_WIDTH + 6 if index_letters else 0.0
        cell_w = (viewport.width() - 2 * PADDING - index_w) / cols
        if details:
            cell_h = DETAIL_ROW_HEIGHT + ROW_GAP
        elif mode in APP_MODES:
            cell_h = cell_w
        elif previews:
            cell_h = (cell_w - PADDING) / TILE_ASPECT + LABEL_HEIGHT + PADDING
        else:
            cell_h = ROW_HEIGHT + ROW_GAP
        layout = kit_grid.grid_layout(len(entries), cols, sections)
        grid = kit_grid.Grid(viewport, cols, cell_w, cell_h, gap, layout, padding=PADDING, section_h=SECTION_HEIGHT)
        tile_top = grid.top

        with self.lock:
            self.layout, self.sections = layout, sections
            self.page_rows = grid.page_rows
            scroll_to, self.scroll_to = self.scroll_to, None

        # A letter jump puts its row at the top; otherwise the selection (with its
        # heading, if it has one) scrolls into view.
        scroll = grid.scroll(self.scroll, wheel, jump_to=scroll_to, reveal=current if reveal else None)
        self.scroll = scroll

        columns = (
            detail_columns(cell_w - PADDING, show_screens, WINDOW_DETAIL_COLUMNS if window_rows else DETAIL_COLUMNS) if details else []
        )

        clipped = ui.painter_at(viewport)
        view_px = to_pixels(viewport, ppp)
        selected = None
        mark_click = None
        close_click = None
        shown = set()
        # The menu opens in its own popup window (render_menu), so it can reach past
        # this one: where it was opened, or for keyboard and voice at its tile.
        menu_request = None
        if menu is not None and target is not None:
            items = self._menu_items(menu_entry, menu.page)
            anchor = menu.pos
            if anchor is None:
                # The marked windows' menu opens at the selected tile.
                index = entries.index(menu_entry) if menu_entry is not None else max(0, min(current, len(entries) - 1))
                if index < len(layout):
                    col = layout[index][0]
                    anchor = egui.Pos2(
                        viewport.min.x + PADDING + col * cell_w + 40,
                        viewport.min.y + PADDING + tile_top(index) - scroll + 20,
                    )
                else:
                    anchor = viewport.min
            menu_w = JUMP_MENU_WIDTH if menu.page.startswith("jump") else MENU_WIDTH
            # Screen pixels: the window has no frame, so its rect is its client area.
            at = (target[0] + round(anchor.x * ppp), target[1] + round(anchor.y * ppp))
            menu_request = (at, (round(menu_w * ppp), round(kit_menu.height(items) * ppp)))
        if menu_request != self.menu_request:
            self.menu_request = menu_request
            cron.after("0ms", lambda request=menu_request: self._place_menu_popup(request))

        if not entries:
            painter.text(
                egui.Pos2(viewport.center().x, viewport.min.y + 3 * PADDING),
                egui.Align2.CENTER_TOP,
                "No matching windows",
                egui.FontId.proportional(15.0),
                DIM_TEXT,
            )

        # The launcher's section headings.
        grid.section_headings(clipped, KIT, sections, scroll)

        for i, entry in enumerate(entries):
            tile = grid.rect(i, scroll)
            thumbnail = thumbnails.get(entry.hwnd)
            if not tile.intersects(viewport):
                if thumbnail is not None:
                    thumbnail.hide()
                continue

            # Each tile's close button, Alt+Tab style. It sits on the tile, which gets
            # egui's hover and clicks, so the pointer's position decides between them.
            # Not while placing, where clicks pick windows.
            close_rect = self._tile_close_rect(tile, "details" if details else mode, previews)
            has_close = menu is None and placement is None and viewport.contains_rect(close_rect) and bool(tile_hwnds(entry))
            # The close button's own area comes first, under the tile's, so it is its own
            # UIA element (invoked by UI Automation) while the tile still gets the mouse.
            cell = kit_grid.cell_interact(
                ui,
                KIT,
                tile,
                viewport,
                key=str(entry.hwnd),
                name=f"{i + 1} {self._tile_name(entry, mode)}",
                selected=i == current,
                close_rect=close_rect if has_close else None,
                close_name=f"Close {entry.title}",
                pointer=pointer_pos,
            )
            response, hovered, close_hovered = cell.response, cell.hovered, cell.close_hovered
            if hovered and i != current and pointer_moving and pointer_moving_now and menu is None:
                # The mouse moves the selection too, but only while it actually moves
                # (not when tiles scroll under a resting pointer, e.g. after a letter
                # jump), and not while a menu is open for the selected tile.
                with self.lock:
                    self.selected = current = i
            # (An installed app in the launcher has no windows to mark.)
            is_marked = bool(marked) and bool(tile_hwnds(entry)) and all(h in marked for h in tile_hwnds(entry))
            kit_grid.paint_cell(clipped, KIT, tile, selected=i == current, marked=is_marked, hovered=(hovered or close_hovered) and menu is None)

            badges = []
            if entry.hwnd in placed:
                badges.append((f"placed: {slot_label(placed[entry.hwnd])}", SELECTED))
            if show_desktops and entry.desktop_number:
                desktop = next((d for d in desktops if d.number == entry.desktop_number), None)
                is_current = entry.desktop_key == current_desktop
                badges.append((desktop.label() if desktop else str(entry.desktop_number), CURRENT_DESKTOP if is_current else BORDER))
            if show_screens and entry.screen_number and mode not in APP_MODES:
                badges.append((f"Screen {entry.screen_number}", SCREEN_BADGE))
            if details:
                self._draw_detail_row(
                    ui, clipped, entry, i, tile, columns, letter_at.get(i), current_desktop, show_desktops, is_marked
                )
            elif mode in APP_MODES:
                if show_desktops and entry.desktop_numbers:
                    here = current_desktop is not None and any(w.desktop_key == current_desktop for w in entry.windows)
                    numbers = ", ".join(str(n) for n in entry.desktop_numbers)
                    label = f"Desktop{'s' if len(entry.desktop_numbers) > 1 else ''} {numbers}"
                    badges.append((label, CURRENT_DESKTOP if here else BORDER))
                self._draw_app_tile(ui, clipped, entry, i, tile, badges, is_marked, launcher=mode == "launcher", letter=letter_at.get(i))
            elif previews:
                shown.add(entry.hwnd)
                self._draw_tile(ui, clipped, entry, i, tile, thumbnail, view_px, ppp, badges, is_marked)
            else:
                self._draw_row(ui, clipped, entry, i, tile, badges, is_marked)

            if has_close and (hovered or close_hovered or i == current):
                widgets.paint_glyph(clipped, KIT, close_rect, "close", close_hovered)
                if close_hovered:
                    response.on_hover_text(
                        f"Close all {entry.app_name} windows" if mode in APP_MODES else "Close window"
                    )
            if cell.close_clicked():
                # Just this window (or app), even when others are marked.
                close_click = i + 1
            elif menu is None and response.clicked():
                if ctrl_down or shift_down:
                    # Ctrl+click toggles a mark, Shift+click marks a range; a plain
                    # click still focuses the window.
                    with self.lock:
                        self.selected = i
                    mark_click = (self.mark, [i + 1]) if ctrl_down else (self.mark_to, i + 1)
                else:
                    selected = i + 1
            elif response.secondary_clicked():
                with self.lock:
                    self.selected = i
                    # On a marked tile: the marked windows' menu.
                    self.menu = Menu(None, pointer_pos, marked=True) if is_marked else Menu(entry.hwnd, pointer_pos)
                ui.ctx().request_repaint()
                cron.after("0ms", self._update_tags)

        # Windows filtered out by the search keep their thumbnail registered, hidden.
        for hwnd, thumbnail in thumbnails.items():
            if hwnd not in shown:
                thumbnail.hide()

        if details:
            # The column headings, pinned above the rows; a click sorts by that column.
            # Drawn after the rows, on an opaque band, so that rows scrolled up under
            # them never show through (or take their clicks).
            y0 = viewport.min.y - COLUMN_HEADER_HEIGHT
            painter.rect_filled(
                egui.Rect.from_min_max(egui.Pos2(area.min.x, y0), egui.Pos2(area.max.x, viewport.min.y)), 0, BACKGROUND
            )
            sort_key = kit_table.draw_header(
                ui, KIT, viewport.min.x + PADDING, y0, COLUMN_HEADER_HEIGHT, columns, sort=(sort_column, sort_reverse) if sort_column else None
            )
            if sort_key is not None:
                cron.after("0ms", lambda key=sort_key: self.sort_launcher(key))
            painter.line_segment(
                egui.Pos2(viewport.min.x + PADDING, viewport.min.y - 1), egui.Pos2(viewport.max.x - PADDING, viewport.min.y - 1), egui.Stroke(1.0, BORDER)
            )

        if index_letters:
            jump_letter = kit_grid.index_strip(
                ui,
                KIT,
                viewport.max.x - PADDING / 2 - SCROLLBAR_WIDTH - INDEX_WIDTH / 2 - 2,
                viewport.min.y + PADDING,
                viewport.height() - 2 * PADDING,
                INDEX_LETTERS,
                index_letters,
                index_letter(entries[current].title) if running_count <= current < len(entries) else None,
                width=INDEX_WIDTH,
            )
            if jump_letter is not None:
                cron.after("0ms", lambda: self.jump(jump_letter))

        grid.scrollbar(painter, KIT, scroll, SCROLLBAR_WIDTH)

        if menu is not None and primary_clicked:
            # A click here, outside the menu's popup, closes it (and doesn't pick a tile).
            cron.after("0ms", self.close_menu)

        if mark_click is not None:
            cron.after("0ms", lambda: mark_click[0](mark_click[1]))
        if close_click is not None:
            cron.after("0ms", lambda: self.close_windows([close_click]))
        if selected is not None:
            # Don't hide the window from inside its own render.
            cron.after("0ms", lambda: self.select(selected))

    async def render_menu(self, ui: egui.Ui) -> None:
        """The open menu, filling its popup window (egui_kit.popup). The popup never
        takes the focus: keys, numbers and voice still go to the switcher."""
        with self.lock:
            menu = self.menu
            entry = self._menu_entry(menu)
        if menu is None or (entry is None and not menu.marked):
            return
        items = self._menu_items(entry, menu.page)
        async with ui.input() as inp:
            pointer = inp.pointer.latest_pos()
            # Only a mouse that is moving now takes the highlight from the keyboard.
            moving = inp.pointer.is_moving()
            clicked = inp.pointer.primary_clicked()
        rect = ui.max_rect()
        ui.painter().rect_filled(rect, 0, KIT.theme.menu_bg)
        pick = kit_menu.draw_menu(
            ui, KIT, menu, items, rect, hover=moving, pointer=pointer, icon_texture=self._popup_menu_icon, button_tips=MENU_BUTTON_TIPS, clicked=clicked
        )
        if pick is not None:
            cron.after("0ms", lambda: self._pick(menu, pick))

    def _draw_close_button(self, ui: egui.Ui, painter: egui.Painter, rect: egui.Rect) -> bool:
        """An × that closes the switcher, like Escape; returns whether it was clicked."""
        return widgets.icon_button(ui, KIT, rect, "close", name="Close switcher", key="close", tip="Close (Esc)")

    def _draw_mark_bar(
        self, ui: egui.Ui, painter: egui.Painter, area: egui.Rect, count: int, hidden: int, screens: bool, right: float
    ):
        """The header while windows are marked: how many, and buttons acting on them.
        Returns what a clicked button does, to run after the frame."""
        center_y = area.min.y + HEADER_HEIGHT / 2
        summary = f"{count} marked" + (f" ({hidden} hidden)" if hidden else "")
        x = painter.text(
            egui.Pos2(area.min.x + PADDING, center_y), egui.Align2.LEFT_CENTER, summary, egui.FontId.proportional(15.0), MARKED
        ).max.x + 12
        buttons = [
            ("Close", lambda pos: self.close_marked),
            ("Minimize", lambda pos: self.minimize_marked),
            ("Restore", lambda pos: self.restore_marked),
            ("Snap  >", lambda pos: lambda: self.open_bar_dropdown("snap"))
            if count == 1
            else ("Layout  >", lambda pos: lambda: self.open_bar_dropdown("layout")),
            ("Move to desktop  >", lambda pos: lambda: self.open_bar_dropdown("desktop")),
        ]
        if screens:
            buttons.append(("Move to screen  >", lambda pos: lambda: self.open_bar_dropdown("screen")))
        buttons.append(("Clear", lambda pos: self.clear_marks))
        pages = {"Snap  >": "snap", "Layout  >": "layout", "Move to desktop  >": "desktop", "Move to screen  >": "screen"}
        menu = self.menu
        open_page = menu.page if menu is not None and menu.dropdown else None
        pills = [widgets.Pill("marked:" + label, label, active=pages.get(label) is not None and pages.get(label) == open_page) for label, _make in buttons]
        clicked_key, rects, _x = widgets.pill_row(ui, KIT, x, center_y, pills, limit=right, size=MARK_BAR_FONT)
        # Where the dropdowns open (under their buttons), for voice and the arrow keys too.
        self.bar_anchors = {
            pages[label]: egui.Pos2(rects["marked:" + label].min.x, rects["marked:" + label].max.y + 2)
            for label, _make in buttons
            if label in pages and "marked:" + label in rects
        }
        for label, make in buttons:
            if clicked_key == "marked:" + label:
                rect = rects[clicked_key]
                return make(egui.Pos2(rect.min.x, rect.max.y + 2))
        return None

    def _draw_minimap(self, painter: egui.Painter, rect: egui.Rect, placement: Placement):
        """The screen in miniature with the layout's slots; the current one filled."""
        r = placement.screen.visible_rect
        aspect = r.width / max(r.height, 1)
        h = min(rect.height(), rect.width() / aspect)
        w = h * aspect
        screen = egui.Rect.from_center_size(rect.center(), egui.Vec2(w, h))
        painter.rect_filled(screen, 2, TILE)
        placed_slots = set(placement.placed.values())
        for i, slot in enumerate(placement.slots):
            try:
                left, top, right, bottom = slot_fractions(slot)
            except Exception:
                continue
            cell = egui.Rect.from_min_max(
                egui.Pos2(screen.min.x + w * left, screen.min.y + h * top),
                egui.Pos2(screen.min.x + w * right, screen.min.y + h * bottom),
            ).shrink(1.0)
            if i == placement.index:
                painter.rect_filled(cell, 1, SELECTED)
            elif slot in placed_slots:
                painter.rect_filled(cell, 1, CHIP)
            painter.rect_stroke(cell, 1, egui.Stroke(1.0, TEXT), egui.StrokeKind.Inside)
