from talon import Context, Module
from talon.engine import engine

mod = Module()
@mod.action_class
class Actions:  
    def sleep():
        """Sleep the engine"""
        engine.mimic("go to sleep".split()),
        
    def wake():
        """Wake the engine"""
        engine.mimic("wake up".split()),
