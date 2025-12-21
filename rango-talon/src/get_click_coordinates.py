from talon import actions, skia, ui
from talon.experimental import locate
from talon.skia import Rect

from .command import run_simple_command, run_targeted_command

COLORS_A = [0xD75353, 0x53D753, 0x5353D7, 0xD75353]
COLORS_B = [0x737373, 0xDF5656, 0x1616DF, 0x959595]
COLORS_C = [0x53D753, 0xD75353, 0xD75353, 0x53D753]
COLORS_D = [0x595959, 0xDF5656, 0x1616DF, 0x959595]


def create_4x4_image(colors):
    pixels = []

    for color in colors:
        red = (color >> 16) & 0xFF
        green = (color >> 8) & 0xFF
        blue = color & 0xFF
        pixels.extend([red, green, blue, 255])

    pixels = bytes(pixels)

    stride = 2 * 4
    height = 2
    width = 2

    return skia.Image.from_pixels(
        pixels,
        stride,
        width,
        height,
        skia.Image.ColorType.RGBA_8888,
        skia.Image.AlphaType.OPAQUE,
    )


def draw_and_locate_pattern(
    target: dict, colors: list[int], threshold: float, rect: Rect = None
):
    run_targeted_command("drawLocatePattern", target, colors=colors)
    actions.sleep("100ms")
    img = create_4x4_image(colors)
    matches = locate.locate(
        img, rect=rect or ui.active_window().rect, threshold=threshold
    )
    run_simple_command("removeLocatePattern")

    return matches


def get_click_coordinates(target: dict):
    """Get the coordinates to click on an element"""
    alternatives = [(COLORS_A, 0.98), (COLORS_B, 0.95), (COLORS_C, 0.93)]

    for colors, threshold in alternatives:
        matches = draw_and_locate_pattern(target, colors, threshold=threshold)
        if matches:
            break
    else:
        raise Exception(
            "Unable to find pattern to locate element after trying all patterns"
        )

    if len(matches) > 1:
        for match in matches:
            new_matches = draw_and_locate_pattern(
                target, PATTERN_D, threshold=0.95, rect=match
            )
            if new_matches:
                return match.x, match.y

    return matches[0].x, matches[0].y
