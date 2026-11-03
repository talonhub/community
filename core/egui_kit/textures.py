"""Icon textures: RGBA icons turned into egui textures, cached per window.

Every egui window has its own context, so textures can't be shared between windows;
the pixels can (see app_switcher/windows/app_icons.py). Textures must be created and
dropped on the window's egui thread, i.e. inside its render: `get` creates them and
`drop_where` / `trim` drop them. A window made anew (reopened after its title bar's X)
has a new context: `clear()` the cache then.

An icon is anything with `width`, `height` and straight (unmultiplied) `rgba` bytes.
"""

import threading
from collections import OrderedDict

import egui


class IconTextures:
    def __init__(self, prefix: str, limit: int = 600):
        # Texture names: "<prefix>_<n>".
        self.prefix = prefix
        self.limit = limit
        self.lock = threading.Lock()
        # key -> (texture, the icon it was made from)
        self._textures: OrderedDict = OrderedDict()
        self._count = 0

    def get(self, ui: egui.Ui, key, icon) -> "egui.TextureHandle | None":
        """The texture for `icon` under `key`, made on first use (or again when a
        different icon arrives for the key). None for no icon."""
        if icon is None:
            return None
        with self.lock:
            found = self._textures.get(key)
            if found is not None and found[1] is icon:
                self._textures.move_to_end(key)
                return found[0]
            self._count += 1
            name = f"{self.prefix}_{self._count}"
        image = egui.ColorImage.from_rgba_unmultiplied(icon.width, icon.height, icon.rgba)
        texture = ui.ctx().load_texture(name, image, egui.TextureOptions.linear())
        with self.lock:
            self._textures[key] = (texture, icon)
            self._textures.move_to_end(key)
            dropped = self._trim()
        del dropped
        return texture

    def keys(self) -> list:
        with self.lock:
            return list(self._textures)

    def drop_where(self, stale) -> int:
        """Drop the textures whose key `stale(key)` says (egui thread). Returns how many."""
        with self.lock:
            keys = [key for key in self._textures if stale(key)]
            dropped = [self._textures.pop(key) for key in keys]
        n = len(dropped)
        del dropped
        return n

    def clear(self):
        """Forget every texture (a new egui context, or shutting down)."""
        with self.lock:
            self._textures.clear()

    def __len__(self) -> int:
        with self.lock:
            return len(self._textures)

    def _trim(self) -> list:
        """Drop the least recently used beyond the limit (lock held); returns them so
        the caller releases them outside the lock."""
        dropped = []
        while len(self._textures) > self.limit:
            dropped.append(self._textures.popitem(last=False))
        return dropped
