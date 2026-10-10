import datetime as dt

from talon import actions

# Tells us the last time a notification was shown so we can
# decide when to re-show it without annoying the user too
# much
notification_last_shown = {}


def debounce_notify(
    id: str, message: str, debounce_hours: float = 24.0, **notify_kwargs
):
    """
    Notify the user, at most once every `debounce_hours`.
    id uniquely identifies this message family, messages with the same id will be debounced together.
    notify_kwargs are passed directly to actions.app.notify
    """
    last_shown = notification_last_shown.get(id)
    now = dt.datetime.now()
    threshold = now + dt.timedelta(hours=debounce_hours)
    if not last_shown or last_shown > threshold:
        actions.app.notify(message, **notify_kwargs)
        notification_last_shown[id] = now
