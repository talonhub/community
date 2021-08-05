from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
os: mac
"""


@ctx.action_class('app')
class AppActions:
    def preferences():
        actions.key('cmd-,')

    def tab_close():
        actions.key('cmd-w')
        # action(app.tab_detach):
        #  Move the current tab to a new window

    def tab_next():
        actions.key('cmd-alt-right')

    def tab_open():
        actions.key('cmd-t')

    def tab_previous():
        actions.key('cmd-alt-left')

    def tab_reopen():
        actions.key('cmd-shift-t')

    def window_close():
        actions.key('cmd-w')

    def window_hide():
        actions.key('cmd-m')

    def window_hide_others():
        actions.key('cmd-alt-h')

    def window_open():
        actions.key('cmd-n')

    def window_previous():
        actions.key('cmd-shift-`')

    # Custom behavior to handle Mac desktop 'Spaces'
    def window_next():
        switch_window_by_offset_from_current(1)

    # Custom behavior to handle Mac desktop 'Spaces'
    def window_previous():
        switch_window_by_offset_from_current(-1)


def switch_window_by_offset_from_current(offset):
    active_window = ui.active_window()
    windows = ui.active_app().windows()

    # Handle case where empty windows with no title show up in the results
    windows = list(filter(lambda local_window: len(local_window.title) > 0, windows))

    # Sort by title since they get reordered on every switch and we want to switch windows in a fixed order
    windows.sort(key=lambda local_window: local_window.title)

    for (index, window) in enumerate(windows):
        if window is active_window:
            index_of_new_window = (index + offset) % len(windows)
            windows[index_of_new_window].focus()
