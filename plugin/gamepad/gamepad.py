from talon import Module, actions, ctrl, ui
from talon.screen import Screen

screen: Screen = ui.main_screen()
slow_scroll = False
slow_mouse_move = False

mod = Module()
mod.tag("gamepad", desc="Activate tag to enable gamepad bindings")


@mod.action_class
class Actions:
    # DPAD buttons

    def gamepad_press_dpad_left():
        """Gamepad press button dpad left"""
        gamepad_mouse_jump("left")

    def gamepad_release_dpad_left():
        """Gamepad release button dpad left"""
        actions.skip()

    def gamepad_press_dpad_up():
        """Gamepad press button dpad up"""
        gamepad_mouse_jump("up")

    def gamepad_release_dpad_up():
        """Gamepad release button dpad up"""
        actions.skip()

    def gamepad_press_dpad_right():
        """Gamepad press button dpad right"""
        gamepad_mouse_jump("right")

    def gamepad_release_dpad_right():
        """Gamepad release button dpad right"""
        actions.skip()

    def gamepad_press_dpad_down():
        """Gamepad press button dpad down"""
        gamepad_mouse_jump("down")

    def gamepad_release_dpad_down():
        """Gamepad release button dpad down"""
        actions.skip()

    # Compass / ABXY buttons

    def gamepad_press_west():
        """Gamepad press button west"""
        actions.mouse_drag(0)

    def gamepad_release_west():
        """Gamepad release button west"""
        actions.mouse_release(0)

    def gamepad_press_north():
        """Gamepad press button north"""
        actions.mouse_drag(1)

    def gamepad_release_north():
        """Gamepad release button north"""
        actions.mouse_release(1)

    def gamepad_press_east():
        """Gamepad press button east"""
        actions.key("ctrl:down")
        actions.mouse_click()
        actions.key("ctrl:up")

    def gamepad_release_east():
        """Gamepad release button east"""
        actions.skip()

    def gamepad_press_south():
        """Gamepad press button south"""
        actions.mouse_drag(2)

    def gamepad_release_south():
        """Gamepad release button south"""
        actions.mouse_release(2)

    # Select / Start buttons

    def gamepad_press_select():
        """Gamepad press button select"""
        actions.skip()

    def gamepad_release_select():
        """Gamepad release button select"""
        actions.skip()

    def gamepad_press_start():
        """Gamepad press button start"""
        actions.speech.toggle()

    def gamepad_release_start():
        """Gamepad release button start"""
        actions.skip()

    # Shoulder buttons

    def gamepad_press_left_shoulder():
        """Gamepad press button left shoulder"""
        actions.user.go_back()

    def gamepad_release_left_shoulder():
        """Gamepad release button left shoulder"""
        actions.skip()

    def gamepad_press_right_shoulder():
        """Gamepad press button right shoulder"""
        actions.user.go_forward()

    def gamepad_release_right_shoulder():
        """Gamepad release button right shoulder"""
        actions.skip()

    # Stick buttons

    def gamepad_press_left_stick():
        """Gamepad press button left thumb stick"""
        gamepad_scroll_slow_toggle()

    def gamepad_release_left_stick():
        """Gamepad release button left thumb stick"""
        actions.skip()

    def gamepad_press_right_stick():
        """Gamepad press button right thumb stick"""
        gamepad_mouse_move_slow_toggle()

    def gamepad_release_right_stick():
        """Gamepad release button right thumb stick"""
        actions.skip()

    # Analog triggers

    def gamepad_trigger_left(value: float):
        """Gamepad trigger left movement"""
        gamepad_scroll(0, value * -1)

    def gamepad_trigger_right(value: float):
        """Gamepad trigger right movement"""
        gamepad_scroll(0, value)

    # Analog thumb sticks

    def gamepad_stick_left(x: float, y: float):
        """Gamepad left stick movement"""
        gamepad_scroll(x, y)

    def gamepad_stick_right(x: float, y: float):
        """Gamepad right stick movement"""
        gamepad_mouse_move(x, y)

    # Scaffolding actions used by the Talon file

    def gamepad_button_down(button: str):
        """Gamepad press button <button>"""
        match button:
            # DPAD buttons
            case "dpad_left":
                actions.user.gamepad_press_dpad_left()
            case "dpad_up":
                actions.user.gamepad_press_dpad_up()
            case "dpad_right":
                actions.user.gamepad_press_dpad_right()
            case "dpad_down":
                actions.user.gamepad_press_dpad_down()

            # Compass / ABXY buttons
            case "west":
                actions.user.gamepad_press_west()
            case "north":
                actions.user.gamepad_press_north()
            case "east":
                actions.user.gamepad_press_east()
            case "south":
                actions.user.gamepad_press_south()

            # Select / Start buttons
            case "select":
                actions.user.gamepad_press_select()
            case "start":
                actions.user.gamepad_press_start()

            # Shoulder buttons
            case "left_shoulder":
                actions.user.gamepad_press_left_shoulder()
            case "right_shoulder":
                actions.user.gamepad_press_right_shoulder()

            # Stick buttons
            case "left_stick":
                actions.user.gamepad_press_left_stick()
            case "right_stick":
                actions.user.gamepad_press_right_stick()

            case _:
                raise ValueError(f"Unknown button: {button}")

    def gamepad_button_up(button: str):
        """Gamepad release button <button>"""
        match button:
            # DPAD buttons
            case "dpad_left":
                actions.user.gamepad_release_dpad_left()
            case "dpad_up":
                actions.user.gamepad_release_dpad_up()
            case "dpad_right":
                actions.user.gamepad_release_dpad_right()
            case "dpad_down":
                actions.user.gamepad_release_dpad_down()

            # Compass / ABXY buttons
            case "west":
                actions.user.gamepad_release_west()
            case "north":
                actions.user.gamepad_release_north()
            case "east":
                actions.user.gamepad_release_east()
            case "south":
                actions.user.gamepad_release_south()

            # Select / Start buttons
            case "select":
                actions.user.gamepad_release_select()
            case "start":
                actions.user.gamepad_release_start()

            # Shoulder buttons
            case "left_shoulder":
                actions.user.gamepad_release_left_shoulder()
            case "right_shoulder":
                actions.user.gamepad_release_right_shoulder()

            # Stick buttons
            case "left_stick":
                actions.user.gamepad_release_left_stick()
            case "right_stick":
                actions.user.gamepad_release_right_stick()

            case _:
                raise ValueError(f"Unknown button: {button}")


