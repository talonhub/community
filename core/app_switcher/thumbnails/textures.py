"""Icon textures for cells and jump-list rows (the kit's IconTextures; egui's thread only)."""

import threading
import egui
from ..windows import app_icons, jump_lists
from .model import Entry


class TexturesMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    def _texture(self, ui: egui.Ui, entry: Entry) -> "egui.TextureHandle | None":
        """The entry's icon as an egui texture, created on first use."""
        icon = entry.icon
        return self.textures.get(ui, (entry.hwnd, icon.width), icon) if icon is not None else None

    def _menu_icon(self, ui: egui.Ui, icon_of) -> "egui.TextureHandle | None":
        """A jump list entry's icon as a texture; fetched in the background the first
        time (the menu redraws when it arrives), None until then or if it has none."""
        entry, app_id = icon_of
        key = ("jump", entry.kind, entry.path or hash(entry.data))
        with self.lock:
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
                    found = app_icons.fetch(source, 32, thumbnail=picture) if source else None
                except Exception:
                    found = None
                with self.lock:
                    self.jump_icons[key] = found
                self.refresh()

            threading.Thread(target=fetch, name="jump list icon", daemon=True).start()
            return None
        return self.textures.get(ui, key, icon)
