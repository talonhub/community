parrot(rree):
	# close zoom if open
    user.zoom_close()
    mouse_click(1)
    # close the mouse grid if open
    user.grid_close()

parrot(hiss):
	#user.mouse_normal_scroll()
	user.mouse_gaze_scroll()
	