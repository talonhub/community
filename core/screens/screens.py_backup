from talon import Module, cron, ui
from talon.canvas import Canvas

mod = Module()


@mod.action_class
class Actions:
    def screens_show_numbering():
        """Show screen number on each screen"""
        screens = get_sorted_screens()
        number = 1
        for screen in screens:
            show_screen_number(screen, number)
            number += 1

    def screens_get_by_number(screen_number: int) -> ui.Screen:
        """Get screen by number"""
        screens = get_sorted_screens()
        length = len(screens)
        if screen_number < 1 or screen_number > length:
            raise Exception(
                f"Non-existing screen {screen_number} in range [1, {length}]"
            )
        return screens[screen_number - 1]

    def screens_get_previous(screen: ui.Screen) -> ui.Screen:
        """Get the screen before this one"""
        return get_screen_by_offset(screen, -1)

    def screens_get_next(screen: ui.Screen) -> ui.Screen:
        """Get the screen after this one"""
        return get_screen_by_offset(screen, 1)


def get_screen_by_offset(screen: ui.Screen, offset: int) -> ui.Screen:
    screens = get_sorted_screens()
    index = (screens.index(screen) + offset) % len(screens)
    return screens[index]


def get_sorted_screens():
    """Return screens sorted by their topmost, then leftmost, edge.
    Screens will be sorted leftto-right, then top-to-bottom as a tiebreak.
    """
    return sorted(
        ui.screens(),
        key=lambda screen: screen.visible_rect.left,
    )


def show_screen_number(screen: ui.Screen, number: int):
    def on_draw(c):
        c.paint.typeface = "arial"
        # The min(width, height) is to not get gigantic size on portrait screens
        c.paint.textsize = round(min(c.width, c.height) / 2)
        text = f"{number}"
        rect = c.paint.measure_text(text)[1]
        x = c.x + c.width / 2 - rect.x - rect.width / 2
        y = c.y + c.height / 2 + rect.height / 2

        c.paint.style = c.paint.Style.FILL
        c.paint.color = "eeeeee"
        c.draw_text(text, x, y)

        c.paint.style = c.paint.Style.STROKE
        c.paint.color = "000000"
        c.draw_text(text, x, y)

        cron.after("3s", canvas.close)

    canvas = Canvas.from_rect(screen.rect)
    canvas.register("draw", on_draw)
    canvas.freeze()
