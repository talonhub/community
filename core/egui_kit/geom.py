"""Short constructors for egui geometry."""

import egui


def P(x: float, y: float) -> egui.Pos2:
    return egui.Pos2(x, y)


def R(x: float, y: float, w: float, h: float) -> egui.Rect:
    return egui.Rect.from_min_size(egui.Pos2(x, y), egui.Vec2(w, h))
