from talon import Context, Module, actions, ui, app

mod = Module()
mod.apps.rsi_guard = """
os: windows
and app.name: RSIGuard Desktop Ergonomics
os: windows
and app.exe: RSIGuard.exe
"""
mod.apps.rsi_guard = """
os: mac
and app.bundle: com.enviance.rsiguard
"""
windows_titles = ["RSIGuard  v6.2.0.0SB - Registered"]
mac_titles = ["exceeded max", "break provided", "exposure"]
# RSIGuard  v6.2.0.0SB - Registered
def sleep_talon(win):
    if app.platform == "mac" and actions.app.bundle() == "com.enviance.rsiguard":
        for title in mac_titles:
            if title in win.title.lower():
                actions.user.sleep_all()
    elif app.platform == "windows":
        if win.title in windows_titles:
            actions.user.sleep_all()
        
# ui.register("win_focus", sleep_talon)