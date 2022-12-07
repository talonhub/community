from typing import Callable, Optional

from talon import Context, Module, actions, app, cron

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
    current_key: Optional[str] = None
    callback: Optional[Callable] = None

    def on_confirm(key: str, fn: Callable, timeout: str = "3s"):
        """Prompt for confirmation within timeout"""
        global current_key, callback
        current_key = key
        callback = fn
        app.notify(title="Confirm?", subtitle=key)
        cron.after(timeout, actions.user.cancel_confirm)

    def cancel_confirm():
        """Cancel current confirmation prompt"""
        global current_key, callback
        if current_key:
            app.notify(title="Cancelled", subtitle=current_key)
            current_key = None
            callback = None

    def confirm(key: str):
        """Confirm and execute callback"""
        global current_key, callback
        if current_key == key and callback:
            app.notify(title="Confirmed", subtitle=current_key)
            callback()
            current_key = None
            callback = None
