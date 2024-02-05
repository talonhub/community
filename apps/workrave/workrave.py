from talon import Context, Module, actions, app, ui
mod = Module()
mod.apps.workrave = """
os: windows
and app.name: Workrave
os: windows
and app.exe: Workrave.exe
"""
def win_event_handler(window):
    if window.title == "Rest break":
        actions.speech.disable()
        
def register_events():
    ui.register("win_title", win_event_handler)

# prevent scary errors in the log by waiting for talon to be fully loaded
# before registering the events
app.register("ready", register_events)

