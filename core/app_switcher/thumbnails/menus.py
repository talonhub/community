"""The right-click menus and the marked bar's dropdowns: their pages (window, app,
marked windows, snap, layout, desktop, screen, jump lists) and picking from them."""

import sys
from talon import actions, app
from ...egui_kit import menu as kit_menu
from ...egui_kit.menu import MenuItem
from ..windows import virtual_desktops as vd
from ..windows import app_identity
from ..windows import jump_lists
from ..windows import shell_apps
from . import launcher_apps
from .config import JUMP_PAGE_ROWS, LAYOUTS, MENU_SNAPS
from .model import AppGroup, launch_id
from .placement import slot_label


class Menu(kit_menu.MenuState):
    """The right-click menu of one window, or with `marked` of the marked windows
    (`hwnd` None); `page` is "main" or a submenu's name."""

    def __init__(
        self, hwnd: int | None, pos: "egui.Pos2 | None", marked: bool = False, page: str = "main", dropdown: bool = False
    ):
        # A marked bar button's dropdown: just that page's items, under the button, no
        # "< Back"; Left/Right go to the neighbouring button's dropdown.
        super().__init__(page, dropdown)
        self.hwnd = hwnd
        # Where it opens, in points; None: at the window's tile (keyboard, voice).
        self.pos = pos
        self.marked = marked




