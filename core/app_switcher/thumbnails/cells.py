"""What each cell shows: a window tile with its live thumbnail (or icon), a list row,
an app tile, a details row; cell names and close-button positions."""

import egui
from ...egui_kit import widgets
from . import dwm_thumbnails as dwm
from ...egui_kit.text import elide_estimate as elide
from ...egui_kit.text import estimate_width
from .config import (
    APP_ICON,
    APP_MODES,
    CHIP,
    CURRENT_DESKTOP,
    DIM_TEXT,
    ICON_POINTS,
    KIT,
    LABEL_HEIGHT,
    NUMBER_WIDTH,
    ROW_ICON,
    RUNNING_DOT,
    TEXT,
    TILE_CLOSE,
    WHITE,
)
from .model import AppGroup, Entry, window_state
from .sizing import fit, to_pixels


class CellsMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    def _draw_app_tile(
        self,
        ui: egui.Ui,
        painter: egui.Painter,
        group: AppGroup,
        i: int,
        tile: egui.Rect,
        badges: list,
        marked: bool = False,
        launcher: bool = False,
        letter: str | None = None,
    ):
        """An apps-view tile: number, large icon, app name, window count, badges. In the
        launcher, running apps get a green dot and their window count even with one, and
        the first installed app of each letter a letter marker."""
        if letter:
            pill = egui.Rect.from_center_size(egui.Pos2(tile.max.x - 18, tile.min.y + 14), egui.Vec2(22, 20))
            painter.rect_filled(pill, 5, CHIP)
            painter.text(pill.center(), egui.Align2.CENTER_CENTER, letter, egui.FontId.proportional(14.0), WHITE)
        number = painter.text(
            egui.Pos2(tile.min.x + 8, tile.min.y + 12),
            egui.Align2.LEFT_CENTER,
            str(i + 1),
            egui.FontId.proportional(14.0),
            DIM_TEXT,
        )
        if marked:
            widgets.paint_check(painter, KIT, egui.Pos2(number.max.x + 12, tile.min.y + 12))
        count = len(group.windows)
        if count > 1 or (launcher and count):
            text = painter.text(
                egui.Pos2(tile.max.x - 12 - TILE_CLOSE, tile.min.y + 12),
                egui.Align2.RIGHT_CENTER,
                f"{count} window{'s' if count > 1 else ''}",
                egui.FontId.proportional(12.0),
                DIM_TEXT,
            )
            if launcher:
                painter.circle_filled(egui.Pos2(text.min.x - 8, tile.min.y + 12), 4.0, RUNNING_DOT)
        size = min(APP_ICON, tile.width() - 24, tile.height() - 72)
        center_x = tile.center().x
        top = tile.min.y + 24
        texture = self._texture(ui, group)
        if texture is not None and size > 0:
            rect = egui.Rect.from_min_size(egui.Pos2(center_x - size / 2, top), egui.Vec2(size, size))
            uv = egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0))
            painter.image(texture.id(), rect, uv, WHITE if not group.minimized else DIM_TEXT)
        painter.text(
            egui.Pos2(center_x, top + max(size, 0) + 14),
            egui.Align2.CENTER_CENTER,
            elide(group.title, tile.width() - 12, 14.0),
            egui.FontId.proportional(14.0),
            TEXT,
        )
        if badges:
            # Centered along the bottom.
            width = sum(estimate_width(text, 12.0) + 18 for text, _color in badges)
            widgets.badges(painter, KIT, badges, center_x + width / 2, tile.max.y - 14)

    def _draw_detail_row(self, ui, painter, entry, i, row, columns, letter, current_desktop, show_desktops, marked):
        """A row of the launcher's details table."""
        center_y = row.center().y
        font = egui.FontId.proportional(13.0)
        windows = getattr(entry, "windows", [])
        for column in columns:
            key = column.key
            left = row.min.x + column.x + 6
            width = column.w - 12
            if key == "number":
                painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, str(i + 1), egui.FontId.proportional(14.0), DIM_TEXT)
                if marked:
                    widgets.paint_check(painter, KIT, egui.Pos2(left + 26, center_y), radius=6.0)
            elif key == "icon":
                texture = self._texture(ui, entry)
                if texture is not None:
                    rect = egui.Rect.from_min_size(egui.Pos2(left - 4, center_y - 11), egui.Vec2(22, 22))
                    uv = egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0))
                    painter.image(texture.id(), rect, uv, WHITE)
            elif key == "name":
                # (No letter pill here: the A-Z index on the right shows where you are.)
                # A window row's Application is its app; the launcher's rows are apps.
                name = entry.app_name if isinstance(entry, Entry) else entry.title
                painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, elide(name, width, 14.0), egui.FontId.proportional(14.0), TEXT)
            elif key == "title":
                painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, elide(entry.title, width, 14.0), egui.FontId.proportional(14.0), TEXT)
            elif key == "state":
                state = window_state(entry)
                painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, state, font, DIM_TEXT if state == "Normal" else TEXT)
            elif key == "running":
                if windows:
                    painter.circle_filled(egui.Pos2(left + 4, center_y), 4.0, RUNNING_DOT)
                    painter.text(
                        egui.Pos2(left + 14, center_y), egui.Align2.LEFT_CENTER, f"{len(windows)} window{'s' if len(windows) > 1 else ''}", font, TEXT
                    )
            elif key == "spoken":
                forms = self._spoken_forms(entry)
                if forms:
                    painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, elide(", ".join(forms[:2]), width, 13.0), font, TEXT)
            elif key == "desktop":
                numbers = getattr(entry, "desktop_numbers", None) or []
                if isinstance(entry, Entry):
                    numbers = [entry.desktop_number] if entry.desktop_number else []
                    windows = [entry]
                if numbers and show_desktops:
                    here = current_desktop is not None and any(w.desktop_key == current_desktop for w in windows)
                    painter.text(
                        egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, ", ".join(str(n) for n in numbers), font, CURRENT_DESKTOP if here else TEXT
                    )
                elif numbers:
                    painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, ", ".join(str(n) for n in numbers), font, DIM_TEXT)
            elif key == "screen":
                numbers = getattr(entry, "screen_numbers", None) or []
                if isinstance(entry, Entry):
                    numbers = [entry.screen_number] if entry.screen_number else []
                if numbers:
                    painter.text(egui.Pos2(left, center_y), egui.Align2.LEFT_CENTER, ", ".join(str(n) for n in numbers), font, TEXT)

    def _draw_tile(
        self,
        ui: egui.Ui,
        painter: egui.Painter,
        entry: Entry,
        i: int,
        tile: egui.Rect,
        thumbnail: "dwm.Thumbnail | None",
        view_px: tuple[int, int, int, int],
        ppp: float,
        badges: list,
        cover: tuple[int, int, int, int] | None = None,
        marked: bool = False,
    ):
        """A grid tile: the live thumbnail (or icon) with the number and title below;
        a marked one has a check before the number (DWM draws over the thumbnail area)."""
        label_y = tile.max.y - LABEL_HEIGHT / 2 - 2
        # Room for the close button at the end.
        right = widgets.badges(painter, KIT, badges, tile.max.x - 10 - TILE_CLOSE, label_y)
        left = tile.min.x + 6
        if marked:
            widgets.paint_check(painter, KIT, egui.Pos2(left + 7, label_y))
            left += 18
        label = f"{i + 1}  {entry.title}"
        painter.text(
            egui.Pos2(left, label_y),
            egui.Align2.LEFT_CENTER,
            elide(label, right - left - 6, 13.0),
            egui.FontId.proportional(13.0),
            TEXT,
        )

        # The thumbnail area; shown underneath DWM's thumbnail, so it only shows
        # through while the thumbnail is not registered or has no content.
        thumb = egui.Rect.from_min_max(
            egui.Pos2(tile.min.x + 6, tile.min.y + 6),
            egui.Pos2(tile.max.x - 6, tile.max.y - LABEL_HEIGHT - 4),
        )
        if entry.iconic:
            self._draw_icon(ui, painter, entry, thumb)
        else:
            painter.text(
                thumb.center(),
                egui.Align2.CENTER_CENTER,
                elide(entry.app_name, thumb.width(), 14.0),
                egui.FontId.proportional(14.0),
                DIM_TEXT,
            )

        if thumbnail is not None:
            box = to_pixels(thumb, ppp)
            dest = fit(*thumbnail.source_size(), box)
            if cover is not None and dwm.intersect(dest, cover):
                # Under the menu: DWM would draw on top of it. Back once the menu closes.
                thumbnail.hide()
            else:
                # Clipped to the viewport: DWM would otherwise draw over the header.
                thumbnail.place(dest, view_px)

    def _draw_row(
        self, ui: egui.Ui, painter: egui.Painter, entry: Entry, i: int, row: egui.Rect, badges: list, marked: bool = False
    ):
        """A list row: number, small icon, window title and, dimmer, the app name; a
        marked row has a check on the icon's corner."""
        center_y = row.center().y
        x = row.min.x + 10
        painter.text(
            egui.Pos2(x, center_y),
            egui.Align2.LEFT_CENTER,
            str(i + 1),
            egui.FontId.proportional(14.0),
            DIM_TEXT,
        )
        x += NUMBER_WIDTH
        texture = self._texture(ui, entry)
        if texture is not None:
            rect = egui.Rect.from_min_size(
                egui.Pos2(x, center_y - ROW_ICON / 2), egui.Vec2(ROW_ICON, ROW_ICON)
            )
            uv = egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0))
            painter.image(texture.id(), rect, uv, WHITE)
        if marked:
            widgets.paint_check(painter, KIT, egui.Pos2(x + ROW_ICON - 2, center_y + ROW_ICON / 2 - 4), radius=6.0)
        x += ROW_ICON + 10

        app_label = entry.app_label()
        # Room for the close button at the end.
        right = widgets.badges(painter, KIT, badges, row.max.x - 14 - TILE_CLOSE, center_y)
        app_w = min(estimate_width(app_label, 13.0), row.width() * 0.35)
        painter.text(
            egui.Pos2(right, center_y),
            egui.Align2.RIGHT_CENTER,
            elide(app_label, app_w, 13.0),
            egui.FontId.proportional(13.0),
            DIM_TEXT,
        )
        painter.text(
            egui.Pos2(x, center_y),
            egui.Align2.LEFT_CENTER,
            elide(entry.title, right - app_w - 24 - x, 14.0),
            egui.FontId.proportional(14.0),
            TEXT,
        )

    def _tile_name(self, entry, mode: str) -> str:
        """A tile's accessible name: its title, and what it is (apps: windows, or not running)."""
        if mode in APP_MODES:
            count = len(getattr(entry, "windows", []))
            return f"{entry.title}, {count} window{'s' if count != 1 else ''}" if count else f"{entry.title}, not running"
        app_name = getattr(entry, "app_name", "")
        return f"{entry.title} ({app_name})" if app_name and app_name.lower() not in entry.title.lower() else entry.title

    def _tile_close_rect(self, tile: egui.Rect, mode: str, previews: bool) -> egui.Rect:
        """Where a tile's close button goes: the top right of an app tile, the right end
        of a list row, and in the grid the right end of the label row (DWM draws the
        thumbnail over the rest of the tile)."""
        if mode in APP_MODES:
            center = egui.Pos2(tile.max.x - 6 - TILE_CLOSE / 2, tile.min.y + 12)
        elif previews:
            center = egui.Pos2(tile.max.x - 6 - TILE_CLOSE / 2, tile.max.y - LABEL_HEIGHT / 2 - 2)
        else:
            center = egui.Pos2(tile.max.x - 8 - TILE_CLOSE / 2, tile.center().y)
        return egui.Rect.from_center_size(center, egui.Vec2(TILE_CLOSE, TILE_CLOSE))

    def _draw_icon(self, ui: egui.Ui, painter: egui.Painter, entry: Entry, thumb: egui.Rect):
        """The app's icon, large and centered, with "<app> (minimized)" underneath."""
        label_h = 20.0
        size = min(ICON_POINTS, thumb.width(), thumb.height() - label_h - 8)
        center = thumb.center()
        top = center.y - (size + 8 + label_h) / 2
        texture = self._texture(ui, entry)
        if texture is not None and size > 0:
            rect = egui.Rect.from_min_size(
                egui.Pos2(center.x - size / 2, top), egui.Vec2(size, size)
            )
            uv = egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0))
            painter.image(texture.id(), rect, uv, WHITE)
            text_y = top + size + 8 + label_h / 2
        else:
            text_y = center.y
        painter.text(
            egui.Pos2(center.x, text_y),
            egui.Align2.CENTER_CENTER,
            elide(entry.state_label(), thumb.width(), 14.0),
            egui.FontId.proportional(14.0),
            DIM_TEXT,
        )
