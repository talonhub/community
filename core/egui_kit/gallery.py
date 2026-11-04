"""A dev window showing every egui kit control in its states: "egui kit gallery".

The kit's third user and its test surface: screenshots of the shared look, UIA dumps
per control, and a place to try a kit change without opening a tool. The only kit file
that declares anything to Talon.
"""

import egui
from talon import Module, app

from . import grid, menu, native, shortcuts, table, widgets
from .a11y import dump_uia
from .geom import P, R
from .host import HostWindow
from .search_box import search_box
from .theme import THEME, font
from .widgets import Chip, Kit

TITLE = "egui kit gallery"
_STASH = "_talon_egui_kit_gallery"

mod = Module()


class Gallery:
    def __init__(self):
        self.kit = Kit("gallery", THEME)
        self.text = egui.Mutable("")
        self.choice = "b"
        self.nav = "all"
        self.toggles = {"on": True, "off": False}
        self.setting = True
        self.chips = ["alpha", "beta clash", "gamma"]
        self.clicks = 0
        self.menu = menu.MenuState()
        self.sort = ("name", False)
        self.selected_row = 1
        self.chip = True
        self.letter = "C"
        self.pinned = False
        self.host = HostWindow(
            TITLE, self.render, theme=THEME, tag="egui_kit_gallery", decorated=True, resizable=True, draggable=True, autosize=False, focusable=True
        )

    def show(self):
        self.host.ensure_open()
        self.host.show(focus=True)
        left, top, right, bottom = native.foreground_work_area()
        width, height = min(2200, right - left), min(1500, bottom - top)
        x, y = left + (right - left - width) // 2, top + (bottom - top - height) // 2

        def place(hwnd):
            native.move_hwnd(hwnd, (x, y, x + width, y + height))
            self.host.repaint()

        self.host.when_ready(place)

    def hide(self):
        self.host.hide()

    def shutdown(self):
        self.host.close()

    def set_theme(self, theme):
        self.kit = Kit("gallery", theme)
        self.host.theme = theme
        self.host._prepared = False
        self.host.repaint()

    async def render(self, ui: egui.Ui) -> None:
        kit = self.kit
        t = kit.theme
        painter = ui.painter()
        full = ui.max_rect()
        painter.rect_filled(full, 0, t.bg)
        x, y = full.min.x + 20, full.min.y + 16
        col2 = x + 700

        painter.text(P(x, y + 16), egui.Align2.LEFT_CENTER, f"clicks: {self.clicks}", font(13), t.text_muted)
        y += 52

        widgets.section_label(painter, kit, x, y, "Buttons")
        y += 22
        bx = x
        for kind in ("primary", "secondary", "outline"):
            for enabled in (True, False):
                label = kind if enabled else "disabled"
                if widgets.button(ui, kit, R(bx, y, 100, 32), label, kind, enabled=enabled, key=f"{kind}:{enabled}"):
                    self.clicks += 1
                bx += 108
        y += 44
        bx = x
        for label, active in (("Pill", False), ("Active  >", True)):
            size = widgets.pill_size(painter, label, height=22)
            if widgets.button(ui, kit, R(bx, y, size.x, size.y), label, "pill", active=active, key="pill:" + label):
                self.clicks += 1
            bx += size.x + 8
        bx += 16
        for glyph in widgets.GLYPHS:
            if widgets.icon_button(ui, kit, R(bx, y, 22, 22), glyph, name=glyph.capitalize(), key="glyph:" + glyph, tip=glyph):
                self.clicks += 1
            bx += 30
        widgets.paint_check(painter, kit, P(bx + 10, y + 11))
        widgets.paint_check(painter, kit, P(bx + 32, y + 11), radius=6.0)
        y += 44

        widgets.section_label(painter, kit, x, y, "Toggles")
        y += 22
        bx = x
        for key in ("on", "off"):
            if widgets.toggle(ui, kit, R(bx, y, 40, 22), self.toggles[key], name=f"Toggle {key}", key="toggle:" + key):
                self.toggles[key] = not self.toggles[key]
            bx += 56
        widgets.toggle(ui, kit, R(bx, y, 40, 22), True, name="Disabled toggle", key="toggle:disabled", enabled=False)
        y += 40
        if widgets.setting_row(ui, kit, x, y, 400, "A setting", "Its description, in muted text.", self.setting, key="setting"):
            self.setting = not self.setting
        y += 64

        widgets.section_label(painter, kit, x, y, "Chips")
        y += 22
        bx = x
        for variant in widgets.CHIP_VARIANTS:
            widgets.paint_chip(painter, kit, R(bx, y, 80, 22), variant, variant)
            bx += 88
        y += 34
        chips = [Chip(text, "warn" if "clash" in text else "accent", remove_key="chip:" + text) for text in self.chips]
        removed, y = widgets.chip_flow(ui, kit, x, y, x + 400, chips, height=30, size=13.5, radius=8, pad=12)
        if removed is not None:
            self.chips.pop(removed)
        if not self.chips:
            self.chips = ["alpha", "beta clash", "gamma"]
        y += 40
        many = [Chip(f"form {n}", "auto") for n in range(12)]
        widgets.chip_flow(ui, kit, x, y + 11, x + 400, many, wrap_lines=False)
        y += 34
        _, y = widgets.chip_flow(ui, kit, x, y, x + 400, many, height=26, size=13, radius=7, pad=10)
        y += 40

        # Second column.
        y2 = full.min.y + 68
        widgets.section_label(painter, kit, col2, y2, "Text field")
        y2 += 22
        await widgets.text_field(ui, kit, R(col2, y2, 300, 38), self.text, hint="Type here", name="Gallery text")
        y2 += 54
        widgets.section_label(painter, kit, col2, y2, "Combo box")
        y2 += 22
        options = [("a", "Option A"), ("b", "Option B"), ("c", "Option C")]
        picked = await widgets.combo(
            ui, kit, R(col2, y2, 300, 38), salt="gallery_combo", name="Choice", selected_text=dict(options)[self.choice], options=options, selected=self.choice
        )
        if picked is not widgets.NO_CHANGE:
            self.choice = picked
        y2 += 54
        widgets.section_label(painter, kit, col2, y2, "Nav list")
        y2 += 22
        picked, y2 = widgets.nav_list(ui, kit, col2, y2, 300, [("all", "All", 12), ("on", "Enabled", 9), ("off", "Disabled", 3)], self.nav)
        if picked is not None:
            self.nav = picked
        y2 += 16
        card = R(col2, y2, 300, 120)
        widgets.card(painter, kit, card)
        widgets.key_values(painter, kit, col2 + 16, y2 + 16, 268, [("Executable", "example.exe"), ("Path", r"C:\Program Files\Example\example.exe")])

        # Under the first column: a menu with every kind of row.
        col3 = x
        y3 = y
        widgets.section_label(painter, kit, col3, y3, "Menu")
        y3 += 22
        items = self.menu_items(self.menu.page)
        async with ui.input() as inp:
            pointer = inp.pointer.latest_pos()
            moving = inp.pointer.is_moving()
        picked = menu.draw_menu(
            ui, kit, self.menu, items, R(col3, y3, menu.WIDTH, menu.height(items)), hover=moving, pointer=pointer, button_tips={"pin": "Pin", "unpin": "Unpin"}
        )
        if picked is not None:
            if picked.page is not None:
                menu.open_page(self.menu, picked.page, self.menu_items(picked.page))
            else:
                picked.action()

        # A sortable table: headings, then scrolling rows.
        tx = x + 310
        ty = y
        widgets.section_label(painter, kit, tx, ty, "Table")
        ty += 22
        columns = table.column_layout(
            [
                table.Column("n", "#", 40),
                table.Column("name", "Name", sortable=True),
                table.Column("size", "Size", 90, align="right", sortable=True),
            ],
            370,
        )
        clicked = table.draw_header(ui, kit, tx, ty, 26, columns, sort=self.sort)
        if clicked is not None:
            self.sort = (clicked, not self.sort[1]) if self.sort[0] == clicked else (clicked, False)
        rows = sorted(
            [(f"file {n:02}", n * 37 % 500) for n in range(40)],
            key=lambda r: r[0] if self.sort[0] == "name" else r[1],
            reverse=self.sort[1],
        )

        def cell(rui, i, row):
            p = rui.painter()
            for c in columns:
                text = str(i + 1) if c.key == "n" else rows[i][0] if c.key == "name" else f"{rows[i][1]} KB"
                if c.column.align == "right":
                    p.text(P(row.min.x + c.x + c.w - 6, row.center().y), egui.Align2.RIGHT_CENTER, text, font(13), t.text)
                else:
                    p.text(P(row.min.x + c.x + 6, row.center().y), egui.Align2.LEFT_CENTER, text, font(13), t.text)
            return False

        result = await table.draw_rows(
            ui, kit, R(tx, ty + 26, 370, 200), len(rows), row_h=30, salt="gallery_rows", cell=cell, row_name=lambda i: rows[i][0], selected=self.selected_row
        )
        if result.clicked is not None:
            self.selected_row = result.clicked

        self.draw_step5(ui, kit, col2, full.min.y + 520)
        self.draw_shortcuts(ui, kit, x + 405, full.min.y + 150, 190)

    def draw_shortcuts(self, ui, kit, x, y, w):
        """Key caps: single keys, combinations, a wrapping legend and a cheat sheet."""
        painter = ui.painter()
        widgets.section_label(painter, kit, x, y, "Keyboard shortcuts")
        y += 22
        for row in (("escape", "enter", "a", "f5", "a-z"), ("ctrl+shift+p", "up down")):
            bx = x
            for keys in row:
                bx = shortcuts.paint_keys(painter, kit, bx, y + 10, keys) + 12
            y += 30
        y += 6
        hints = [
            shortcuts.Shortcut("up down", "Move"),
            shortcuts.Shortcut("enter", "Pick"),
            shortcuts.Shortcut("right", "Open"),
            shortcuts.Shortcut("left backspace", "Back"),
            shortcuts.Shortcut("escape", "Close"),
            shortcuts.Shortcut("a-z", "Window"),
        ]
        card = R(x, y, w, shortcuts.legend_height(painter, hints, w - 20) + 12)
        widgets.card(painter, kit, card)
        y = shortcuts.legend(painter, kit, x + 10, y + 6, w - 20, hints) + 18
        sheet = [
            shortcuts.Shortcut("ctrl+f", "Find"),
            shortcuts.Shortcut("ctrl+shift+p", "Palette"),
            shortcuts.Shortcut("pageup pagedown", "Page"),
            shortcuts.Shortcut("alt+f4", "Close"),
        ]
        shortcuts.shortcut_list(painter, kit, x, y, w, sheet)

    def draw_step5(self, ui, kit, x, y):
        """The search box, a pill row, badges and an index strip."""
        t = kit.theme
        painter = ui.painter()
        widgets.section_label(painter, kit, x, y, "Search box, pills, badges, index")
        y += 22
        if search_box(ui, kit, R(x, y, 330, 32), "", "Type to search", chip_text="app: Example" if self.chip else None, chip_name="Remove filter app:Example"):
            self.chip = False
        if not self.chip and widgets.button(ui, kit, R(x + 240, y + 44, 90, 32), "Chip", "secondary", key="restore-chip"):
            self.chip = True
        y += 44
        pills = [widgets.Pill("p:close", "Close"), widgets.Pill("p:snap", "Snap  >", active=True), widgets.Pill("p:clear", "Clear")]
        widgets.pill_row(ui, kit, x, y + 11, pills, limit=x + 330)
        widgets.badges(painter, kit, [("Desktop 1", t.badge_desktop), ("Screen 2", t.badge_screen)], x + 330, y + 47)
        picked = grid.index_strip(ui, kit, x - 40, y - 440, 240, "#ABCDEFGHIJKLM", set("ACDGKM"), self.letter)
        if picked is not None:
            self.letter = picked

    def menu_items(self, page: str) -> list:
        def count():
            self.clicks += 1

        def pin():
            self.pinned = not self.pinned

        if page == "more":
            return [menu.MenuItem("<  Back", page="main"), menu.MenuItem("Heading", kind="heading"), menu.MenuItem("Deeper item", count)]
        return menu.sections(
            [menu.MenuItem("Focus", count), menu.MenuItem("Disabled item", count, enabled=False)],
            [
                menu.MenuItem("More" + menu.SUBMENU_MARK, page="more"),
                menu.MenuItem("With a button", count, buttons=[("unpin" if self.pinned else "pin", pin)]),
            ],
        )


gallery: Gallery | None = None


def on_ready():
    global gallery
    gallery = HostWindow.replace(_STASH, Gallery, tag="egui_kit_gallery")


app.register("ready", on_ready)


@mod.action_class
class Actions:
    def egui_kit_gallery():
        """Show the egui kit's control gallery (development)"""
        if gallery:
            gallery.show()

    def egui_kit_gallery_hide():
        """Hide the egui kit's control gallery"""
        if gallery:
            gallery.hide()

    def egui_kit_gallery_dump_uia():
        """Print the egui kit gallery's UI Automation tree to the Talon log"""
        dump_uia(TITLE, "egui_kit_gallery", 10)
