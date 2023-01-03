import os
from talon import Module, ui

mod = Module()

@mod.action_class
class Actions:
    def talon_restart():
        """restart talon"""
        talon_app = ui.apps(pid=os.getpid())[0]
        print("Restarting:", talon_app)
        os.startfile(talon_app.exe)
        talon_app.quit()
        
    def talon_quit():
        """quit talon"""
        talon_app = ui.apps(pid=os.getpid())[0]
        print("Quitting:", talon_app)
