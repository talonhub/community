from talon import Context, Module
from talon.engine import engine

mod = Module()
@mod.action_class
class Actions:  
    def engine_sleep():
        """Sleep the engine"""
        engine.mimic("go to sleep".split()),
        
    def engine_wake():
        """Wake the engine"""
        engine.mimic("wake up".split()),

    def engine_mimic(cmd: str):
        """Sends phrase to engine"""
        engine.mimic(cmd.split())
