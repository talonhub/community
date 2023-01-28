from talon import Context, Module, actions, ui
mod = Module()
mod.apps.r_s_i_guard_desktop_ergonomics = """
os: windows
and app.name: RSIGuard Desktop Ergonomics
os: windows
and app.exe: RSIGuard.exe
"""
# RSIGuard  v6.2.0.0SB - Registered
def sleep_talon(win):
    if win.title=="RSIGuard  v6.2.0.0SB - Registered":
        actions.user.sleep_all()
        
ui.register("win_focus", sleep_talon)

