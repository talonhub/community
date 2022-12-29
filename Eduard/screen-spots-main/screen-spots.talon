mode: command
-
# save a mouse position to a spot name
spot save <user.text>: user.save_spot(user.text)

# click a saved spot then return the cursor to its prior position
spot [(click|touch)] <user.text>: user.click_spot(user.text)

# move the cursor to a saved spot
spot move <user.text>: user.move_to_spot(user.text)

# hold left click then move the cursor to a saved spot
spot drag <user.text>: user.drag_spot(user.text)

spot swipe <user.text>: user.drag_spot(user.text, 1)

# deletes all current spots (does not alter the cached dictionary of spots)
spot clear all: user.clear_spot_dictionary()

# delete a specific spot (does not alter the cached dictionary of spots)
spot clear <user.text>: user.clear_spot(user.text)

# display a list of all active spot names
spot list [all]: user.list_spot()

# Close the list of active spot names. including 'clothes' because that's commonly misheard by talon
spot (close|clothes)$: user.close_spot_list()

# displays a small colored circle at the location of each saved spot
spot [toggle] heatmap: user.toggle_spot_heatmap()