class MenuMixin:
    """Switcher methods: see the module docstring. Mixed into Switcher, whose state they use."""

    def open_marked_menu(self, pos: "egui.Pos2 | None" = None, page: str = "main"):
        """Open the marked windows' menu (or one of its submenus), if any are marked."""
        if not self.marked_entries():
            return
        with self.lock:
            self.menu = Menu(None, pos, marked=True, page=page)
        self.refresh()
        self._update_tags()

    def open_bar_dropdown(self, page: str):
        """Open a marked bar button's dropdown ("snap", "layout", "desktop", "screen")
        under the button, on its first item: by click and by voice alike."""
        entries = self.marked_entries()
        if not entries:
            return
        if (page == "snap") != (len(entries) == 1) and page in ("snap", "layout"):
            # Snap is for one marked window, a layout for several: the bar shows one.
            app.notify("Thumbnail switcher", "Snap one marked window; say layout for several" if page == "snap" else "Layout needs two or more marked windows; say snap")
            return
        menu = Menu(None, self.bar_anchors.get(page), marked=True, page=page, dropdown=True)
        items = self._marked_menu_items(page, dropdown=True)
        menu.highlight = next((i for i, it in enumerate(items) if it.enabled), 0)
        with self.lock:
            self.menu = menu
        self.refresh()
        self._update_tags()

    def _marked_menu_items(self, page: str, dropdown: bool | None = None) -> list[MenuItem]:
        """The marked windows' menu; a bar dropdown's pages have no "< Back"."""
        if dropdown is None:
            dropdown = bool(self.menu is not None and self.menu.dropdown)
        items = self._marked_menu_page(page)
        return [item for item in items if item.page != "main"] if dropdown else items

    def _marked_menu_page(self, page: str) -> list[MenuItem]:
        entries = self.marked_entries()
        back = MenuItem("<  Back", page="main")
        if page == "snap":
            return [back] + [
                MenuItem(slot_label(slot).capitalize(), lambda slot=slot: self.layout_windows([], [slot], entries=entries[:1]))
                for slot in MENU_SNAPS
            ]
        if page == "layout":
            return [back] + [
                MenuItem(f"{layout.replace('_', ' ').capitalize()} ({len(slots)})", lambda layout=layout: self.layout_marked(layout))
                for layout, slots in LAYOUTS.items()
            ]
        if page == "desktop":
            items = [back]
            for desktop in self.desktops:
                items.append(
                    MenuItem(
                        desktop.label(),
                        lambda n=desktop.number: self.move_marked_to_desktop(number=n),
                        enabled=any(e.desktop_number != desktop.number for e in entries),
                    )
                )
            items.append(MenuItem("New desktop", self.move_marked_to_new_desktop))
            return items
        if page == "screen":
            items = [back]
            for n in range(1, self.screen_count + 1):
                items.append(
                    MenuItem(
                        f"Screen {n}",
                        lambda n=n: self.move_marked_to_screen(screen=n),
                        enabled=any(e.screen_number != n for e in entries),
                    )
                )
            items.append(MenuItem("Next screen", lambda: self.move_marked_to_screen(offset=1)))
            items.append(MenuItem("Previous screen", lambda: self.move_marked_to_screen(offset=-1)))
            return items
        count = len(entries)
        return [
            # A heading, not an item: disabled, so it has no number.
            MenuItem(f"{count} marked window{'s' if count != 1 else ''}"),
            MenuItem("Close all", self.close_marked),
            MenuItem("Minimize all", self.minimize_marked, enabled=any(not e.minimized for e in entries)),
            MenuItem("Restore all", self.restore_marked, enabled=any(e.minimized for e in entries)),
            # One window snaps; several make a layout.
            MenuItem("Snap  >", page="snap") if count == 1 else MenuItem("Layout  >", page="layout"),
            MenuItem("Move to desktop  >", page="desktop", enabled=vd.available()),
            *([MenuItem("Move to screen  >", page="screen")] if self.screen_count > 1 else []),
            MenuItem("Clear marks", self.clear_marks),
        ]

    def open_menu(self, index: int, pos: "egui.Pos2 | None" = None):
        """Open the menu for tile `index` (1-based), at `pos` or at the tile."""
        with self.lock:
            if not 0 < index <= len(self.entries):
                return
            self.selected = index - 1
            self.menu = Menu(self.entries[index - 1].hwnd, pos)
        self.refresh()
        self._update_tags()

    def close_menu(self):
        with self.lock:
            self.menu = None
        # Now, not on the next frame: the focus comes back here before it hides.
        self._hide_menu_popup()
        self.refresh()
        self._update_tags()

    def menu_back(self):
        """Back from a submenu to the menu's first page (a bar dropdown has none)."""
        with self.lock:
            if self.menu is not None:
                kit_menu.back(self.menu)
        self.refresh()

    def _menu_entry(self, menu: Menu | None) -> "Entry | AppGroup | None":
        """The tile the menu is for; None for the marked windows' menu. Lock held."""
        if menu is None or menu.marked:
            return None
        return next((e for e in self.entries if e.hwnd == menu.hwnd), None)

    def menu_key(self, key: str):
        """Up/Down (Home/End) move the highlight over enabled items, Enter picks, Right
        opens the highlighted submenu, Left goes back from one."""
        with self.lock:
            menu = self.menu
            entry = self._menu_entry(menu)
        if menu is None or (entry is None and not menu.marked):
            return
        items = self._menu_items(entry, menu.page)
        if menu.dropdown and key in ("ArrowLeft", "ArrowRight"):
            # Like a menu bar: the neighbouring button's dropdown.
            pages = list(self.bar_anchors)
            if menu.page in pages and len(pages) > 1:
                step = 1 if key == "ArrowRight" else -1
                self.open_bar_dropdown(pages[(pages.index(menu.page) + step) % len(pages)])
            return
        result = kit_menu.navigate(menu, items, key)
        if result == "back":
            self.menu_back()
        elif result is not None:
            self._pick(menu, result)
        else:
            self.refresh()

    def pick_menu_item(self, number: int):
        """Pick the open menu's item `number`, as numbered on its current page."""
        with self.lock:
            menu = self.menu
            entry = self._menu_entry(menu)
        if menu is None or (entry is None and not menu.marked):
            return
        item = kit_menu.item_number(self._menu_items(entry, menu.page), number)
        if item is not None:
            self._pick(menu, item)

    def _pick(self, menu: Menu, item: MenuItem):
        if not item.enabled:
            return
        if item.page is not None:
            if item.page == "main":
                self.menu_back()
                return
            with self.lock:
                entry = self._menu_entry(menu)
            items = self._menu_items(entry, item.page) if entry is not None or menu.marked else []
            kit_menu.open_page(menu, item.page, items)
            self.refresh()
            return
        if item.keep_open:
            # A row's button (pin, unpin, remove): the page updates in place.
            item.action()
            self.refresh()
            return
        self.close_menu()
        item.action()

    def menu_button(self, kind: str, number: int):
        """Voice for a menu row's button: "pin 3", "unpin 1", "remove 2"."""
        with self.lock:
            menu = self.menu
            entry = self._menu_entry(menu)
        if menu is None or (entry is None and not menu.marked):
            return
        item = kit_menu.item_number(self._menu_items(entry, menu.page), number)
        if item is not None:
            action = next((a for k, a in item.buttons if k == kind), None)
            if action is not None:
                action()
                self.refresh()

    def _menu_items(self, entry: "Entry | None", page: str) -> list[MenuItem]:
        """The menu's items; actions find the window's tile number when they run. With
        no entry, the marked windows' menu."""
        if entry is None:
            return self._marked_menu_items(page)

        def number() -> int:
            with self.lock:
                return next((i + 1 for i, e in enumerate(self.entries) if e.hwnd == entry.hwnd), 0)

        if page.startswith("jump"):
            return self._jump_menu(entry, page)
        # Left out when the app has no jump list.
        jump_items = [MenuItem("Jump list  >", page="jump:0")] if self._has_jump_list(entry) else []
        # Its launch_applications.json entry; none for apps not in the launch list
        # (Console1, portable apps), so the item is left out for those.
        entry_id = self._launch_entry_id(entry)
        edit_items = [MenuItem("Edit launch entry...", lambda: self._edit_launch_entry(entry_id))] if entry_id else []
        if isinstance(entry, launcher_apps.InstalledApp):
            return kit_menu.sections([MenuItem("Launch", lambda: self.launch(number()) if number() else None)], jump_items + edit_items)
        if isinstance(entry, AppGroup):
            if page == "desktop":
                items = [MenuItem("<  Back", page="main")]
                for desktop in self.desktops:
                    items.append(
                        MenuItem(
                            desktop.label(),
                            lambda n=desktop.number: self.move_app_to_desktop(entry, n),
                            enabled=any(w.desktop_number != desktop.number for w in entry.windows),
                        )
                    )
                return items
            if page == "screen":
                return self._screen_menu(number, here=None)
            if page == "snap":
                # Its most recent window, like the window menu's Snap.
                return [MenuItem("<  Back", page="main")] + [
                    MenuItem(slot_label(slot).capitalize(), lambda slot=slot: self.snap_window(number(), slot))
                    for slot in MENU_SNAPS
                ]
            if page == "layout":
                # All its windows, most recent first, like the marked windows' layouts.
                return [MenuItem("<  Back", page="main")] + [
                    MenuItem(
                        f"{layout.replace('_', ' ').capitalize()} ({len(slots)})",
                        lambda layout=layout: self.layout_windows([], LAYOUTS[layout], entries=entry.windows),
                    )
                    for layout, slots in LAYOUTS.items()
                ]
            # The window menu's items for all of the app's windows (one source for the
            # apps strip and the launcher), plus app ones.
            any_minimized = any(w.minimized for w in entry.windows)
            all_minimized = all(w.minimized for w in entry.windows)
            return kit_menu.sections(
                [
                    MenuItem("Focus", lambda: self.select(number()) if number() else None),
                    MenuItem("Launch new window", lambda: self.launch(number()) if number() else None),
                    MenuItem("Show windows", lambda: self.show_app_windows(number()) if number() else None),
                ],
                [
                    MenuItem(
                        "Close all windows" if len(entry.windows) > 1 else "Close",
                        lambda: self.close_windows([number()]),
                    ),
                    MenuItem("Restore all" if len(entry.windows) > 1 else "Restore", lambda: self.restore_windows(entries=entry.windows), enabled=any_minimized),
                    MenuItem("Minimize all" if len(entry.windows) > 1 else "Minimize", lambda: self.minimize_windows(entries=entry.windows), enabled=not all_minimized),
                    MenuItem("Maximize", lambda: self.maximize_window(number())),
                ],
                [
                    # One window snaps; several make a layout.
                    *([MenuItem("Snap  >", page="snap")] if len(entry.windows) == 1 else []),
                    *([MenuItem("Layout  >", page="layout")] if len(entry.windows) > 1 else []),
                    MenuItem("Move all to desktop  >", page="desktop", enabled=vd.available() and len(self.desktops) > 1),
                    *([MenuItem("Move all to screen  >", page="screen")] if self.screen_count > 1 else []),
                ],
                jump_items + edit_items,
            )
        if page == "screen":
            return self._screen_menu(number, here=entry.screen_number)
        if page == "snap":
            return [MenuItem("<  Back", page="main")] + [
                MenuItem(slot_label(slot).capitalize(), lambda slot=slot: self.snap_window(number(), slot))
                for slot in MENU_SNAPS
            ]
        if page == "desktop":
            items = [MenuItem("<  Back", page="main")]
            for desktop in self.desktops:
                current = desktop.guid.key() == entry.desktop_key
                items.append(
                    MenuItem(
                        desktop.label() + (" (here)" if current else ""),
                        lambda n=desktop.number: self.move_to_desktop([number()], number=n),
                        enabled=not current,
                    )
                )
            items.append(MenuItem("New desktop", lambda: self.move_to_new_desktop(number())))
            return items
        return kit_menu.sections(
            [
                MenuItem("Focus", lambda: self._activate(self.entries_at([number()])) if number() else None),
                MenuItem("Close", lambda: self.close_windows([number()])),
                MenuItem("Restore", lambda: self.restore_windows([number()]))
                if entry.minimized
                else MenuItem("Minimize", lambda: self.minimize_windows([number()])),
                MenuItem("Maximize", lambda: self.maximize_window(number())),
            ],
            [
                MenuItem("Snap  >", page="snap"),
                MenuItem("Move to desktop  >", page="desktop", enabled=vd.available()),
                *([MenuItem("Move to screen  >", page="screen")] if self.screen_count > 1 else []),
            ],
            [MenuItem(f"Filter to {entry.app_name}", lambda: self.set_app(entry.app_name), enabled=bool(entry.app_name))] + jump_items,
        )

    def _jump_ids(self, entry) -> list[str]:
        """The ids a tile's jump list may be filed under, best first: the window's or
        process's AppUserModelID (Steam sets "Valve.Steam.Client"), the MMC console's,
        the launch list's, the Start menu entry of its executable (VS Code)."""
        if isinstance(entry, launcher_apps.InstalledApp):
            return [entry.app_id]
        identity = app_identity.resolve(entry.hwnd, getattr(entry, "talon_app_name", entry.app_name))
        ids = [identity.window_id, identity.process_id, identity.document_id]
        launch = getattr(entry, "launch", None)
        if launch is not None:
            ids.append(launch.app_id)
        if identity.exe_path:
            ids.append(shell_apps.app_id_for_path(identity.exe_path))
        return [i for i in ids if i]

    def _launch_entry_id(self, entry) -> str | None:
        """The app's unique_identifier in launch_applications.json, if it has an entry."""
        community = sys.modules.get(launcher_apps.COMMUNITY)
        overrides = getattr(community, "APPLICATIONS_OVERRIDES", None) if community else None
        if not overrides:
            return None
        candidates = [launch_id(entry)]
        if not isinstance(entry, launcher_apps.InstalledApp):
            candidates += self._jump_ids(entry)
        for candidate in candidates:
            found = overrides.get(candidate.lower()) if candidate else None
            if found is not None and getattr(found, "unique_identifier", None):
                return found.unique_identifier
        return None

    def _edit_launch_entry(self, app_id: str):
        """Close the switcher and open the launch applications editor on the entry."""
        self.hide()
        try:
            actions.user.launch_applications_editor_show_entry(app_id)
        except Exception as e:
            app.notify("Launch applications editor", f"Couldn't open it: {e}")

    def _has_jump_list(self, entry) -> bool:
        try:
            return any(jump_lists.has_jump_list(i) for i in self._jump_ids(entry))
        except Exception:
            return False

    def _jump_menu(self, entry, page: str) -> list[MenuItem]:
        """A page of the tile's jump list: category headings, numbered entries,
        separators as dividers; "jump:<n>" pages entries, "jumpremove:<n>" lists recent
        items to remove."""
        kind, _, number = page.partition(":")
        index = int(number or 0)
        jump = jump_lists.jump_list(self._jump_ids(entry))
        items = [MenuItem("<  Back", page="main")]
        if jump is None:
            return items + [MenuItem("No jump list")]
        exe = None if isinstance(entry, launcher_apps.InstalledApp) else app_identity.resolve(entry.hwnd).exe_path
        app_id = jump.app_id
        rows = []
        for category in jump.categories:
            rows.append(MenuItem(category.name, kind="heading"))
            for item in category.entries:
                if item.kind == "separator":
                    rows.append(MenuItem("", kind="separator"))
                    continue
                # Like the taskbar: pinned items can be unpinned; recent ones pinned or
                # removed; app categories' items pinned; tasks neither.
                buttons = []
                if category.kind == "pinned":
                    buttons = [("unpin", lambda item=item: jump_lists.unpin(app_id, item))]
                elif category.kind == "recent":
                    buttons = [
                        ("pin", lambda item=item: jump_lists.pin(app_id, item)),
                        ("remove", lambda item=item: jump_lists.remove(app_id, item)),
                    ]
                elif category.kind == "custom":
                    buttons = [("pin", lambda item=item: jump_lists.pin(app_id, item))]
                rows.append(MenuItem(item.title, lambda item=item: self._run_jump(item, exe), buttons=buttons, icon=(item, app_id)))
        pages = max(1, -(-len(rows) // JUMP_PAGE_ROWS))
        index = max(0, min(index, pages - 1))
        items += rows[index * JUMP_PAGE_ROWS : (index + 1) * JUMP_PAGE_ROWS]
        if index > 0:
            items.append(MenuItem("<  Previous", page=f"{kind}:{index - 1}"))
        if index < pages - 1:
            items.append(MenuItem("More  >", page=f"{kind}:{index + 1}"))
        return items

    def _run_jump(self, item, exe: str | None):
        """Open a jump list entry and close the switcher; the app takes the focus."""
        try:
            jump_lists.run(item, exe)
        except OSError as e:
            app.notify("Jump list", f"Couldn't open {item.title}: {e}")
            return
        self.hide()

    def _screen_menu(self, number, here: int | None) -> list[MenuItem]:
        """The screens submenu: each screen (the window's own greyed out), next, previous."""
        items = [MenuItem("<  Back", page="main")]
        for n in range(1, self.screen_count + 1):
            items.append(
                MenuItem(
                    f"Screen {n}" + (" (here)" if n == here else ""),
                    lambda n=n: self.move_to_screen(number(), screen=n),
                    enabled=n != here,
                )
            )
        items.append(MenuItem("Next screen", lambda: self.move_to_screen(number(), offset=1)))
        items.append(MenuItem("Previous screen", lambda: self.move_to_screen(number(), offset=-1)))
        return items
