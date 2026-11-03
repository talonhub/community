"""Context menus: items, the open menu's state, drawing, and keyboard navigation.

Like the Windows 11 Start menu's context menu: 36-point rows, small grey headings, a
gutter with each item's number (for voice and digit keys), an optional icon column,
then the label; submenus show a chevron. Rows can carry small icon buttons at their
end (pin, unpin, remove), each its own UIA element.

The tool builds the items of a page (`pages`) and acts on what comes back: a picked
item, or a page change it applies with `open_page` / `back`. Pages are one level deep:
"main" and its submenus; an item whose `page` is "main" goes back.
"""

import egui

from . import widgets
from .a11y import describe
from .text import elide_estimate
from .widgets import Kit

ITEM_HEIGHT = 36.0
SEPARATOR_HEIGHT = 9.0
PADDING = 4.0
ICON = 16.0
LABEL_X = 52.0  # from the row's left edge, with the icon column
BUTTON = 20.0
WIDTH = 290.0
SUBMENU_MARK = "  >"  # labels ending so open a submenu


class MenuItem:
    def __init__(
        self,
        label: str,
        action=None,
        page: str | None = None,
        enabled: bool = True,
        buttons=(),
        keep_open: bool = False,
        kind: str = "item",
        icon=None,
    ):
        self.label = label
        # "item"; "heading" (a category) or "separator", which do nothing.
        self.kind = kind
        # Something the tool's `icon_texture` turns into a texture for the icon column.
        self.icon = icon
        # Runs after the frame; or `page` opens a submenu instead ("main": back).
        self.action = action
        self.page = page
        self.enabled = enabled and (action is not None or page is not None)
        # Icon buttons at the row's end, as (glyph, action): "pin", "unpin", "remove".
        self.buttons = list(buttons)
        # Runs without closing the menu (the buttons' actions).
        self.keep_open = keep_open


class MenuState:
    """An open menu: its page and highlighted row. Tools subclass it to say what the
    menu is for."""

    def __init__(self, page: str = "main", dropdown: bool = False):
        self.page = page
        # A dropdown (e.g. under a toolbar button): a single page, no going back.
        self.dropdown = dropdown
        self.highlight = 0
        # The first page's row a submenu was opened from, highlighted again on the way back.
        self.parent_highlight = 0
        # The click that opened it hasn't finished yet (so it doesn't dismiss it).
        self.fresh = False


def sections(*groups: list[MenuItem]) -> list[MenuItem]:
    """The non-empty groups of items, with separators between them."""
    items = []
    for group in groups:
        if group:
            if items:
                items.append(MenuItem("", kind="separator"))
            items.extend(group)
    return items


def numbered(item: MenuItem) -> bool:
    """Whether an item gets a number: enabled ones, except going back."""
    return item.enabled and item.page != "main"


def numbers(items: list[MenuItem]) -> list[int | None]:
    """Each item's number on its page (1-based), or None."""
    result, n = [], 0
    for item in items:
        if numbered(item):
            n += 1
            result.append(n)
        else:
            result.append(None)
    return result


def item_number(items: list[MenuItem], number: int) -> MenuItem | None:
    """The item numbered `number` on its page."""
    items = [item for item in items if numbered(item)]
    return items[number - 1] if 0 < number <= len(items) else None


def row_height(item: MenuItem) -> float:
    return SEPARATOR_HEIGHT if item.kind == "separator" else ITEM_HEIGHT


def height(items: list[MenuItem]) -> float:
    return sum(row_height(item) for item in items) + 2 * PADDING


# --- state changes ---


def back(state: MenuState):
    """Back from a submenu to the first page (a dropdown has none)."""
    if not state.dropdown:
        state.page, state.highlight = "main", state.parent_highlight


