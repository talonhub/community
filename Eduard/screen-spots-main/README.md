# screen-spots
Save a set of screen locations to later click on or move to using talon voice.

Defines shortcuts for saving the current mouse coordinates to a specific word/phrase. You can then use another shortcut with the same phrase to either move the mouse cursor to the saved position, or click on the saved position and immediately return the cursor to its current position.

The intended use case is to save the position of buttons or other frequently used locations so that you can click on them or return to them more quickly and with less effort.

Your spots are automatically saved to a file so you maintain your set across restarts.

# Installation
Assumes you already have Talon Voice: https://talonvoice.com/

Clone or copy this entire repo into the user/ directory of your talon installation. 

# Examples (view screen-spots.talon for a full list of commands)
Place your mouse cursor over something you click a lot.

Say "spot save one"

Use your cursor as per usual

Say "spot click one" or "spot one" whenever you want to click that spot

Move your mouse somewhere new

Say "spot save enemy"

Say "spot move enemy" whenever you want to move your mouse over that spot

Say "spot drag enemy" to click and drag from the current mouse position to that spot

Say "spot heatmap" to toggle showing all saved spots with a small coloured circle on the screen

Check screen-spots.talon for more commands. You can delete some or all spots and list all spot names

# Talon Settings
You can use the following settings to customize how this tool functions. You can refer to the unofficial talon wiki for how [talon settings](https://talon.wiki/unofficial_talon_docs/#settings) work.

- `screen_spots_heatmap_color` the color of the drawn dots in the spot heatmap, default="ff0F9D58"
- `screen_spots_heatmap_size` the size of the drawn dots in the spot heatmap, default=5
- `screen_spots_slow_move_enabled` slows the mouse's movement speed during spot commands when enabled (some games don't detect the instant mouse movement correctly). Set to 0 (the default) to disable, any other number to enable
- `screen_spots_slow_move_distance` the maximum distance to move in either direction per tick during slow movement, default=200

# Working Items
? move some of the commands into a menu only ?
    - fewer commands to conflict with spot [move] <user.text>

sometimes coordinates would be better if relative to the current window, could toggle with a command
    * reference talon_ui_helper

? application specific spot sets?

command to reload from backup
