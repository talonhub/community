# egui support

This is currently not part of our stable API and may undergo significant revision.

## setting up a gui

You can set up a gui by using the open_gui decorator on a callback function that renders on an egui Oi. This callback will be passed 2 arguments: an egui.UI object and a UIWrapper wrapping the egui.UI. The wrapper offers convenience methods.

The decorator returns a GUI object. Its methods include `show` for showing the gui, `hide` for hiding the gui, `focus` for focusing the gui, and `refresh` for forcing the gui to refresh even if the user is not interacting with it. If you want the gui to get refreshed periodically, use the refresh_period argument of the open_gui decorator with a time specification string such as "500ms" to refresh every 500 milliseconds.
