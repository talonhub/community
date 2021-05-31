import datetime
from talon import Context, actions, Module

mod = Module()
apps = mod.apps
ctx = Context()

@mod.action_class
class Actions:
    def date_now() -> str:
        """Return the current date"""
        return str( datetime.date.today() )
    def date_now_utc() -> str:
        """Return the current UTC date"""
        return str( datetime.datetime.utcnow().date() )
    def timestamp_now() -> str:
        """Return the current timestamp"""
        return str( datetime.datetime.now() ).split( '.' )[ 0 ]
    def timestamp_now_hires() -> str:
        """Return the current timestamp with fractional second"""
        return str( datetime.datetime.now() )
    def timestamp_now_utc() -> str:
        """Return the current UTC timestamp"""
        return str( datetime.datetime.utcnow() ).split( '.' )[ 0 ]
    def timestamp_now_utc_hires() -> str:
        """Return the current UTC timestamp with fractional second"""
        return str( datetime.datetime.utcnow() )
