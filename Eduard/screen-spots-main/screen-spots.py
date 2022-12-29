from talon import ctrl, Module, actions, storage, imgui, ui, canvas
from talon.skia import  Paint

mod = Module()

setting_heatmap_color = mod.setting(
    "screen_spots_heatmap_color",
    type=str,
    default="ff0F9D58",
    desc="set the color of the drawn dots in the spot heatmap",
)

setting_heatmap_size = mod.setting(
    "screen_spots_heatmap_size",
    type=int,
    default=5,
    desc="set the size of the drawn dots in the spot heatmap",
)

setting_slow_move_enabled = mod.setting(
    "screen_spots_slow_move_enabled",
    type=int,
    default=0,
    desc="slows the mouse's movement speed during spot commands when enabled (some games don't detect the instant mouse movement correctly). Set to 0 (the default) to disable, any other number to enable",
)

# Initialize with the spots in storage if there are any. All keys should be strings
spot_dictionary = storage.get("screen-spots", {})

heatmap_showing = False


@imgui.open(y=0)
def gui_list_keys(gui: imgui.GUI):
    global spot_dictionary

    gui.text("spot names")
    gui.line()

    for key in spot_dictionary:
        gui.text(key)

    gui.spacer()

    if gui.button("Spot close"):
        actions.user.close_spot_list()



def backup_spot():
    """Save the spot dictionary to be used again upon reload"""
    storage.set("screen-spots", spot_dictionary)

can = canvas.Canvas.from_screen(ui.main_screen())

def draw_spot(canvas):
    canvas.paint.color = setting_heatmap_color.get()
    canvas.paint.style = Paint.Style.FILL
    for key, spot in spot_dictionary.items():
        canvas.draw_circle(spot[0], spot[1], setting_heatmap_size.get())

can.register('draw', draw_spot)
can.hide()

def refresh():
    if heatmap_showing:
        can.freeze()

@mod.action_class
class SpotClass:
    def save_spot(spot_key: str):
        """Saves the current mouse position (to a specific key phrase)"""
        x = actions.mouse_x()
        y = actions.mouse_y()

        spot_dictionary[spot_key] = [x, y]
        refresh()
        backup_spot()

    def toggle_spot_heatmap():
        """Display the spot on the screen"""
        global can, heatmap_showing
        if heatmap_showing:
            can.hide()
            heatmap_showing = False
        else:
            can.freeze()
            heatmap_showing = True

    def move_to_spot(spot_key: str) -> bool:
        """
        Moves the cursor to a location, if one was saved for the given key.
        Returns true if the cursor was moved
        """
        if spot_key in spot_dictionary:
            spot = spot_dictionary[spot_key]

            if setting_slow_move_enabled.get():
                actions.user.slow_mouse_move(spot[0], spot[1])
            else:
                actions.mouse_move(spot[0], spot[1])
            return True
        return False

    def click_spot(spot_key: str):
        """Clicks the saved mouse position (if it exists) then returns your cursor to its current position"""
        current_x = actions.mouse_x()
        current_y = actions.mouse_y()

        was_moved = actions.user.move_to_spot(spot_key)

        if was_moved:
            if setting_slow_move_enabled.get():
                actions.user.slow_mouse_click()
                actions.user.slow_mouse_move(current_x, current_y)
            else:
                ctrl.mouse_click(button=0, hold=16000)
                actions.mouse_move(current_x, current_y)

    def drag_spot(spot_key: str, release_drag: int=0):
        """Drag the mouse from its current location to the saved position (if it exists)"""
        if spot_key in spot_dictionary:
            actions.user.mouse_drag(0)
            actions.user.move_to_spot(spot_key)
            if release_drag != 0:
                actions.sleep("50ms")
                actions.mouse_release(0)

    def clear_spot_dictionary():
        """Reset the active spot list to a new empty dictionary"""
        global spot_dictionary
        spot_dictionary = {}
        backup_spot()
        refresh()
        
    def clear_spot(spot_key: str):
        """Remove a specific saved spot"""
        global spot_dictionary
        if spot_key in spot_dictionary:
            del spot_dictionary[spot_key]
            backup_spot()
            refresh()

    def list_spot():
        """Display a list of existing spot names"""
        gui_list_keys.show()

    def close_spot_list():
        """Closes the list of existing spot names"""
        gui_list_keys.hide()
