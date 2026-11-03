"""The shared look of Talon egui tools: colour tokens, type and metrics.

THEME is the one look every tool uses (dark).
"""

from dataclasses import dataclass

import egui


def rgb(hex_color: str) -> egui.Color32:
    h = hex_color.lstrip("#")
    return egui.Color32.from_rgb(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def font(size: float) -> egui.FontId:
    return egui.FontId.proportional(size)


def mono(size: float) -> egui.FontId:
    return egui.FontId.monospace(size)


@dataclass(frozen=True)
class Theme:
    dark: bool
    # Surfaces
    bg: egui.Color32  # the window
    surface: egui.Color32  # tiles, cards, inputs
    surface_hover: egui.Color32  # a hovered tile
    surface_alt: egui.Color32  # header strips, column headings
    border: egui.Color32
    divider: egui.Color32  # lines between rows
    input_border: egui.Color32
    hover: egui.Color32  # a hovered row or button
    # Text
    text: egui.Color32
    text_muted: egui.Color32  # secondary text, hints
    text_label: egui.Color32  # small caps section labels
    text_faint: egui.Color32  # disabled
    text_off: egui.Color32  # unavailable choices (an index letter with nothing under it)
    white: egui.Color32
    # Accent (focus, selection, primary buttons)
    accent: egui.Color32
    accent_hover: egui.Color32
    accent_disabled: egui.Color32
    on_accent: egui.Color32  # text on accent fills
    selected_row: egui.Color32
    selected_nav: egui.Color32  # the chosen item of a nav list
    # Chips and badges
    chip_bg: egui.Color32
    chip_text: egui.Color32
    chip_hover: egui.Color32  # a chip's remove button, hovered
    auto_chip_bg: egui.Color32  # generated values, shown but not stored
    auto_chip_border: egui.Color32
    badge_desktop: egui.Color32  # the current virtual desktop's badge
    badge_screen: egui.Color32
    # Status
    success: egui.Color32  # running, saved
    danger: egui.Color32  # close buttons, hovered
    warn_bg: egui.Color32
    warn_text: egui.Color32
    warn_dot: egui.Color32
    warn_hover: egui.Color32
    mark: egui.Color32  # multi-select outline and check
    mark_fill: egui.Color32
    # Controls
    track_off: egui.Color32  # a toggle that's off
    menu_bg: egui.Color32
    menu_border: egui.Color32
    menu_hover: egui.Color32
    shadow: egui.Color32
    # Corner radii: controls, chips and tiles; containers (cards, menus).
    radius: float = 6.0
    radius_card: float = 8.0

    def apply(self, ctx: "egui.Context"):
        """egui's own widgets (text fields, combo boxes) follow the theme's lightness."""
        ctx.set_visuals(egui.Visuals.dark() if self.dark else egui.Visuals.light())


THEME = Theme(
    dark=True,
    bg=egui.Color32.from_rgb(24, 24, 28),
    surface=egui.Color32.from_rgb(40, 40, 46),
    surface_hover=egui.Color32.from_rgb(60, 70, 95),
    surface_alt=egui.Color32.from_rgb(32, 32, 37),
    border=egui.Color32.from_rgb(90, 90, 100),
    divider=egui.Color32.from_rgb(52, 52, 58),
    input_border=egui.Color32.from_rgb(90, 90, 100),
    hover=egui.Color32.from_rgb(52, 52, 60),
    text=egui.Color32.from_rgb(235, 235, 235),
    text_muted=egui.Color32.from_rgb(150, 150, 160),
    text_label=egui.Color32.from_rgb(170, 170, 180),
    text_faint=egui.Color32.from_rgb(110, 110, 120),
    text_off=egui.Color32.from_rgb(80, 80, 88),
    white=egui.Color32.from_rgb(255, 255, 255),
    accent=egui.Color32.from_rgb(70, 150, 255),
    accent_hover=egui.Color32.from_rgb(100, 170, 255),
    accent_disabled=egui.Color32.from_rgb(55, 75, 105),
    on_accent=egui.Color32.from_rgb(255, 255, 255),
    selected_row=egui.Color32.from_rgb(38, 52, 78),
    selected_nav=egui.Color32.from_rgb(45, 60, 90),
    chip_bg=egui.Color32.from_rgb(45, 85, 150),
    chip_text=egui.Color32.from_rgb(255, 255, 255),
    chip_hover=egui.Color32.from_rgb(65, 110, 185),
    auto_chip_bg=egui.Color32.from_rgb(40, 40, 46),
    auto_chip_border=egui.Color32.from_rgb(90, 90, 100),
    badge_desktop=egui.Color32.from_rgb(45, 110, 80),
    badge_screen=egui.Color32.from_rgb(105, 80, 140),
    success=egui.Color32.from_rgb(80, 200, 120),
    danger=egui.Color32.from_rgb(196, 43, 28),
    warn_bg=egui.Color32.from_rgb(74, 52, 24),
    warn_text=egui.Color32.from_rgb(245, 190, 110),
    warn_dot=egui.Color32.from_rgb(230, 140, 40),
    warn_hover=egui.Color32.from_rgb(100, 70, 32),
    mark=egui.Color32.from_rgb(230, 160, 40),
    mark_fill=egui.Color32.from_rgb(66, 56, 38),
    track_off=egui.Color32.from_rgb(80, 80, 90),
    menu_bg=egui.Color32.from_rgb(44, 44, 46),
    menu_border=egui.Color32.from_rgb(72, 72, 78),
    menu_hover=egui.Color32.from_rgb(64, 64, 70),
    shadow=egui.Color32.from_rgb(10, 10, 12),
)