def open_page(state: MenuState, page: str, items: list[MenuItem]):
    """Show submenu `page` (its `items`), on its first item past "< Back"."""
    if page == "main":
        back(state)
        return
    if state.page == "main":
        state.parent_highlight = state.highlight
    state.page = page
    state.highlight = next((i for i, it in enumerate(items) if it.enabled and it.page != "main"), 0)


def navigate(state: MenuState, items: list[MenuItem], key: str):
    """Keyboard: Up/Down (Home/End) move the highlight over enabled items. Enter picks
    the highlighted item, Right picks it if it opens a submenu: both return it. Left
    goes back from a submenu (returns "back"). Otherwise returns None."""
    enabled = [i for i, item in enumerate(items) if item.enabled]
    if not enabled:
        return None
    highlighted = items[state.highlight] if state.highlight < len(items) else None
    if key == "Enter":
        return highlighted
    if key == "ArrowRight":
        if highlighted is not None and highlighted.enabled and highlighted.page not in (None, "main"):
            return highlighted
        return None
    if key == "ArrowLeft":
        return "back" if state.page != "main" else None
    if key in ("Home", "End"):
        state.highlight = enabled[0] if key == "Home" else enabled[-1]
        return None
    if key in ("ArrowUp", "ArrowDown"):
        step = 1 if key == "ArrowDown" else -1
        later = [i for i in enabled if (i - state.highlight) * step > 0]
        state.highlight = (min(later) if step > 0 else max(later)) if later else (enabled[0] if step > 0 else enabled[-1])
    return None


# --- drawing ---


