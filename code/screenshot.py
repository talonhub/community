from talon import Module, screen, ui, actions
from talon.engine import engine
import os
import platform

active_platform = platform.platform(terse=True)

mod = Module()
@mod.action_class
class Actions:
    def screenshot():
        '''takes a screenshot of the entire screen and saves it to the desktop as screenshot.png'''
        img = screen.capture_rect(screen.main_screen().rect)
        path = os.path.expanduser(os.path.join('~', 'Desktop', 'screenshot.png'))
        img.write_file(path)
        
    def screenshot_window():
        '''takes a screenshot of the current window and says it to the desktop as screenshot.png'''
        img = screen.capture_rect(ui.active_window().rect)
        path = os.path.expanduser(os.path.join('~', 'Desktop', 'screenshot.png'))
        img.write_file(path)

    def screenshot_selection():
        '''triggers an application is capable of taking a screenshot of a portion of the screen'''
        if "Windows-10" in active_platform:
            actions.key("super-shift-s")       

    def screenshot_clipboard():
        '''takes a screenshot of the entire screen and saves it to the clipboard'''

        if "Windows-10" in active_platform:
            engine.mimic("press print screen")
            
    def screenshot_window_clipboard():
        '''takes a screenshot of the window and saves it to the clipboard'''
   
        if "Windows-10" in active_platform:
            engine.mimic("press control alt print screen")
            