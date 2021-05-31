import datetime
from talon import Context, actions, Module

mod = Module()
apps = mod.apps
ctx = Context()

@mod.action_class
class Actions:
    def time_format(fmt: str=None) -> str:
        """Return current local date or datetime formatted as a str using 'fmt', which
should be a .strftime() style format string; if 'fmt' is not
specified, iso format is used"""
        now = datetime.datetime.now()
        if fmt is None:
            return now.isoformat()
        return now.strftime(fmt)

    def time_format_utc(fmt: str=None) -> str:
        """Return current UTC date or datetime formatted as a str using 'fmt', which
should be a .strftime() style format string; if 'fmt' is not
specified, iso format is used"""
        now = datetime.datetime.utcnow()
        if fmt is None:
            return now.isoformat()
        return now.strftime(fmt)
