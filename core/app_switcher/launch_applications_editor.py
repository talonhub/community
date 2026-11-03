"""An egui editor for this machine's launch_applications.json (prototype).

Edits `exclude` and `spoken_forms` live: each change is saved a moment later (every other
key is written back as it was read), and changes made to the file elsewhere load in.
app_switcher.py picks up each save through its resource.watch.

Say "launch applications editor" to open it.
"""

import json
import os
import platform
import sys
import threading
import time
from collections import Counter

import egui
from talon import Module, actions, app, cron, registry, ui
from talon.egui import Window

# While prototyping: open the editor on every (re)load so render errors show in the log.
DEV_SHOW_ON_LOAD = False

JSON_PATH = os.path.normcase(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        app.platform,
        platform.node(),
        "launch_applications.json",
    )
)
HOST = platform.node()
WINDOW_TITLE = "Launch applications"
NO_EXE = "(no executable)"

FILTERS = [
    ("all", "All"),
    ("enabled", "Enabled"),
    ("disabled", "Disabled"),
    ("forms", "Custom Spoken Form"),
]


def rgb(hex_color: str) -> egui.Color32:
    h = hex_color.lstrip("#")
    return egui.Color32.from_rgb(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# The proposal's palette.
BG = rgb("#F4F5F7")
SURFACE = rgb("#FFFFFF")
BORDER = rgb("#E1E4E9")
DIVIDER = rgb("#EEF0F3")
HEADER_BG = rgb("#F8F9FA")
TEXT = rgb("#1B1F24")
MUTED = rgb("#5B6470")
LABEL = rgb("#4A525D")
FAINT = rgb("#6B737E")
ACCENT = rgb("#2F5BD3")
ACCENT_DISABLED = rgb("#A9B4CC")
SELECTED_ROW = rgb("#EEF3FE")
SELECTED_FILTER = rgb("#E3E9F7")
HOVER = rgb("#F3F5F8")
CHIP_BG = rgb("#EAF0FD")
CHIP_TEXT = rgb("#1E3F9E")
TRACK_OFF = rgb("#C3C9D2")
WARN_BG = rgb("#FFF3E3")
WARN_TEXT = rgb("#8A4B00")
WARN_DOT = rgb("#C76A00")
INPUT_BORDER = rgb("#CDD2DA")
WHITE = rgb("#FFFFFF")
AUTO_BG = rgb("#F4F5F7")
AUTO_BORDER = rgb("#D5D9E0")

HEADER_H = 44.0
PAD = 20.0
LEFT_W = 260.0
RIGHT_W = 380.0
ROW_H = 52.0
LIST_HEADER_H = 52.0
COLUMN_HEADER_H = 34.0
TOGGLE_W, TOGGLE_H = 40.0, 22.0

mod = Module()


def snapshot(entry: dict) -> tuple:
    forms = entry.get("spoken_forms")
    return (bool(entry.get("exclude")), tuple(forms) if forms else None)


def font(size: float) -> egui.FontId:
    return egui.FontId.proportional(size)


def mono(size: float) -> egui.FontId:
    return egui.FontId.monospace(size)


def P(x: float, y: float) -> egui.Pos2:
    return egui.Pos2(x, y)


def R(x: float, y: float, w: float, h: float) -> egui.Rect:
    return egui.Rect.from_min_size(egui.Pos2(x, y), egui.Vec2(w, h))


def text_width(painter: egui.Painter, text: str, font_id: egui.FontId) -> float:
    return painter.layout_no_wrap(text, font_id, TEXT).size().x


def elide(painter: egui.Painter, text: str, font_id: egui.FontId, width: float) -> str:
    if width <= 0:
        return ""
    if text_width(painter, text, font_id) <= width:
        return text
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if text_width(painter, text[:mid] + "…", font_id) <= width:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + "…"


def card(painter: egui.Painter, rect: egui.Rect):
    painter.rect(rect, 12, SURFACE, egui.Stroke(1.0, BORDER), egui.StrokeKind.Inside)


def describe(resp: egui.Response, typ, label: str, enabled: bool = True, selected: bool | None = None):
    """Give a custom-painted control an accessibility node (role, name, state), so
    UI Automation clients such as windows-hinting can find and click it."""
    try:
        if selected is None:
            info = egui.WidgetInfo.labeled(typ, enabled, label)
        else:
            info = egui.WidgetInfo.selected(typ, enabled, selected, label)
        resp.widget_info(info)
    except Exception as e:  # never let accessibility break drawing
        print(f"launch_applications_editor: widget_info failed: {e!r}")


def name_text_edit(resp: egui.Response, label: str, value: str, hint: str):
    """Text fields drawn without a frame or visible label still need a UIA name."""
    try:
        info = egui.WidgetInfo.text_edit(True, value, value, hint)
        info.label = label
        resp.widget_info(info)
    except Exception as e:
        print(f"launch_applications_editor: naming a text field failed: {e!r}")


def hit(ui: egui.Ui, rect: egui.Rect, key: str) -> egui.Response:
    """A clickable area with a stable id (so its accessibility node is stable across
    frames) that doesn't move the layout cursor."""
    return ui.interact(rect, egui.Id(f"lae:{key}"), egui.Sense.click())


def paint_toggle(painter: egui.Painter, rect: egui.Rect, on: bool, enabled: bool = True):
    track = (ACCENT if on else TRACK_OFF) if enabled else DIVIDER
    painter.rect_filled(rect, rect.height() / 2, track)
    r = rect.height() / 2 - 3
    cx = rect.max.x - r - 3 if on else rect.min.x + r + 3
    painter.circle_filled(P(cx, rect.center().y), r, WHITE)


def paint_button(painter: egui.Painter, rect: egui.Rect, label: str, kind: str, hovered: bool, enabled: bool = True):
    """kind: "primary", "secondary" or "outline"."""
    if kind == "primary":
        fill = (rgb("#2850BC") if hovered else ACCENT) if enabled else ACCENT_DISABLED
        painter.rect_filled(rect, 8, fill)
        color = WHITE
    else:
        fill = HOVER if hovered and enabled else SURFACE
        stroke = ACCENT if kind == "outline" and enabled else INPUT_BORDER
        painter.rect(rect, 8, fill, egui.Stroke(1.0, stroke), egui.StrokeKind.Inside)
        color = (ACCENT if kind == "outline" else TEXT) if enabled else FAINT
    painter.text(rect.center(), egui.Align2.CENTER_CENTER, label, font(14), color)


class Editor:
    def __init__(self):
        self.lock = threading.RLock()
        self.entries: list[dict] = []
        self.baseline: dict[int, tuple] = {}
        self.mtime = 0.0
        self.message = ""
        self.selected: int | None = None
        self.filter = "enabled"
        self.exe_filter: str | None = None
        self.query = egui.Mutable("")
        self.new_form = egui.Mutable("")
        self.showing = False
        self.visuals_set = False
        # Edits save themselves a moment after they're made, and changes made to the
        # file elsewhere (app_switcher adding new apps, a text editor) load in.
        self.save_job = None
        self.saved_at: float | None = None
        # Spoken form -> unique_identifier, from app_switcher's live user.launch list
        # (which includes the forms it generates from display names).
        self.launch_map: dict[str, str] = {}
        # The same list turned around: unique_identifier (lower case) -> its forms.
        self.auto_forms: dict[str, list[str]] = {}
        self.form_notice = ""
        # The right-click menu: {"i": entry index, "pos": egui.Pos2} while open.
        self.menu: dict | None = None
        self.poll_job = cron.interval("1s", self.poll)

        # unique_identifiers (lower case), for an exact-identifier search.
        self.identifiers: set[str] = set()
        # A unique title while placing the window, so the lookup can't pick up a window a
        # previous load left behind; it goes back to WINDOW_TITLE once placed.
        self.instance_title = f"{WINDOW_TITLE} [{id(self):x}]"
        # The native window, once placed. The title bar's X destroys it, and a closed
        # talon.egui.Window never shows again, so show() makes a new one then.
        self.hwnd: int | None = None
        self.window = self.make_window()

    def make_window(self) -> Window:
        window = Window()
        window.title = WINDOW_TITLE
        window.decorated = True
        window.resizable = True
        window.draggable = True
        window.autosize = False
        window.toplevel = False
        window.focusable = True
        window.set_content(self.render)
        return window

    # --- file ---

    def load(self):
        try:
            with open(JSON_PATH, "r") as f:
                entries = json.load(f)
            mtime = os.path.getmtime(JSON_PATH)
        except Exception as e:
            with self.lock:
                self.message = f"Couldn't read the file: {e}"
            return
        with self.lock:
            self.entries = entries
            self.identifiers = {(e.get("unique_identifier") or "").lower() for e in entries} - {""}
            self.baseline = {i: snapshot(e) for i, e in enumerate(entries)}
            self.mtime = mtime
            self.message = ""
            if self.selected is None or self.selected >= len(entries):
                self.selected = 0 if entries else None
        self.refresh_launch_map()
        print(f"launch_applications_editor: loaded {len(entries)} entries")
        self.window.refresh()

    def save(self):
        with self.lock:
            try:
                if os.path.getmtime(JSON_PATH) != self.mtime:
                    # Changed elsewhere since it was loaded; take that version.
                    self.message = "The file changed elsewhere; reloaded it. Redo your last change."
                    cron.after("0ms", self._reload_keep_message)
                    return
                text = json.dumps(self.entries, indent=4)
                tmp = JSON_PATH + ".tmp"
                with open(tmp, "w") as f:
                    f.write(text)
                os.replace(tmp, JSON_PATH)
                self.mtime = os.path.getmtime(JSON_PATH)
                self.baseline = {i: snapshot(e) for i, e in enumerate(self.entries)}
                self.saved_at = time.time()
                # app_switcher rebuilds user.launch from the saved file; read it after.
                cron.after("2s", self.refresh_launch_map)
                self.message = ""
            except Exception as e:
                self.message = f"Couldn't save: {e}"
        print("launch_applications_editor: saved" if not self.message else f"launch_applications_editor: {self.message}")
        self.window.refresh()

    def _reload_keep_message(self):
        message = self.message
        self.load()
        self.message = message

    def autosave(self):
        self.save_job = None
        self.save()

    def poll(self):
        """Load the file again when something else changed it."""
        if not self.showing or self.save_job is not None:
            return
        try:
            mtime = os.path.getmtime(JSON_PATH)
        except OSError:
            return
        if mtime != self.mtime and not self.unsaved():
            print("launch_applications_editor: file changed elsewhere, reloading")
            self.load()

    def unsaved(self) -> int:
        return sum(1 for i, e in enumerate(self.entries) if snapshot(e) != self.baseline.get(i))

    # --- showing ---

    def show(self):
        if self.hwnd is not None and not dwm.is_window(self.hwnd):
            # Closed with the title bar's X.
            try:
                self.window.close()
            except Exception:
                pass
            self.window = self.make_window()
            self.hwnd = None
            self.visuals_set = False
        self.load()
        self.showing = True
        # Fit the work area (physical pixels, without the taskbar) of the monitor in use.
        left, top, right, bottom = dwm.foreground_work_area()
        width, height = int((right - left) * 0.92), int((bottom - top) * 0.92)
        x, y = left + ((right - left) - width) // 2, top + ((bottom - top) - height) // 2
        self.target = (x, y, x + width, y + height)
        self.place_tries = 0
        self.window.title = self.instance_title
        self.window.show()
        self.window.focus()
        cron.after("50ms", self.place)

    def show_entry(self, app_id: str) -> bool:
        """Open on one entry, by its unique_identifier: selected, with the list showing
        all entries, searched by that identifier. False if there's no such entry."""
        self.show()
        with self.lock:
            index = next(
                (i for i, e in enumerate(self.entries) if (e.get("unique_identifier") or "").lower() == app_id.lower()), None
            )
            if index is None:
                return False
            self.selected = index
            self.filter = "all"
            self.exe_filter = None
            self.menu = None
            entry = self.entries[index]
            self.query.set(entry.get("unique_identifier") or entry.get("display_name") or "")
            self.new_form.set("")
            self.form_notice = ""
        self.window.refresh()
        return True

    def place(self):
        """Move the native window into place; it only exists once egui has drawn a frame,
        and talon.egui.Window doesn't expose its handle, so look it up by title."""
        hwnd = self.hwnd if self.hwnd is not None and dwm.is_window(self.hwnd) else dwm.find_own_hwnd(self.instance_title)
        if hwnd is None:
            self.place_tries += 1
            if self.place_tries < 40:
                cron.after("50ms", self.place)
            else:
                print("launch_applications_editor: couldn't find the window to place it")
                self.window.title = WINDOW_TITLE
            return
        self.hwnd = hwnd
        dwm.move_hwnd(hwnd, self.target)
        self.window.title = WINDOW_TITLE
        # egui only lays out again on its next frame; ask for a few after the move.
        for delay in ("0ms", "100ms", "300ms", "600ms"):
            cron.after(delay, self.window.refresh)

    def hide(self):
        self.showing = False
        self.window.hide()

    def shutdown(self):
        self.showing = False
        if getattr(self, "poll_job", None) is not None:
            cron.cancel(self.poll_job)
            self.poll_job = None
        if getattr(self, "save_job", None) is not None:
            cron.cancel(self.save_job)
            self.save_job = None
            self.save()
        self.window.close()

    # --- model (lock held) ---

    # The search, the Show filter and the executable filter combine (AND). Each side's
    # counts are what picking that row would show, given the other two.

    def show_test(self, key: str, i: int, e: dict) -> bool:
        if key == "enabled":
            return not e.get("exclude")
        if key == "disabled":
            return bool(e.get("exclude"))
        if key == "forms":
            return bool(e.get("spoken_forms"))
        return True

    def exe_test(self, exe: str | None, e: dict) -> bool:
        return exe is None or (e.get("executable_name") or NO_EXE) == exe

    def query_test(self, query: str, e: dict) -> bool:
        if not query:
            return True
        uid = (e.get("unique_identifier") or "").lower()
        if query in self.identifiers:
            # An identifier (as "Edit launch entry" searches) names exactly one app.
            return uid == query
        hay = " ".join(
            [e.get("display_name") or "", e.get("executable_name") or "", uid, *(e.get("spoken_forms") or [])]
        ).lower()
        return query in hay

    def matches(self, i: int, e: dict, query: str) -> bool:
        return self.show_test(self.filter, i, e) and self.exe_test(self.exe_filter, e) and self.query_test(query, e)

    def counts(self, query: str) -> dict[str, int]:
        scoped = [(i, e) for i, e in enumerate(self.entries) if self.exe_test(self.exe_filter, e) and self.query_test(query, e)]
        return {key: sum(1 for i, e in scoped if self.show_test(key, i, e)) for key, _ in FILTERS}

    def exe_counts(self, query: str) -> list[tuple[str, int]]:
        """Executables with more than one entry in the file (a stable list), each with
        how many entries it would show given the Show filter and search."""
        everywhere = Counter(e.get("executable_name") or NO_EXE for e in self.entries)
        scoped = Counter(
            e.get("executable_name") or NO_EXE
            for i, e in enumerate(self.entries)
            if self.show_test(self.filter, i, e) and self.query_test(query, e)
        )
        return [(exe, scoped.get(exe, 0)) for exe, n in everywhere.most_common() if n >= 2]

    # --- drawing ---

    async def render(self, ui: egui.Ui) -> None:
        ctx = ui.ctx()
        if not self.visuals_set:
            ctx.set_visuals(egui.Visuals.light())
            try:
                ctx.enable_accesskit()
            except Exception as e:
                print(f"launch_applications_editor: enable_accesskit failed: {e!r}")
            self.visuals_set = True
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

    def button(self, ui, painter, rect, label, kind="secondary", enabled=True, key=None) -> bool:
        resp = hit(ui, rect, "button:" + (key or label))
        describe(resp, egui.WidgetType.Button, label.replace("+", "").strip(), enabled)
        paint_button(painter, rect, label, kind, resp.hovered(), enabled)
        return enabled and resp.clicked()

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
            label, dot = "Saved " + time.strftime("%H:%M:%S", time.localtime(self.saved_at)) + " · changes apply immediately", rgb("#2E8B57")
        else:
            label, dot = "Changes save and apply immediately", rgb("#2E8B57")
        r = painter.text(right, egui.Align2.RIGHT_CENTER, label, font(13), MUTED)
        painter.circle_filled(P(r.min.x - 10, rect.center().y), 4, dot)

    def section_label(self, painter, x, y, text):
        painter.text(P(x, y), egui.Align2.LEFT_TOP, text.upper(), font(11.5), LABEL)

    def filter_row(self, ui, painter, rect, label, count, on) -> bool:
        resp = hit(ui, rect, "filter:" + label)
        describe(resp, egui.WidgetType.SelectableLabel, f"{label} ({count})", True, on)
        if on:
            painter.rect_filled(rect, 8, SELECTED_FILTER)
        elif resp.hovered():
            painter.rect_filled(rect, 8, HOVER)
        width = rect.width() - 24 - 40
        painter.text(P(rect.min.x + 12, rect.center().y), egui.Align2.LEFT_CENTER,
                     elide(painter, label, font(14), width), font(14), TEXT)
        painter.text(P(rect.max.x - 12, rect.center().y), egui.Align2.RIGHT_CENTER, str(count), font(13), MUTED)
        return resp.clicked()

    async def draw_sidebar(self, ui, painter, rect, counts):
        x, y, w = rect.min.x, rect.min.y, rect.width()
        self.section_label(painter, x, y, "Search")
        y += 22
        box = R(x, y, w, 38)
        painter.rect(box, 8, SURFACE, egui.Stroke(1.0, INPUT_BORDER), egui.StrokeKind.Inside)
        async with ui.allocate_new_ui(egui.UiBuilder().max_rect(box.shrink2(egui.Vec2(10, 8)))) as sui:
            qresp = sui.add(
                egui.TextEdit.singleline(self.query)
                .hint_text("Name, exe or spoken form")
                .frame(egui.Frame.none())
                .desired_width(w - 20)
                .font_id(font(14))
                .text_color(TEXT)
            )
        name_text_edit(qresp, "Search", self.query.get(), "Name, exe or spoken form")
        y += 38 + 24

        self.section_label(painter, x, y, "Show")
        y += 22
        for key, label in FILTERS:
            if self.filter_row(ui, painter, R(x, y, w, 36), label, counts[key], self.filter == key):
                self.filter = key
            y += 38
        y += 18

        self.section_label(painter, x, y, "Executable")
        y += 22
        exes = counts["exes"]
        selected = "Any executable" if self.exe_filter is None else self.exe_filter
        box = R(x, y, w, 38)
        async with ui.allocate_new_ui(egui.UiBuilder().max_rect(box)) as cui:
            async with cui.spacing_mut() as spacing:
                spacing.interact_size = egui.Vec2(w, 34)
            async with (
                egui.ComboBox.from_id_salt("lae_exe").selected_text(egui.RichText(selected).size(14))
                .width(w).height(480).show()
            ) as combo:
                if combo.shown:
                    pui = combo.ui
                    if pui.selectable_label(self.exe_filter is None, egui.RichText("Any executable").size(14)).clicked():
                        self.exe_filter = None
                    for exe, n in exes:
                        label = egui.RichText(f"{exe}   {n}").size(14)
                        if pui.selectable_label(self.exe_filter == exe, label).clicked():
                            self.exe_filter = exe
            try:
                resp = combo.response() if callable(combo.response) else combo.response
                describe(resp, egui.WidgetType.ComboBox, f"Executable: {selected}")
            except Exception as e:
                print(f"launch_applications_editor: naming the combo box failed: {e!r}")
        y += 38 + 6
        painter.text(P(x, y), egui.Align2.LEFT_TOP, "Only executables with more than one entry.", font(12), FAINT)

    async def draw_list(self, ui, painter, rect, shown):
        card(painter, rect)
        x0, x1 = rect.min.x, rect.max.x
        y = rect.min.y
        title = dict(FILTERS)[self.filter]
        if self.exe_filter is not None:
            title = self.exe_filter if self.filter == "all" else f"{title} · {self.exe_filter}"
        painter.text(P(x0 + 20, y + LIST_HEADER_H / 2), egui.Align2.LEFT_CENTER, title, font(15.5), TEXT)
        count_label = f"{len(shown)} " + ("entry" if len(shown) == 1 else "entries")
        tx = x0 + 20 + text_width(painter, title, font(15.5)) + 12
        painter.text(P(tx, y + LIST_HEADER_H / 2), egui.Align2.LEFT_CENTER, count_label, font(13), MUTED)

        any_on = any(self.entries[i].get("exclude") for i in shown)
        any_off = any(not self.entries[i].get("exclude") for i in shown)
        bw, bh = 116, 32
        inc = R(x1 - 20 - bw, y + (LIST_HEADER_H - bh) / 2, bw, bh)
        exc = R(inc.min.x - 10 - bw, inc.min.y, bw, bh)
        if self.button(ui, painter, exc, "Disable All", "outline", bool(shown) and any_off):
            for i in shown:
                self.entries[i]["exclude"] = True
        if self.button(ui, painter, inc, "Enable All", "secondary", bool(shown) and any_on):
            for i in shown:
                self.entries[i]["exclude"] = False
        y += LIST_HEADER_H
        painter.hline(x0, x1, y, egui.Stroke(1.0, BORDER))

        # Column header strip.
        strip = R(x0 + 1, y + 0.5, rect.width() - 2, COLUMN_HEADER_H)
        painter.rect_filled(strip, 0, HEADER_BG)
        name_x = x0 + 20
        forms_x = x0 + 20 + (rect.width() - 40 - 84) * 0.52
        excl_x = x1 - 20
        for label, px, align in (
            ("APPLICATION", name_x, egui.Align2.LEFT_CENTER),
            ("SPOKEN FORMS", forms_x, egui.Align2.LEFT_CENTER),
            ("ENABLED", excl_x, egui.Align2.RIGHT_CENTER),
        ):
            painter.text(P(px, strip.center().y), align, label, font(11.5), LABEL)
        y += COLUMN_HEADER_H
        painter.hline(x0, x1, y, egui.Stroke(1.0, BORDER))

        body = egui.Rect.from_min_max(P(x0 + 1, y + 1), P(x1 - 1, rect.max.y - 8))
        if not shown:
            painter.text(body.center(), egui.Align2.CENTER_CENTER, "No entries match. Try another search or filter.",
                         font(14), MUTED)
            return
        async with ui.allocate_new_ui(egui.UiBuilder().max_rect(body)) as lui:
            async with lui.spacing_mut() as spacing:
                spacing.item_spacing = egui.Vec2(0, 0)
            async with (
                egui.ScrollArea.vertical().id_salt("lae_rows").auto_shrink(False).show_rows(ROW_H, len(shown))
            ) as rows:
                rui = rows.ui
                for i in shown[rows.row_start:rows.row_end]:
                    self.draw_row(rui, i, self.entries[i], forms_x - x0, excl_x - x0)

    def draw_row(self, rui, i, e, forms_off, excl_off):
        width = rui.available_width()
        rect, resp = rui.allocate_exact_size(egui.Vec2(width, ROW_H), egui.Sense.click())
        uid = e.get("unique_identifier") or str(i)
        describe(resp, egui.WidgetType.SelectableLabel, e.get("display_name") or "?", True, self.selected == i)
        painter = rui.painter()
        selected = self.selected == i
        if selected:
            painter.rect_filled(rect, 0, SELECTED_ROW)
        elif resp.hovered():
            painter.rect_filled(rect, 0, HOVER)
        painter.hline(rect.min.x, rect.max.x, rect.max.y - 0.5, egui.Stroke(1.0, DIVIDER))

        x = rect.min.x
        name_w = forms_off - 20 - 24
        excluded = bool(e.get("exclude"))
        name = e.get("display_name") or "?"
        name_font = font(14.5)
        dot_room = 0
        name_text = elide(painter, name, name_font, name_w - dot_room)
        nr = painter.text(P(x + 19, rect.min.y + 9), egui.Align2.LEFT_TOP, name_text, name_font,
                          FAINT if excluded else TEXT)
        if excluded:
            painter.hline(nr.min.x, nr.max.x, nr.center().y, egui.Stroke(1.2, FAINT))
        sub = e.get("executable_name") or e.get("unique_identifier") or ""
        painter.text(P(x + 19, rect.min.y + 30), egui.Align2.LEFT_TOP, elide(painter, sub, mono(12), name_w), mono(12), MUTED)

        # Spoken forms as chips.
        cx = x + forms_off
        limit = x + excl_off - 84
        forms = e.get("spoken_forms") or []
        auto = False
        if not forms:
            # Not stored in the file: show what Talon generated from the name.
            forms = self.live_forms(e)
            auto = True
            if not forms:
                note = "Not registered (disabled)" if excluded else "Auto from name"
                painter.text(P(cx, rect.center().y), egui.Align2.LEFT_CENTER, note, font(13), FAINT)
        for form in forms:
            w = text_width(painter, form, font(12.5)) + 16
            if cx + w > limit:
                painter.text(P(cx, rect.center().y), egui.Align2.LEFT_CENTER, "…", font(13), MUTED)
                break
            chip = R(cx, rect.center().y - 11, w, 22)
            if auto:
                painter.rect(chip, 6, AUTO_BG, egui.Stroke(1.0, AUTO_BORDER), egui.StrokeKind.Inside)
                painter.text(chip.center(), egui.Align2.CENTER_CENTER, form, font(12.5), MUTED)
            else:
                painter.rect_filled(chip, 6, CHIP_BG)
                painter.text(chip.center(), egui.Align2.CENTER_CENTER, form, font(12.5), CHIP_TEXT)
            cx += w + 6

        toggle = R(x + excl_off - TOGGLE_W, rect.center().y - TOGGLE_H / 2, TOGGLE_W, TOGGLE_H)
        paint_toggle(painter, toggle, not excluded)
        # Its own interactive area (on top of the row), so it is its own UIA element.
        tresp = hit(rui, toggle.expand(6), "toggle:" + uid)
        describe(tresp, egui.WidgetType.Checkbox, f"Enabled: {e.get('display_name') or '?'}", True, not excluded)
        if tresp.clicked():
            e["exclude"] = not excluded
        elif resp.clicked():
            self.selected = i
            self.new_form.set("")
            self.form_notice = ""
        if resp.secondary_clicked() and resp.interact_pointer_pos is not None:
            self.selected = i
            self.menu = {"i": i, "pos": resp.interact_pointer_pos, "fresh": True}

    async def draw_detail(self, ui, painter, rect):
        card(painter, rect)
        inner = rect.shrink(22)
        if self.selected is None or self.selected >= len(self.entries):
            painter.text(inner.left_top(), egui.Align2.LEFT_TOP, "Select an application to edit it.", font(14), MUTED)
            return
        e = self.entries[self.selected]
        x, y, w = inner.min.x, inner.min.y, inner.width()

        self.section_label(painter, x, y, "Store app" if not e.get("path") else "Desktop app")
        if self.button(ui, painter, R(x + w - 88, y - 6, 88, 32), "Launch", "outline"):
            self.launch(e)
        y += 30
        name = e.get("display_name") or "?"
        painter.text(P(x, y), egui.Align2.LEFT_TOP, elide(painter, name, font(21), w), font(21), TEXT)
        y += 32
        y = self.wrapped(painter, x, y, w, "Display name comes from Windows and is regenerated on refresh.", font(13), MUTED)
        y += 22

        painter.text(P(x, y), egui.Align2.LEFT_TOP, "Spoken forms", font(14), TEXT)
        y += 26
        forms = list(e.get("spoken_forms") or [])
        if not forms:
            live = self.live_forms(e)
            if live:
                y = self.wrapped(painter, x, y, w, "From the name (add your own to replace these):", font(13), MUTED)
                y += 6
                ax = x
                for form in live:
                    cw = text_width(painter, form, font(13)) + 20
                    if ax + cw > x + w and ax > x:
                        ax = x
                        y += 32
                    chip = R(ax, y, cw, 26)
                    painter.rect(chip, 7, AUTO_BG, egui.Stroke(1.0, AUTO_BORDER), egui.StrokeKind.Inside)
                    painter.text(chip.center(), egui.Align2.CENTER_CENTER, form, font(13), MUTED)
                    ax += cw + 6
                y += 34
            elif e.get("exclude"):
                y = self.wrapped(painter, x, y, w, "None registered: the app is disabled.", font(13), MUTED)
                y += 8
            else:
                y = self.wrapped(painter, x, y, w, f"None yet — Talon derives them from “{name}”.", font(13), MUTED)
                y += 8
        cx = x
        clashes = []
        for idx, form in enumerate(forms):
            owner = self.form_owner(form, e)
            if owner:
                clashes.append(f"“{form}” is also used by {owner}.")
            chip_bg, chip_fg = (WARN_BG, WARN_TEXT) if owner else (CHIP_BG, CHIP_TEXT)
            tw = text_width(painter, form, font(13.5))
            chip_w = tw + 12 + 28
            if cx + chip_w > x + w and cx > x:
                cx = x
                y += 36
            chip = R(cx, y, chip_w, 30)
            close = R(chip.max.x - 28, chip.min.y, 28, 30)
            resp = hit(ui, close, "remove-form:" + form)
            describe(resp, egui.WidgetType.Button, f"Remove {form}")
            painter.rect_filled(chip, 8, chip_bg)
            if resp.hovered():
                painter.rect_filled(close, 8, rgb("#FCE3C4") if owner else rgb("#D6E1FB"))
            painter.text(P(chip.min.x + 12, chip.center().y), egui.Align2.LEFT_CENTER, form, font(13.5), chip_fg)
            painter.text(close.center(), egui.Align2.CENTER_CENTER, "✕", font(12), chip_fg)
            if resp.clicked():
                forms.pop(idx)
                e["spoken_forms"] = forms or None
                break
            cx += chip_w + 6
        if forms:
            y += 38
        for note in clashes:
            y = self.wrapped(painter, x, y, w, note, font(13), WARN_TEXT)
            y += 4
        if clashes:
            y += 6

        add = R(x + w - 72, y, 72, 38)
        box = R(x, y, w - 72 - 8, 38)
        painter.rect(box, 8, SURFACE, egui.Stroke(1.0, INPUT_BORDER), egui.StrokeKind.Inside)
        async with ui.allocate_new_ui(egui.UiBuilder().max_rect(box.shrink2(egui.Vec2(10, 8)))) as fui:
            out = (
                egui.TextEdit.singleline(self.new_form)
                .hint_text("e.g. code, vs code, editor")
                .frame(egui.Frame.none())
                .desired_width(box.width() - 20)
                .font_id(font(14))
                .text_color(TEXT)
                .show(fui)
            )
        name_text_edit(out.response, "Add spoken forms", self.new_form.get(), "e.g. code, vs code, editor")
        async with ui.input() as inp:
            enter = inp.key_pressed(egui.Key.Enter)
        if self.button(ui, painter, add, "+  Add") or (enter and out.response.lost_focus()):
            self.add_form(e)
            out.response.request_focus()
        y += 38 + 8
        if self.form_notice:
            y = self.wrapped(painter, x, y, w, self.form_notice, font(13), WARN_TEXT)
        y += 20

        # Exclude toggle.
        painter.text(P(x, y), egui.Align2.LEFT_TOP, "Enabled", font(14), TEXT)
        painter.text(P(x, y + 22), egui.Align2.LEFT_TOP, "When off, “launch” commands leave it out.", font(13), MUTED)
        toggle = R(x + w - TOGGLE_W - 4, y + 8, TOGGLE_W + 4, TOGGLE_H + 4)
        resp = hit(ui, toggle, "detail-enabled")
        excluded = bool(e.get("exclude"))
        describe(resp, egui.WidgetType.Checkbox, "Enabled", True, not excluded)
        paint_toggle(painter, toggle, not excluded)
        if resp.clicked():
            e["exclude"] = not excluded
        y += 56

        painter.hline(x, x + w, y, egui.Stroke(1.0, DIVIDER))
        y += 16
        painter.text(P(x, y), egui.Align2.LEFT_TOP, "Details", font(14), TEXT)
        y += 28
        for label, value in (
            ("Executable", e.get("executable_name")),
            ("Path", e.get("path")),
            ("Identifier", e.get("unique_identifier")),
        ):
            painter.text(P(x, y), egui.Align2.LEFT_TOP, label, font(12.5), MUTED)
            y = self.wrapped(painter, x + 88, y, w - 88, str(value) if value else "null", mono(12), TEXT)
            y += 10

    async def draw_menu(self, ui, painter, full):
        menu = self.menu
        if menu is None or menu["i"] >= len(self.entries):
            self.menu = None
            return
        e = self.entries[menu["i"]]
        items = [
            ("Launch", lambda: self.launch(e)),
            ("Disable" if not e.get("exclude") else "Enable",
             lambda: e.__setitem__("exclude", not e.get("exclude"))),
        ]
        item_h, width = 34.0, 180.0
        pos = menu["pos"]
        x = min(pos.x, full.max.x - width - 8)
        y = min(pos.y, full.max.y - item_h * len(items) - 16)
        box = R(x, y, width, item_h * len(items) + 8)
        painter.rect_filled(box.translate(egui.Vec2(0, 3)).expand(2), 10, rgb("#E4E7EC"))
        painter.rect(box, 8, SURFACE, egui.Stroke(1.0, INPUT_BORDER), egui.StrokeKind.Inside)
        # Swallow clicks on the menu's padding.
        hit(ui, box, "menu")
        chosen = None
        for n, (label, act) in enumerate(items):
            row = R(x + 4, y + 4 + n * item_h, width - 8, item_h)
            resp = hit(ui, row, "menu:" + label)
            describe(resp, egui.WidgetType.Button, label)
            if resp.hovered():
                painter.rect_filled(row, 6, SELECTED_ROW)
            painter.text(P(row.min.x + 12, row.center().y), egui.Align2.LEFT_CENTER, label, font(14), TEXT)
            if resp.clicked():
                chosen = act
        async with ui.input() as inp:
            escape = inp.key_pressed(egui.Key.Escape)
            clicked = inp.pointer.primary_clicked() or inp.pointer.secondary_clicked()
            pointer = inp.pointer.latest_pos()
        if chosen is not None:
            self.menu = None
            chosen()
        elif menu.get("fresh"):
            # The click that opened it.
            menu["fresh"] = False
        elif escape or (clicked and pointer is not None and not box.contains(pointer)):
            self.menu = None

    def launch(self, e: dict):
        """Launch (or focus, if it's running) the app the way "launch" commands do."""
        uid = e.get("unique_identifier")
        if not uid:
            return
        print(f"launch_applications_editor: launching {e.get('display_name')}")

        def run():
            try:
                actions.user.switcher_launch(uid)
            except Exception as ex:
                with self.lock:
                    self.message = f"Couldn't launch {e.get('display_name')}: {ex}"
                self.window.refresh()

        cron.after("0ms", run)

    def wrapped(self, painter, x, y, w, text, font_id, color) -> float:
        galley = painter.layout(text, font_id, color, w)
        painter.galley(P(x, y), galley, color)
        return y + galley.size().y

    def refresh_launch_map(self):
        try:
            merged = {}
            for mapping in registry.lists.get("user.launch", []):
                merged.update(mapping)
        except Exception as e:
            print(f"launch_applications_editor: couldn't read user.launch: {e!r}")
            return
        auto: dict[str, list[str]] = {}
        for form, uid in merged.items():
            auto.setdefault(str(uid).lower(), []).append(str(form))
        with self.lock:
            self.launch_map = {str(k).lower(): str(v) for k, v in merged.items()}
            self.auto_forms = {uid: sorted(forms, key=lambda f: (len(f), f)) for uid, forms in auto.items()}
        print(f"launch_applications_editor: user.launch has {len(merged)} spoken forms for {len(auto)} apps")
        self.window.refresh()

    def live_forms(self, e: dict) -> list[str]:
        """What Talon answers to for this entry right now (from user.launch)."""
        return self.auto_forms.get((e.get("unique_identifier") or "").lower(), [])

    def form_owner(self, form: str, e: dict) -> str | None:
        """Which other entry already answers to `form`, as a label, or None.

        Stored spoken forms are checked in the editor's current (possibly just edited)
        entries of enabled apps. Forms generated
        from display names come from the live user.launch list, skipping apps that
        now have custom forms (those replace the generated ones) or are disabled."""
        for other in self.entries:
            # Disabled apps' spoken forms aren't registered, so they don't clash.
            if other is not e and not other.get("exclude") and form in (other.get("spoken_forms") or []):
                return other.get("display_name") or "?"
        uid = self.launch_map.get(form)
        mine = (e.get("unique_identifier") or "").lower()
        if uid is None or uid.lower() == mine:
            return None
        for other in self.entries:
            if (other.get("unique_identifier") or "").lower() == uid.lower():
                if other.get("spoken_forms") or other.get("exclude"):
                    return None
                return other.get("display_name") or uid
        return uid

    def add_form(self, e: dict):
        """Add the field's spoken forms; several can be entered at once, comma-separated.

        Forms that clash with another app, or that can't be spoken (digits, symbols),
        are left in the field with a note saying why."""
        new = [" ".join(part.split()).lower() for part in self.new_form.get().split(",")]
        new = [form for form in new if form]
        if not new:
            return
        forms = list(e.get("spoken_forms") or [])
        rejected, notes = [], []
        for form in dict.fromkeys(new):
            if form in forms:
                continue
            if not all(ch.isalpha() or ch in " '-" for ch in form):
                rejected.append(form)
                notes.append(f"“{form}” has digits or symbols; spoken forms must be words.")
                continue
            owner = self.form_owner(form, e)
            if owner:
                rejected.append(form)
                notes.append(f"“{form}” is already used by {owner}.")
                continue
            forms.append(form)
        if len(forms) != len(e.get("spoken_forms") or []):
            e["spoken_forms"] = forms
        self.new_form.set(", ".join(rejected))
        self.form_notice = " ".join(notes)

# Talon hot-reloads modules, but the previous module's Editor keeps its window. Keep
# the live one where the next load can close it.
# Every instance ever made is kept, so reloads in quick succession can't orphan one.
_STASH = "_talon_launch_applications_editor_instances"
_OLD_STASH = "_talon_launch_applications_editor_instance"
editor: Editor | None = None


def dump_uia(max_depth: int = 12):
    """Print the editor window's UI Automation tree, as hinting tools see it."""
    pid = os.getpid()
    windows = [w for w in ui.windows() if w.title == WINDOW_TITLE and w.app.pid == pid]
    if not windows:
        print("launch_applications_editor: UIA dump: window not found")
        return
    counts = Counter()
    lines = []

    def walk(el, depth):
        try:
            kind = str(el.control_type)
            name = el.name
        except Exception as e:
            lines.append("  " * depth + f"<error {e!r}>")
            return
        counts[kind] += 1
        if len(lines) < 120:
            lines.append("  " * depth + f"{kind} {name!r}")
        if depth >= max_depth:
            return
        try:
            for child in el.children:
                walk(child, depth + 1)
        except Exception as e:
            lines.append("  " * depth + f"<children error {e!r}>")

    walk(windows[0].element, 0)
    print("launch_applications_editor: UIA dump\n" + "\n".join(lines))
    print(f"launch_applications_editor: UIA counts {dict(counts)}")


def close_stray_windows():
    """Close any editor window a previous load left behind (e.g. two reloads in quick
    succession), the same way its title bar's X would."""
    import ctypes
    from ctypes import wintypes

    pid = os.getpid()
    buf = ctypes.create_unicode_buffer(256)
    found = []

    def callback(hwnd, _lparam):
        owner = wintypes.DWORD()
        dwm.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if owner.value == pid:
            dwm.user32.GetWindowTextW(hwnd, buf, len(buf))
            if buf.value.startswith(WINDOW_TITLE):
                found.append(hwnd)
        return True

    dwm.user32.EnumWindows(dwm.WNDENUMPROC(callback), 0)
    post = ctypes.windll.user32.PostMessageW
    post.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    for hwnd in found:
        post(hwnd, 0x0010, 0, 0)  # WM_CLOSE
    print(f"launch_applications_editor: closed {len(found)} leftover window(s)")


def on_ready():
    global editor
    previous = list(getattr(sys, _STASH, []))
    old = getattr(sys, _OLD_STASH, None)
    if old is not None and old not in previous:
        previous.append(old)
    for instance in previous:
        try:
            instance.shutdown()
        except Exception as e:
            print(f"launch_applications_editor: closing a previous editor failed: {e!r}")
    setattr(sys, _OLD_STASH, None)
    try:
        close_stray_windows()
    except Exception as e:
        print(f"launch_applications_editor: closing leftover windows failed: {e!r}")
    editor = Editor()
    setattr(sys, _STASH, [editor])
    if DEV_SHOW_ON_LOAD:
        editor.show()
        cron.after("4s", dump_uia)


app.register("ready", on_ready)


@mod.action_class
class Actions:
    def launch_applications_editor_show():
        """Show the launch applications editor"""
        if editor:
            editor.show()

    def launch_applications_editor_show_entry(app_id: str):
        """Show the launch applications editor on one entry, by its unique_identifier"""
        if editor and not editor.show_entry(app_id):
            app.notify("Launch applications editor", f"No entry for {app_id}")

    def launch_applications_editor_dump_uia():
        """Print the editor window's UI Automation tree to the Talon log (debugging)"""
        dump_uia()

    def launch_applications_editor_hide():
        """Hide the launch applications editor"""
        if editor:
            editor.hide()
