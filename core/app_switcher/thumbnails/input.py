"""Keyboard and pointer input: keys while a menu is open, searching by typing, moving
the selection, marks, shortcuts; a resting pointer doesn't move the selection."""

import egui
from .config import KEY_NAMES


class InputMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    def _pointer_moved(self, pos: "egui.Pos2 | None") -> bool:
        """Whether the mouse moved since the switcher opened.

        The window can open under a resting cursor, which egui reports as movement;
        that must not move the selection away from the window the user wants.
        """
        if pos is None:
            return False
        point = (round(pos.x), round(pos.y))
        if self.pointer_origin is None:
            self.pointer_origin = point
        return point != self.pointer_origin

    def _handle_input(self, inp: egui.InputState, cols: int, grid: bool):
        """This frame's typing and keys, as one action to run after render.

        Text goes into the search field. Up/Down move the selection by a row,
        Left/Right only while the field is empty (in the grid), Tab locks "app:<name>"
        in as a chip, Backspace in an empty field removes the chip, Enter focuses the
        selected window, and Escape clears the marks, then the search, then closes the
        switcher. Ctrl+Space marks the selected tile, Shift+arrows mark as they move,
        Ctrl+A marks every tile (with an empty field), Delete closes the marked windows
        or the selected one, and Shift+F10 opens the marked windows' menu.
        """
        ops = []
        events = inp.events()
        # Ctrl+Space marks and Alt+letter jumps; don't also type their characters.
        ctrl_space = any(
            e.kind() == "Key" and e.pressed() and KEY_NAMES.get(repr(e.key())) == "Space" and e.modifiers() is not None and e.modifiers().ctrl
            for e in events
        )
        alt_letter = self.mode == "launcher" and any(
            e.kind() == "Key" and e.pressed() and len(KEY_NAMES.get(repr(e.key())) or "") == 1 and e.modifiers() is not None and e.modifiers().alt
            for e in events
        )
        for event in events:
            kind = event.kind()
            if kind in ("Text", "Paste"):
                text = "".join(ch for ch in event.text() or "" if ch.isprintable())
                if (ctrl_space and not text.strip()) or alt_letter:
                    continue
                if text and self.menu is not None:
                    # Digits pick the numbered menu items; other typing waits.
                    for digit in (ch for ch in text if ch in "123456789"):
                        ops.append(lambda digit=digit: self.pick_menu_item(int(digit)))
                elif text:
                    ops.append(lambda text=text: self.set_query(self.query + text))
                continue
            if kind != "Key" or not event.pressed():
                continue
            key = KEY_NAMES.get(repr(event.key()))
            modifiers = event.modifiers()
            ctrl = bool(modifiers is not None and modifiers.ctrl)
            shift = bool(modifiers is not None and modifiers.shift)
            alt = bool(modifiers is not None and modifiers.alt)
            if self.menu is not None:
                # An open menu takes every key; nothing reaches the tiles or the search.
                if key in ("ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Home", "End", "Enter"):
                    ops.append(lambda key=key: self.menu_key(key))
                elif key == "Escape":
                    ops.append(self.escape)
                continue
            if key == "F10" and shift:
                ops.append(lambda: self.open_marked_menu() if self.marked else self.open_menu(self.selected + 1))
            elif key == "Space" and ctrl:
                ops.append(lambda: self.mark([self.selected + 1]))
            elif key == "D" and ctrl and self.mode == "launcher":
                ops.append(lambda: self.set_launcher_details(None))
            elif key == "D" and ctrl and self.mode == "apps":
                ops.append(lambda: self.set_apps_details(not self.apps_details))
            elif key == "D" and ctrl and self.mode == "windows":
                ops.append(lambda: self.show_window_details(not self.window_details))
            elif key == "A" and ctrl:
                ops.append(lambda: self.query or self.mark_all())
            elif key and len(key) == 1 and alt and self.mode == "launcher":
                # Alt+letter jumps in the launcher (plain letters go to the search).
                ops.append(lambda key=key: self.jump(key))
            elif key in ("PageUp", "PageDown"):
                ops.append(lambda key=key: self.move_row((-1 if key == "PageUp" else 1) * self.page_rows))
            elif key in ("Home", "End"):
                ops.append(lambda key=key: self.move_to_end(key == "End"))
            elif key == "ArrowUp":
                ops.append(lambda shift=shift: self.move_row(-1, mark=shift))
            elif key == "ArrowDown" and self.mode == "apps" and not shift and not self.apps_details:
                ops.append(lambda: self.show_app_windows(self.selected + 1))
            elif key == "ArrowDown":
                ops.append(lambda shift=shift: self.move_row(1, mark=shift))
            elif key in ("ArrowLeft", "ArrowRight") and grid:
                step = -1 if key == "ArrowLeft" else 1
                ops.append(lambda step=step, shift=shift: (self.query and not shift) or self.move_selection(step, mark=shift))
            elif key == "Backspace":
                ops.append(lambda ctrl=ctrl: self.backspace(word=ctrl))
            elif key == "Tab" and ctrl and self.mode in ("windows", "apps"):
                ops.append(self.switch_view)
            elif key == "Tab":
                ops.append(self.lock_tag)
            elif key == "Enter":
                ops.append(lambda: self.select(self.selected + 1))
            elif key == "Escape":
                ops.append(self.escape)
            elif key == "Delete":
                ops.append(lambda: self.close_marked(fallback=True))
        if not ops:
            return None
        return lambda: [op() for op in ops]
