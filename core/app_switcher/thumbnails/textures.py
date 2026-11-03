"""Icon textures for cells and jump-list rows; created and dropped on egui's thread only."""

import threading
import egui
from ..windows import jump_lists
from . import window_icons
from .model import Entry


class TexturesMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    def _texture(self, ui: egui.Ui, entry: Entry) -> "egui.TextureHandle | None":
        """The entry's icon as an egui texture, created on first use."""
        if entry.icon is None:
            return None
        icon = entry.icon
        key = (entry.hwnd, icon.width)
        with self.lock:
            texture = self.textures.get(key)
        if texture is None:
            image = egui.ColorImage.from_rgba_unmultiplied(icon.width, icon.height, icon.rgba)
            texture = ui.ctx().load_texture(
                f"thumbnail_switcher_icon_{entry.hwnd}_{icon.width}",
                image,
                egui.TextureOptions.linear(),
            )
            with self.lock:
                self.textures[key] = texture
        return texture

    def _menu_icon(self, ui: egui.Ui, icon_of) -> "egui.TextureHandle | None":
        """A jump list entry's icon as a texture; fetched in the background the first
        time (the menu redraws when it arrives), None until then or if it has none."""
        entry, app_id = icon_of
        key = ("jump", entry.kind, entry.path or hash(entry.data))
        with self.lock:
            if key in self.textures:
                return self.textures[key]
            icon = self.jump_icons.get(key, False)
            if icon is False:
                self.jump_icons[key] = None
        if icon is False:

            def fetch():
                try:
                    source = jump_lists.icon_source(entry, app_id)
                    # A logo image (Windows Terminal's profiles): its picture, not a
                    # PNG file's icon.
                    picture = entry.kind == "link" and bool(source) and source.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
                    found = window_icons.shell_pixels(source, 32, thumbnail=picture) if source else None
                except Exception:
                    found = None
                with self.lock:
                    self.jump_icons[key] = found
                self.refresh()

            threading.Thread(target=fetch, name="jump list icon", daemon=True).start()
            return None
        if icon is None:
            return None
        image = egui.ColorImage.from_rgba_unmultiplied(icon.width, icon.height, icon.rgba)
        texture = ui.ctx().load_texture(f"thumbnail_switcher_jump_{abs(hash(key))}", image, egui.TextureOptions.linear())
        with self.lock:
            self.textures[key] = texture
        return texture