def gamepad_scroll(x: float, y: float):
    """Perform gamepad scrolling"""
    multiplier = 1.5 if slow_scroll else 3
    x = x**3 * multiplier
    y = y**3 * multiplier

    if x != 0 or y != 0:
        actions.mouse_scroll(x=x, y=y, by_lines=True)


def gamepad_mouse_move(dx: float, dy: float):
    """Perform gamepad mouse cursor movement"""
    multiplier = 0.1 if slow_mouse_move else 0.2
    x, y = ctrl.mouse_pos()
    screen = get_screen(x, y)
    dx = dx**3 * screen.dpi * multiplier
    dy = dy**3 * screen.dpi * multiplier
    actions.mouse_move(x + dx, y + dy)


def gamepad_scroll_slow_toggle():
    """Toggle gamepad slow scroll mode"""
    global slow_scroll
    slow_scroll = not slow_scroll


def gamepad_mouse_move_slow_toggle():
    """Toggle gamepad slow mouse move mode"""
    global slow_mouse_move
    slow_mouse_move = not slow_mouse_move


def gamepad_mouse_jump(direction: str):
    """Move the mouse cursor to the specified quadrant of the active screen"""
    x, y = ctrl.mouse_pos()
    rect = ui.screen_containing(x, y).rect
    print(ui.active_window())

    # Half distance between cursor and screen edge
    match direction:
        case "up":
            y = rect.top + (y - rect.top) / 2
        case "down":
            y = rect.bot - (rect.bot - y) / 2
        case "left":
            x = rect.left + (x - rect.left) / 2
        case "right":
            x = rect.right - (rect.right - x) / 2

    actions.mouse_move(x, y)


def get_screen(x: float, y: float) -> Screen:
    global screen
    if not screen.contains(x, y):
        screen = ui.screen_containing(x, y)
    return screen
