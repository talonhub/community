"""Drawing the editor with the egui kit: the header, the sidebar (search, filters, the
Executable choice), the list (columns, rows with chips and switches), the detail
panel, and the right-click menu."""

import time
import egui
from talon import cron
from ...egui_kit import widgets
from ...egui_kit import menu as kit_menu
from ...egui_kit import table as kit_table
from ...egui_kit.geom import P, R
from ...egui_kit.text import elide, wrap
from ...egui_kit.theme import THEME, font, mono
from ...egui_kit.widgets import Chip, Kit
from .store import FILTERS


# The shared theme's colours, by the names the drawing code uses.
T = THEME


BG = T.bg


SURFACE = T.surface


BORDER = T.border


DIVIDER = T.divider


HEADER_BG = T.surface_alt


TEXT = T.text


MUTED = T.text_muted


LABEL = T.text_label


FAINT = T.text_faint


WARN_TEXT = T.warn_text


WARN_DOT = T.warn_dot


HEADER_H = 44.0


PAD = 20.0


LEFT_W = 260.0


RIGHT_W = 380.0


ROW_H = 52.0


LIST_HEADER_H = 52.0


COLUMN_HEADER_H = 34.0


TOGGLE_W, TOGGLE_H = 40.0, 22.0


# The list's columns: the application and its spoken forms share the width; "Enabled"
# (its switch) is fixed, at the right.
LIST_COLUMNS = [
    kit_table.Column("application", "APPLICATION", weight=0.52),
    kit_table.Column("forms", "SPOKEN FORMS", weight=0.48),
    kit_table.Column("enabled", "ENABLED", width=84.0, align="right"),
]


# Controls come from the kit, with the editor's ids ("lae:" prefix, UIA ids unchanged)
# and palette.
KIT = Kit("lae", THEME)


class EditorMenu(kit_menu.MenuState):
    """The right-click menu of entry `i`, opened at `pos`."""

    def __init__(self, i: int, pos: egui.Pos2):
        super().__init__()
        self.i = i
        self.pos = pos
        self.fresh = True


# Keys an open menu takes (when no text field has the keyboard).
MENU_KEYS = ("ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Home", "End", "Enter")


DIGIT_KEYS = [(n, getattr(egui.Key, f"Num{n}")) for n in range(1, 10)]


