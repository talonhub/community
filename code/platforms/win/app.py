# defines the default app actions for windows

import os
from talon import Context, actions, ui, app

# we expect this import to succeed on windows (only)
if app.platform == 'windows':
    import win32gui

ctx = Context()
ctx.matches = r"""
os: windows
"""

# adapted this from code posted by @PeterLinder
# this is a wrapper around the win32 EnumWindows() function, which is documented
# here - https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows.
# you might think that 'top level windows' are non-hidden, non-background windows that are
# not child windows...but you'd be wrong.
def get_top_level_windows():
    def enumHandler(hwnd, resultList):
        resultList.append(hwnd)

    top_level_windows = []

    win32gui.EnumWindows(enumHandler, top_level_windows)
    return top_level_windows

def _focus_neighbor_window(direction: int) -> ui.Window:
    """
    focuses the n-th next or n-th previous instance of the current
    app, depending on the magnitude and sign of the 'direction' arg.
    """
    active_window = ui.active_window()
    active_app = active_window.app

    top_level_windows = get_top_level_windows()
    
    # don't use .hidden for now, as the cached value may be stale (https://github.com/talonvoice/talon/issues/494#issuecomment-1059517184)
    # app_windows = [w for w in ui.windows() if w.app.name == active_app.name and not w.hidden and w.id in top_level_windows]
    app_windows = [w for w in ui.windows() if w.app.name == active_app.name and win32gui.IsWindowVisible(w.id) and w.id in top_level_windows]

    # Windows Explorer is a special case
    if active_app.name == 'Windows Explorer':
        app_windows = [w for w in app_windows if len(w.title) > 0 and os.path.exists(w.title)]
        # for w in app_windows:
        #     if len(w.title) > 0:
        #         pass
        
    app_windows.sort(key=lambda w: w.id)
    window_count = len(app_windows)
    # print(f'_focus_neighbor_window: app_windows: {len(app_windows)=}, {[w.id for w in app_windows]}')
    
    for i in range(window_count):
        if app_windows[i].id == active_window.id:
            target_idx = (i + direction) % window_count
            target_window = app_windows[target_idx]
            
            actions.user.switcher_focus_window(target_window)

            break

@ctx.action_class('app')
class AppActions:
    #app.preferences()
    
    def tab_close():
        actions.key('ctrl-w')
        #action(app.tab_detach):
        #  Move the current tab to a new window
    def tab_next():
        actions.key('ctrl-tab')
    def tab_open():
        actions.key('ctrl-t')
    def tab_previous():
        actions.key('ctrl-shift-tab')
    def tab_reopen():
        actions.key('ctrl-shift-t')
    def window_close():
        actions.key('alt-f4')
    def window_hide():
        actions.key('alt-space n')
    def window_hide_others():
        actions.key('win-d alt-tab')
    def window_next():
        _focus_neighbor_window(1)
    def window_open():
        actions.key('ctrl-n')
        #requires easy window switcher or equivalent (built into most Linux)
    def window_previous():
        _focus_neighbor_window(-1)