def draw_menu(
    ui: egui.Ui,
    kit: Kit,
    state: MenuState,
    items: list[MenuItem],
    rect: egui.Rect,
    *,
    hover: bool = True,
    pointer=None,
    icon_texture=None,
    button_tips: dict | None = None,
    swallow: bool = False,
    shadow: bool = False,
    clicked: bool | None = None,
) -> MenuItem | None:
    """Draw the menu in `rect`; returns the item clicked this frame, if any. A click on
    a row's icon button returns that button's action as an item that keeps the menu
    open. `hover`: the pointer may take the highlight (only while it moves, so it
    doesn't fight the keyboard); `pointer`: its position. `icon_texture(ui, icon)`
    makes an item's icon texture (None while loading). `swallow`: clicks on the
    padding don't fall through. `shadow`: a soft shadow below (light themes).
    `clicked`: the window's own primary click this frame. Given, hover and clicks
    come from `pointer` instead of egui's responses, which stay unhovered in a window
    egui thinks unfocused (a popup that never takes the focus, egui_kit.popup)."""
    t = kit.theme
    painter = ui.painter()
    tips = button_tips or {}
    if shadow:
        painter.rect_filled(rect.translate(egui.Vec2(0, 3)).expand(2), t.radius_card + 2, t.shadow)
    painter.rect_filled(rect, t.radius_card, t.menu_bg)
    painter.rect_stroke(rect, t.radius_card, egui.Stroke(1.0, t.menu_border), egui.StrokeKind.Inside)
    if swallow:
        kit.hit(ui, rect, "menu")
    font = egui.FontId.proportional(14.0)
    picked = None
    nums = numbers(items)
    # The icon column only on pages with icons.
    label_x = LABEL_X if any(item.icon is not None for item in items) else LABEL_X - ICON - 4
    top = rect.min.y + PADDING
    for i, item in enumerate(items):
        row = egui.Rect.from_min_size(egui.Pos2(rect.min.x + PADDING, top), egui.Vec2(rect.width() - 2 * PADDING, row_height(item)))
        top += row.height()
        if item.kind == "separator":
            y = row.center().y
            painter.line_segment(egui.Pos2(rect.min.x, y), egui.Pos2(rect.max.x, y), egui.Stroke(1.0, t.menu_border))
            continue
        if item.kind == "heading":
            # Like the Start menu's: small grey text, further left than the items.
            painter.text(
                egui.Pos2(row.min.x + 10, row.center().y + 2),
                egui.Align2.LEFT_CENTER,
                elide_estimate(item.label, row.width() - 20, 13.0),
                egui.FontId.proportional(13.0),
                t.text_muted,
            )
            continue
        # Icon buttons at the row's end, shown on the highlighted row.
        button_rects = []
        right = row.max.x - 4
        for glyph, action in reversed(item.buttons):
            button = egui.Rect.from_min_size(egui.Pos2(right - BUTTON, row.center().y - BUTTON / 2), egui.Vec2(BUTTON, BUTTON))
            button_rects.append((glyph, action, button))
            right = button.min.x - 4
        # The buttons' own areas first, under the row's (as with tiles' close buttons):
        # UIA elements of their own, while the pointer decides for the mouse.
        invoked = None
        by_pointer = clicked is not None
        for glyph, action, button in button_rects:
            bresp = kit.hit(ui, button, f"menu-button:{state.page}:{i}:{glyph}")
            describe(bresp, egui.WidgetType.Button, f"{tips.get(glyph, glyph)}: {item.label}")
            if bresp.clicked():
                # (By pointer, a click on a button counts below, as the row's.)
                invoked = (glyph, action)
        response = kit.hit(ui, row, f"menu:{state.page}:{i}")
        submenu = item.label.endswith(SUBMENU_MARK)
        describe(response, egui.WidgetType.Button, item.label[: -len(SUBMENU_MARK)] if submenu else item.label, item.enabled)
        row_hovered = (pointer is not None and row.contains(pointer)) if by_pointer else response.hovered()
        # A click from UI Automation (Invoke) still comes as the response's.
        row_clicked = response.clicked() or (by_pointer and clicked and row_hovered)
        if hover and row_hovered and item.enabled and state.highlight != i:
            state.highlight = i
        if state.highlight == i and item.enabled:
            painter.rect_filled(row, 4, t.menu_hover)
        on_button = None
        for glyph, action, button in button_rects:
            over = row_hovered and pointer is not None and button.contains(pointer)
            if over:
                on_button = (glyph, action)
                response.on_hover_text(tips.get(glyph, glyph))
            if state.highlight == i or over:
                widgets.paint_glyph(painter, kit, button, glyph, over)
        # Numbered for voice and digit keys, small and grey in the gutter.
        if nums[i]:
            painter.text(egui.Pos2(row.min.x + 22, row.center().y), egui.Align2.RIGHT_CENTER, str(nums[i]), egui.FontId.proportional(12.0), t.text_muted)
        texture = icon_texture(ui, item.icon) if item.icon is not None and icon_texture is not None else None
        if texture is not None:
            icon_rect = egui.Rect.from_min_size(egui.Pos2(row.min.x + 28, row.center().y - ICON / 2), egui.Vec2(ICON, ICON))
            painter.image(texture.id(), icon_rect, egui.Rect.from_min_max(egui.Pos2(0.0, 0.0), egui.Pos2(1.0, 1.0)), t.white)
        label = item.label
        if submenu:
            # A submenu: its chevron at the row's end, as Windows menus have it.
            label = label[: -len(SUBMENU_MARK)]
            painter.text(egui.Pos2(right - 6, row.center().y), egui.Align2.RIGHT_CENTER, "›", egui.FontId.proportional(18.0), t.text_muted)
        painter.text(
            egui.Pos2(row.min.x + label_x, row.center().y),
            egui.Align2.LEFT_CENTER,
            elide_estimate(label, right - row.min.x - label_x - 20, 14.0),
            font,
            t.text if item.enabled else t.text_muted,
        )
        if invoked is not None:
            picked = MenuItem(invoked[0], invoked[1], keep_open=True)
        elif row_clicked and on_button is not None:
            picked = MenuItem(on_button[0], on_button[1], keep_open=True)
        elif row_clicked and item.enabled:
            picked = item
    return picked