class ViewMixin:
    """Editor methods: see the module docstring. Mixed into Editor, whose state they use."""

    async def render(self, ui: egui.Ui) -> None:
        # (The host sets the theme's visuals and turns on AccessKit on the first frame.)
        with self.lock:
            painter = ui.painter()
            full = ui.max_rect()
            painter.rect_filled(full, 0, BG)

            query = self.query.get().strip().lower()
            shown = [i for i, e in enumerate(self.entries) if self.matches(i, e, query)]
            counts = self.counts(query)
            counts["exes"] = self.exe_counts(query)

            pending = self.unsaved()
            if pending and self.save_job is None:
                self.save_job = cron.after("400ms", self.autosave)
            self.draw_header(ui, painter, R(full.min.x, full.min.y, full.width(), HEADER_H), pending)

            top = full.min.y + HEADER_H + PAD
            bottom = full.max.y - PAD
            height = bottom - top
            # Narrow windows: the side columns give up width before the list does.
            left_w = max(200.0, min(LEFT_W, full.width() * 0.2))
            right_w = max(300.0, min(RIGHT_W, full.width() * 0.28))
            left = R(full.min.x + PAD, top, left_w, height)
            right = R(full.max.x - PAD - right_w, top, right_w, height)
            center = egui.Rect.from_min_max(P(left.max.x + PAD, top), P(right.min.x - PAD, bottom))

            await self.draw_sidebar(ui, painter, left, counts)
            await self.draw_list(ui, painter, center, shown)
            await self.draw_detail(ui, painter, right)
            # Last, so it paints over everything and gets clicks first.
            await self.draw_menu(ui, painter, full)

    def button(self, ui, rect, label, kind="secondary", enabled=True, key=None) -> bool:
        return widgets.button(
            ui, KIT, rect, label, kind, enabled=enabled, key="button:" + (key or label), name=label.replace("+", "").strip()
        )

    def draw_header(self, ui, painter, rect, pending):
        painter.rect_filled(rect, 0, SURFACE)
        painter.hline(rect.min.x, rect.max.x, rect.max.y - 0.5, egui.Stroke(1.0, BORDER))
        x = rect.min.x + 24

        right = P(rect.max.x - 24, rect.center().y)
        if self.message:
            painter.text(right, egui.Align2.RIGHT_CENTER, self.message, font(13), WARN_TEXT)
            return
        if pending:
            label, dot = "Saving…", WARN_DOT
        elif self.saved_at is not None:
            label, dot = "Saved " + time.strftime("%H:%M:%S", time.localtime(self.saved_at)) + " · changes apply immediately", T.success
        else:
            label, dot = "Changes save and apply immediately", T.success
        r = painter.text(right, egui.Align2.RIGHT_CENTER, label, font(13), MUTED)
        painter.circle_filled(P(r.min.x - 10, rect.center().y), 4, dot)

    async def draw_sidebar(self, ui, painter, rect, counts):
        x, y, w = rect.min.x, rect.min.y, rect.width()
        widgets.section_label(painter, KIT, x, y, "Search")
        y += 22
        await widgets.text_field(ui, KIT, R(x, y, w, 38), self.query, hint="Name, exe or spoken form", name="Search")
        y += 38 + 24

        widgets.section_label(painter, KIT, x, y, "Show")
        y += 22
        picked, y = widgets.nav_list(ui, KIT, x, y, w, [(key, label, counts[key]) for key, label in FILTERS], self.filter)
        if picked is not None:
            self.filter = picked
        y += 18

        widgets.section_label(painter, KIT, x, y, "Executable")
        y += 22
        selected = "Any executable" if self.exe_filter is None else self.exe_filter
        picked = await widgets.combo(
            ui,
            KIT,
            R(x, y, w, 38),
            salt="lae_exe",
            name="Executable",
            selected_text=selected,
            options=[(None, "Any executable")] + [(exe, f"{exe}   {n}") for exe, n in counts["exes"]],
            selected=self.exe_filter,
        )
        if picked is not widgets.NO_CHANGE:
            self.exe_filter = picked
        y += 38 + 6
        painter.text(P(x, y), egui.Align2.LEFT_TOP, "Only executables with more than one entry.", font(12), FAINT)

    async def draw_list(self, ui, painter, rect, shown):
        widgets.card(painter, KIT, rect)
        x0, x1 = rect.min.x, rect.max.x
        y = rect.min.y
        title = dict(FILTERS)[self.filter]
        if self.exe_filter is not None:
            title = self.exe_filter if self.filter == "all" else f"{title} · {self.exe_filter}"
        painter.text(P(x0 + 20, y + LIST_HEADER_H / 2), egui.Align2.LEFT_CENTER, title, font(15.5), TEXT)
        count_label = f"{len(shown)} " + ("entry" if len(shown) == 1 else "entries")
        tx = x0 + 20 + widgets.text_size(painter, title, font(15.5)).x + 12
        painter.text(P(tx, y + LIST_HEADER_H / 2), egui.Align2.LEFT_CENTER, count_label, font(13), MUTED)

        any_on = any(self.entries[i].get("exclude") for i in shown)
        any_off = any(not self.entries[i].get("exclude") for i in shown)
        bw, bh = 116, 32
        inc = R(x1 - 20 - bw, y + (LIST_HEADER_H - bh) / 2, bw, bh)
        exc = R(inc.min.x - 10 - bw, inc.min.y, bw, bh)
        if self.button(ui, exc, "Disable All", "outline", bool(shown) and any_off):
            for i in shown:
                self.entries[i]["exclude"] = True
        if self.button(ui, inc, "Enable All", "secondary", bool(shown) and any_on):
            for i in shown:
                self.entries[i]["exclude"] = False
        y += LIST_HEADER_H
        painter.hline(x0, x1, y, egui.Stroke(1.0, BORDER))

        # Column header strip.
        strip = R(x0 + 1, y + 0.5, rect.width() - 2, COLUMN_HEADER_H)
        painter.rect_filled(strip, 0, HEADER_BG)
        columns = kit_table.column_layout(LIST_COLUMNS, rect.width() - 40)
        kit_table.draw_header(ui, KIT, x0 + 20, strip.min.y, COLUMN_HEADER_H, columns, size=11.5, color=LABEL, pad=0)
        forms_off = 20 + columns[1].x
        excl_off = 20 + columns[2].x + columns[2].w
        y += COLUMN_HEADER_H
        painter.hline(x0, x1, y, egui.Stroke(1.0, BORDER))

        body = egui.Rect.from_min_max(P(x0 + 1, y + 1), P(x1 - 1, rect.max.y - 8))
        rows = await kit_table.draw_rows(
            ui,
            KIT,
            body,
            len(shown),
            row_h=ROW_H,
            salt="lae_rows",
            cell=lambda rui, n, row: self.draw_row(rui, shown[n], self.entries[shown[n]], row, forms_off, excl_off),
            row_name=lambda n: self.entries[shown[n]].get("display_name") or "?",
            selected=shown.index(self.selected) if self.selected in shown else None,
            empty_text="No entries match. Try another search or filter.",
        )
        if rows.clicked is not None:
            self.selected = shown[rows.clicked]
            self.new_form.set("")
            self.form_notice = ""
        if rows.secondary is not None:
            n, pos = rows.secondary
            self.selected = shown[n]
            self.menu = EditorMenu(shown[n], pos)

    def draw_row(self, rui, i, e, rect, forms_off, excl_off) -> bool:
        """A row's cells: the name and executable, spoken forms as chips, the Enabled
        switch. True if the switch took the click."""
        uid = e.get("unique_identifier") or str(i)
        painter = rui.painter()
        x = rect.min.x
        name_w = forms_off - 20 - 24
        excluded = bool(e.get("exclude"))
        name = e.get("display_name") or "?"
        name_font = font(14.5)
        nr = painter.text(P(x + 19, rect.min.y + 9), egui.Align2.LEFT_TOP, elide(painter, name, name_font, name_w), name_font, FAINT if excluded else TEXT)
        if excluded:
            painter.hline(nr.min.x, nr.max.x, nr.center().y, egui.Stroke(1.2, FAINT))
        sub = e.get("executable_name") or e.get("unique_identifier") or ""
        painter.text(P(x + 19, rect.min.y + 30), egui.Align2.LEFT_TOP, elide(painter, sub, mono(12), name_w), mono(12), MUTED)

        # Spoken forms as chips.
        cx = x + forms_off
        forms = e.get("spoken_forms") or []
        auto = False
        if not forms:
            # Not stored in the file: show what Talon generated from the name.
            forms = self.live_forms(e)
            auto = True
            if not forms:
                note = "Not registered (disabled)" if excluded else "Auto from name"
                painter.text(P(cx, rect.center().y), egui.Align2.LEFT_CENTER, note, font(13), FAINT)
        chips = [Chip(form, "auto" if auto else "accent") for form in forms]
        widgets.chip_flow(rui, KIT, cx, rect.center().y, x + excl_off - 84, chips, wrap_lines=False)

        toggle = R(x + excl_off - TOGGLE_W, rect.center().y - TOGGLE_H / 2, TOGGLE_W, TOGGLE_H)
        # Its own interactive area (on top of the row), so it is its own UIA element.
        if widgets.toggle(rui, KIT, toggle, not excluded, name=f"Enabled: {name}", key="toggle:" + uid, hit_rect=toggle.expand(6)):
            e["exclude"] = not excluded
            return True
        return False

    async def draw_detail(self, ui, painter, rect):
        widgets.card(painter, KIT, rect)
        inner = rect.shrink(22)
        if self.selected is None or self.selected >= len(self.entries):
            painter.text(inner.left_top(), egui.Align2.LEFT_TOP, "Select an application to edit it.", font(14), MUTED)
            return
        e = self.entries[self.selected]
        x, y, w = inner.min.x, inner.min.y, inner.width()

        widgets.section_label(painter, KIT, x, y, "Store app" if not e.get("path") else "Desktop app")
        if self.button(ui, R(x + w - 88, y - 6, 88, 32), "Launch", "outline"):
            self.launch(e)
        y += 30
        name = e.get("display_name") or "?"
        painter.text(P(x, y), egui.Align2.LEFT_TOP, elide(painter, name, font(21), w), font(21), TEXT)
        y += 32
        y = wrap(painter, x, y, w, "Display name comes from Windows and is regenerated on refresh.", font(13), MUTED)
        y += 22

        painter.text(P(x, y), egui.Align2.LEFT_TOP, "Spoken forms", font(14), TEXT)
        y += 26
        forms = list(e.get("spoken_forms") or [])
        if not forms:
            live = self.live_forms(e)
            if live:
                y = wrap(painter, x, y, w, "From the name (add your own to replace these):", font(13), MUTED)
                y += 6
                _, y = widgets.chip_flow(
                    ui, KIT, x, y, x + w, [Chip(form, "auto") for form in live], height=26, size=13, pad=10
                )
                y += 34
            elif e.get("exclude"):
                y = wrap(painter, x, y, w, "None registered: the app is disabled.", font(13), MUTED)
                y += 8
            else:
                y = wrap(painter, x, y, w, f"None yet — Talon derives them from “{name}”.", font(13), MUTED)
                y += 8
        clashes = []
        chips = []
        for form in forms:
            owner = self.form_owner(form, e)
            if owner:
                clashes.append(f"“{form}” is also used by {owner}.")
            chips.append(Chip(form, "warn" if owner else "accent", remove_key="remove-form:" + form))
        if chips:
            removed, y = widgets.chip_flow(ui, KIT, x, y, x + w, chips, height=30, size=13.5, pad=12)
            if removed is not None:
                forms.pop(removed)
                e["spoken_forms"] = forms or None
        if forms:
            y += 38
        for note in clashes:
            y = wrap(painter, x, y, w, note, font(13), WARN_TEXT)
            y += 4
        if clashes:
            y += 6

        add = R(x + w - 72, y, 72, 38)
        out = await widgets.text_field(
            ui, KIT, R(x, y, w - 72 - 8, 38), self.new_form, hint="e.g. code, vs code, editor", name="Add spoken forms"
        )
        async with ui.input() as inp:
            enter = inp.key_pressed(egui.Key.Enter)
        if self.button(ui, add, "+  Add") or (enter and out.response.lost_focus()):
            self.add_form(e)
            out.response.request_focus()
        y += 38 + 8
        if self.form_notice:
            y = wrap(painter, x, y, w, self.form_notice, font(13), WARN_TEXT)
        y += 20

        # Exclude toggle.
        excluded = bool(e.get("exclude"))
        if widgets.setting_row(ui, KIT, x, y, w, "Enabled", "When off, “launch” commands leave it out.", not excluded, key="detail-enabled"):
            e["exclude"] = not excluded
        y += 56

        painter.hline(x, x + w, y, egui.Stroke(1.0, DIVIDER))
        y += 16
        painter.text(P(x, y), egui.Align2.LEFT_TOP, "Details", font(14), TEXT)
        y += 28
        rows = [("Executable", e.get("executable_name")), ("Path", e.get("path")), ("Identifier", e.get("unique_identifier"))]
        widgets.key_values(painter, KIT, x, y, w, [(label, value or "null") for label, value in rows])

    async def draw_menu(self, ui, painter, full):
        """The kit's menu: numbered items (digits pick them), arrow keys, Enter, Escape."""
        menu = self.menu
        if menu is None or menu.i >= len(self.entries):
            self.menu = None
            return
        e = self.entries[menu.i]
        items = [
            kit_menu.MenuItem("Launch", lambda: self.launch(e)),
            kit_menu.MenuItem("Disable" if not e.get("exclude") else "Enable", lambda: e.__setitem__("exclude", not e.get("exclude"))),
        ]
        width, height = 180.0, kit_menu.height(items)
        x = min(menu.pos.x, full.max.x - width - 8)
        y = min(menu.pos.y, full.max.y - height - 8)
        box = R(x, y, width, height)
        async with ui.input() as inp:
            escape = inp.key_pressed(egui.Key.Escape)
            clicked = inp.pointer.primary_clicked() or inp.pointer.secondary_clicked()
            pointer = inp.pointer.latest_pos()
            moving = inp.pointer.is_moving()
            typing = ui.ctx().wants_keyboard_input()
            keys = [] if typing else [k for k in MENU_KEYS if inp.key_pressed(getattr(egui.Key, k))]
            digits = [] if typing else [n for n, key in DIGIT_KEYS if inp.key_pressed(key)]
        chosen = kit_menu.draw_menu(ui, KIT, menu, items, box, hover=moving, pointer=pointer, swallow=True, shadow=True)
        for key in keys:
            result = kit_menu.navigate(menu, items, key)
            if isinstance(result, kit_menu.MenuItem):
                chosen = result
        for n in digits:
            chosen = kit_menu.item_number(items, n) or chosen
        if chosen is not None and chosen.enabled:
            self.menu = None
            chosen.action()
        elif menu.fresh:
            # The click that opened it.
            menu.fresh = False
        elif escape or (clicked and pointer is not None and not box.contains(pointer)):
            self.menu = None
        if keys or digits:
            self.window.refresh()
