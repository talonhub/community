import datetime
from talon import Context, actions, Module

mod = Module()
apps = mod.apps
ctx = Context()

@mod.action_class
class Actions:
    def date_fill():
        """Insert the current date"""
        actions.insert( str( datetime.date.today() ) )
    def date_fill_utc():
        """Insert the current UTC date"""
        actions.insert( str( datetime.datetime.utcnow().date() ) )
    def timestamp_fill():
        """Insert the current timestamp"""
        actions.insert( str( datetime.datetime.now() ).split( '.' )[ 0 ] )
    def timestamp_fill_hires():
        """Insert the current timestamp with fractional second"""
        actions.insert( str( datetime.datetime.now() ) )
    def timestamp_fill_utc():
        """Insert the current UTC timestamp"""
        actions.insert( str( datetime.datetime.utcnow() ).split( '.' )[ 0 ] )
    def timestamp_fill_utc_hires():
        """Insert the current UTC timestamp with fractional second"""
        actions.insert( str( datetime.datetime.utcnow() ) )
